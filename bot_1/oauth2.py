import os
import json
import asyncio
import aiohttp
import requests
from aiohttp import web
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BOT_CLIENT_ID = os.getenv('BOT_CLIENT_ID')
BOT_CLIENT_SECRET = os.getenv('BOT_CLIENT_SECRET')
OAUTH_REDIRECT_URI = os.getenv('OAUTH_REDIRECT_URI', 'http://localhost:8080/callback')
AUTHORIZED_USERS_DB = 'authorized_users.json'

class OAuth2Manager:
    def __init__(self):
        self.authorized_users = self.load_authorized_users()
    
    def load_authorized_users(self):
        """Load authorized users from file"""
        if os.path.exists(AUTHORIZED_USERS_DB):
            with open(AUTHORIZED_USERS_DB, 'r') as f:
                return json.load(f)
        return {}
    
    def save_authorized_users(self):
        """Save authorized users to file"""
        with open(AUTHORIZED_USERS_DB, 'w') as f:
            json.dump(self.authorized_users, f, indent=2)
    
    def get_authorization_url(self):
        """Generate OAuth2 authorization URL for users to click"""
        return (
            f"https://discord.com/api/oauth2/authorize?"
            f"client_id={BOT_CLIENT_ID}&"
            f"redirect_uri={OAUTH_REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=identify%20email"
        )
    
    async def exchange_code_for_token(self, code):
        """Exchange authorization code for access token"""
        data = {
            'client_id': BOT_CLIENT_ID,
            'client_secret': BOT_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': OAUTH_REDIRECT_URI
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post('https://discord.com/api/oauth2/token', data=data) as resp:
                return await resp.json()
    
    async def get_user_info(self, access_token):
        """Get user info from Discord using access token"""
        headers = {'Authorization': f'Bearer {access_token}'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.com/api/users/@me', headers=headers) as resp:
                return await resp.json()
    
    async def authorize_user(self, code):
        """Complete authorization flow: code -> token -> user info -> store"""
        try:
            # Exchange code for token
            token_data = await self.exchange_code_for_token(code)
            if 'error' in token_data:
                return False, f"Error: {token_data['error_description']}"
            
            access_token = token_data['access_token']
            
            # Get user info
            user_info = await self.get_user_info(access_token)
            if 'error' in user_info:
                return False, "Failed to get user info"
            
            user_id = user_info['id']
            username = user_info['username']
            
            # Store authorized user
            self.authorized_users[user_id] = {
                'username': username,
                'access_token': access_token,
                'refresh_token': token_data.get('refresh_token'),
                'authorized_at': str(__import__('datetime').datetime.now())
            }
            self.save_authorized_users()
            
            return True, f"✅ {username} ({user_id}) has been authorized!"
        
        except Exception as e:
            return False, f"Authorization error: {str(e)}"
    
    def is_authorized(self, user_id):
        """Check if user is authorized"""
        return str(user_id) in self.authorized_users
    
    def get_access_token(self, user_id):
        """Get stored access token for user"""
        user_data = self.authorized_users.get(str(user_id))
        return user_data['access_token'] if user_data else None
    
    async def send_dm_via_api(self, user_id, message):
        """Send DM using Discord API with access token (bypasses mutual guild restriction)"""
        access_token = self.get_access_token(user_id)
        if not access_token:
            return False, "User not authorized"
        
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            async with aiohttp.ClientSession() as session:
                # Create DM channel
                async with session.post('https://discord.com/api/users/@me/channels',
                                       headers=headers,
                                       json={'recipient_id': str(user_id)}) as resp:
                    channel_data = await resp.json()
                    if 'error' in channel_data:
                        return False, f"Error: {channel_data['message']}"
                    
                    channel_id = channel_data['id']
                
                # Send message to DM channel
                async with session.post(f'https://discord.com/api/channels/{channel_id}/messages',
                                       headers=headers,
                                       json={'content': message}) as resp:
                    if resp.status == 200:
                        return True, "DM sent successfully"
                    else:
                        error = await resp.json()
                        return False, f"Error: {error.get('message')}"
        
        except Exception as e:
            return False, f"API Error: {str(e)}"

oauth_manager = OAuth2Manager()

# OAuth2 Callback Handler (for web server)
async def handle_oauth_callback(request):
    """Handle OAuth2 callback from Discord"""
    code = request.rel_url.query.get('code')
    
    if not code:
        return web.Response(text="❌ No authorization code received", status=400)
    
    success, message = await oauth_manager.authorize_user(code)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord Bot Authorization</title>
        <style>
            body {{ font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #36393f; }}
            .container {{ text-align: center; background: #2f3136; padding: 40px; border-radius: 10px; color: white; }}
            .success {{ color: #43b581; }}
            .error {{ color: #f04747; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="{'success' if success else 'error'}">{'✅ Authorization Successful!' if success else '❌ Authorization Failed'}</h1>
            <p>{message}</p>
            <p>You can now close this window.</p>
        </div>
    </body>
    </html>
    """
    
    return web.Response(text=html, content_type='text/html')

async def start_oauth_server(port=8080):
    """Start OAuth2 callback server"""
    app = web.Application()
    app.router.add_get('/callback', handle_oauth_callback)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', port)
    await site.start()
    print(f"[OAuth2] Callback server running on http://localhost:{port}/callback")
    return runner
