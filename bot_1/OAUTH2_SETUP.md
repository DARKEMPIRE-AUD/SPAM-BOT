# OAuth2 Setup Guide for Discord Bot

This bot uses **OAuth2 authorization** to send direct messages to users without needing mutual guilds.

## Why OAuth2?

Discord blocks DMs to users who don't share a server with your bot (Error 50278). OAuth2 bypasses this by:
- Having users explicitly authorize the bot
- Getting an access token to send DMs directly via Discord API
- No more "mutual guild" restrictions!

## Step-by-Step Setup

### 1. Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name it (e.g., "KICKASS CORP") and click Create
4. Go to the "OAuth2" tab on the left

### 2. Get CLIENT_ID and CLIENT_SECRET

1. Under "OAuth2 → General":
   - Copy your `CLIENT ID` 
   - Copy your `CLIENT SECRET` (keep this secret!)
   - Click "Reset Secret" if needed

### 3. Set Redirect URI

1. Under "OAuth2 → General":
2. Click "Add Redirect"
3. Enter: `http://localhost:8080/callback`
4. Click Save

### 4. Update `.env` file

Copy `.env.example` to `..\.env` in the parent directory:

```
BOT_TOKEN=your_bot_token_here
BOT_CLIENT_ID=copy_from_discord_portal
BOT_CLIENT_SECRET=copy_from_discord_portal
OAUTH_REDIRECT_URI=http://localhost:8080/callback
```

### 5. Run the Bot

```bash
python bot_1.py
```

The bot will start an OAuth2 callback server on `http://localhost:8080`

## How to Use OAuth2

### For Bot Owner/Admins:

1. **Get the Authorization Link**
   ```
   !auth-link
   ```
   This generates a link like:
   ```
   https://discord.com/api/oauth2/authorize?client_id=...&redirect_uri=...&response_type=code&scope=identify%20email
   ```

2. **Share the Link**
   - Send the link to any user you want to authorize
   - They click the link and authorize the bot
   - They get redirected to a success page

3. **Send DMs**
   - Now you can DM them with: `!spam <user_id> <message> <times>`
   - No more 403 errors!

### For End Users:

1. Click the authorization link
2. Click "Authorize" on Discord's permission page
3. You'll see a success message
4. Now the bot can send you DMs anytime

### For Owner to Check Authorized Users:

```
!auth-list
```

Shows all users who have authorized the bot with timestamps.

## Troubleshooting

### "OAUTH2_UNAUTHORIZED" error
- Check that your CLIENT_ID and CLIENT_SECRET are correct
- Make sure you have internet connection

### Callback server not starting
- Port 8080 might be in use
- Try closing other applications using port 8080
- Or modify the port in `bot_1.py`: `await start_oauth_server(port=8081)`

### Users can't authorize
- Make sure the redirect URI exactly matches: `http://localhost:8080/callback`
- Check Discord Developer Portal settings

### "User not authorized" message
- The target user hasn't gone through the authorization process yet
- Send them the `!auth-link` first

## File Structure

```
bot_1/
├── bot_1.py              # Main bot file (updated with OAuth2)
├── oauth2.py             # OAuth2 manager (NEW)
├── requirements.txt      # Dependencies (updated)
├── .env.example          # Environment variables template (NEW)
└── README.md             # Documentation (updated)
```

## Advanced: Testing OAuth2 Locally

If you want to test with a different redirect URI:

1. In Discord Developer Portal, add multiple redirect URIs:
   - `http://localhost:8080/callback`
   - `http://your-server-ip:8080/callback`
   - `http://your-domain.com/callback` (for production)

2. Update `.env`:
   ```
   OAUTH_REDIRECT_URI=http://your-server-ip:8080/callback
   ```

3. Restart the bot

## Security Notes

⚠️ **Important:**
- Never share your `BOT_CLIENT_SECRET` 
- Never push `.env` to Git/GitHub
- Add `.env` to `.gitignore`
- The `authorized_users.json` file stores access tokens - keep it secure

## Security Best Practices

1. **Rotate Secret**: In Discord Developer Portal, click "Reset Secret" periodically
2. **Token Storage**: Access tokens are stored in `authorized_users.json` on disk
3. **HTTPS in Production**: If deploying to internet, use HTTPS for redirect URI
4. **Token Expiry**: Implement token refresh logic for long-term tokens

For more info, see [Discord OAuth2 Documentation](https://discord.com/developers/docs/topics/oauth2)
