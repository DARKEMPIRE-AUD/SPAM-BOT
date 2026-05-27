import asyncio
import discord
import os
import threading
from dotenv import load_dotenv
from oauth2 import oauth_manager, start_oauth_server
from web_dashboard import app, set_discord_client, start_web_server

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Configuration
AUTHORIZED_USERS = [
    1380891453416407050,
    1434471542187884565,
    670256947450216495,
    1414061950505189407,
    1433444652878397556,
    1448760037689528450,
    1415064343204204776,
    1455887248481321013,
    1201748943118270494
]
OWNER_ID = 1434471542187884565


class Client(discord.Client):

    async def on_ready(self):
        print(f"=== BOT IS ONLINE ===")
        print(f"Logged on as: {self.user}")
        print(f"=====================")
        self.is_spamming = False
        self.spam_text = ""
        
        # Start OAuth2 callback server
        try:
            self.oauth_runner = await start_oauth_server(port=8888)
            print("[OAuth2] Server started successfully")
        except Exception as e:
            print(f"[OAuth2] Failed to start server: {e}")        
        # Set Discord client for web dashboard
        set_discord_client(self)
        
        # Start web dashboard in background thread
        if not hasattr(self, 'web_thread'):
            self.web_thread = threading.Thread(target=lambda: start_web_server(5000), daemon=True)
            self.web_thread.start()
            print("[Web Dashboard] Started on http://localhost:5000")
    async def on_message(self, message):
        # Ignore the bot's own messages
        if message.author == self.user:
            return

        # --- AUTHORIZED USERS FOR SPAM COMMAND (Two users allowed) ---
        authorized_users = AUTHORIZED_USERS

        # --- DM ONLY: !spam command for personal use ---
        if isinstance(message.channel, discord.DMChannel):
            if message.content.strip() == "!spam":
                # Only allow authorized users
                if message.author.id != OWNER_ID:
                    await message.channel.send("You are not authorized to use this command.")
                    return
                await message.channel.send("What message do you want to spam?")

                def check(m):
                    return m.author == message.author and m.channel == message.channel

                try:
                    reply = await self.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await message.channel.send("Timed out waiting for your message.")
                    return

                spam_msg = reply.content
                await message.channel.send(f"Spamming this message 10 times:\n{spam_msg}")
                for _ in range(10):
                    await message.channel.send(spam_msg)
                    await asyncio.sleep(1)
                return

        # --- !spam <id> <msg> <times> ---
        if message.content.startswith("!spam "):
            if message.author.id not in authorized_users:
                await message.channel.send("You are not authorized to use this command.")
                return
            try:
                parts = message.content.split()
                if len(parts) < 4:
                    raise ValueError
                target_id = int(parts[1])
                times = int(parts[-1])
                msg = " ".join(parts[2:-1])
                msg = f"**{msg}**"  # Make message bold
            except Exception:
                await message.channel.send("Usage: !spam <id> <message> <times>")
                return

            # Try to get channel first
            target = self.get_channel(target_id)
            if target:
                for _ in range(times):
                    try:
                        await target.send(msg)
                        await asyncio.sleep(1)  # Channel spam: keep delay
                    except Exception as e:
                        await message.channel.send(f"Error: {e}")
                        break
                return

            # Try to DM user (no OAuth2 requirement)
            try:
                user = await self.fetch_user(target_id)
                
                # Try to send DMs directly
                for _ in range(times):
                    try:
                        await user.send(msg)
                        await asyncio.sleep(0.5)
                    except discord.Forbidden as e:
                        await message.channel.send(f"❌ Cannot DM user: {str(e)}")
                        break
                    except Exception as e:
                        await message.channel.send(f"Error: {str(e)}")
                        break
                return
                
            except discord.NotFound:
                await message.channel.send("Invalid user/channel ID.")
                return
            except Exception as e:
                await message.channel.send(f"Error: {e}")
                return

        # 1. Stop Command
        if message.content.strip() == "!spspam":
            self.is_spamming = False
            print("[INFO] Spammer stopped via command.")
            return

        # OAuth2 Commands
        if message.content.strip() == "!auth-link":
            if message.author.id not in AUTHORIZED_USERS:
                await message.channel.send("You are not authorized to use this command.")
                return
            auth_url = oauth_manager.get_authorization_url()
            await message.channel.send(
                f"🔐 **OAuth2 Authorization Link**\n\n"
                f"Share this link with users who want to authorize this bot:\n\n"
                f"{auth_url}\n\n"
                f"After they authorize, you can DM them without any restrictions!"
            )
            return
        
        if message.content.strip() == "!auth-list":
            if message.author.id != OWNER_ID:
                await message.channel.send("Only owner can use this command.")
                return
            
            if not oauth_manager.authorized_users:
                await message.channel.send("No authorized users yet.")
                return
            
            user_list = "**Authorized Users:**\n"
            for user_id, data in oauth_manager.authorized_users.items():
                user_list += f"• {data['username']} ({user_id}) - {data['authorized_at']}\n"
            
            await message.channel.send(user_list)
            return

        # 2. Start Command (Format: !stspam <text>)
        if message.content.startswith("!stspam "):
            # Extract everything after "!stspam "
            self.spam_text = message.content[8:].strip()

            if not self.spam_text:
                return

            self.is_spamming = True
            print(f"[INFO] Started spamming: '{self.spam_text}'")

            # Run the loop
            while self.is_spamming:
                try:
                    await message.channel.send(self.spam_text)
                    # 1-second delay to comply with basic Discord limits
                    await asyncio.sleep(1)
                except discord.Forbidden:
                    print(
                        f"\n[ERROR] The bot cannot type in the channel '#{message.channel.name}'."
                    )
                    print(
                        "-> FIX: The server owner must give your bot the 'Send Messages' permission here.\n"
                    )
                    self.is_spamming = False
                    break
                except Exception as e:
                    print(f"[ERROR] Something went wrong: {e}")
                    self.is_spamming = False
                    break


intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)

# Run the bot with token from .env file
if BOT_TOKEN:
    client.run(BOT_TOKEN)
else:
    print("ERROR: BOT_TOKEN not found in .env file!")

