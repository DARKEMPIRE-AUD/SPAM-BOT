# 🚀 Quick Start Guide - OAuth2 Bot

## What Was Fixed?
❌ **Before:** Error 50278 - "Cannot send messages to this user due to having no mutual guilds"
✅ **After:** Users authorize via OAuth2 → Bot can DM them anytime!

## Quick Setup (5 minutes)

### Step 1: Discord Developer Portal
1. Go to https://discord.com/developers/applications
2. Create New Application → Name it
3. Go to OAuth2 tab
4. Copy `CLIENT ID` and `CLIENT SECRET`
5. Add Redirect: `http://localhost:8080/callback`

### Step 2: Update `.env`
Create/Update file: `..\.env` (parent directory)
```
BOT_TOKEN=your_bot_token
BOT_CLIENT_ID=your_client_id_from_discord
BOT_CLIENT_SECRET=your_client_secret_from_discord
OAUTH_REDIRECT_URI=http://localhost:8080/callback
```

### Step 3: Run Bot
```bash
cd bot_1
python bot_1.py
```

You should see:
```
=== BOT IS ONLINE ===
[OAuth2] Callback server running on http://localhost:8080/callback
```

## Usage

### Get Authorization Link
```
!auth-link
```
Copy the link → Send to users you want to DM

### Send DMs to Authorized Users
```
!spam <user_id> <message> <times>
```

Example:
```
!spam 1434471542187884565 "Hello World" 5
```

### View All Authorized Users
```
!auth-list
```

## File Structure
```
d:\spam bot\bot_1\
├── bot_1.py                    ← Main bot
├── oauth2.py                   ← OAuth2 manager (NEW)
├── requirements.txt            ← Dependencies
├── OAUTH2_SETUP.md            ← Full setup guide
├── README.md                   ← Updated docs
├── .env.example               ← Environment template
└── authorized_users.json      ← Auto-created after first auth
```

## What Happens When User Clicks Auth Link?

1. Discord asks user to authorize bot
2. User clicks "Authorize"
3. Redirected to: `http://localhost:8080/callback?code=...`
4. Bot exchanges code for access token
5. Token stored in `authorized_users.json`
6. Success page shows ✅

Now bot can send them DMs without mutual guild requirement!

## Commands Summary

| Command | What It Does |
|---------|-------------|
| `!auth-link` | Generate OAuth2 authorization link to share |
| `!auth-list` | Show all authorized users (owner only) |
| `!spam <id> <msg> <times>` | Send DMs to authorized users |
| `!spam` (in DM) | Personal spam in your DM with bot |
| `!stspam <text>` | Start continuous spam |
| `!spspam` | Stop spam |

## Troubleshooting

### Port 8080 Already in Use
```python
# In bot_1.py, change line:
await start_oauth_server(port=8081)  # Use 8081 instead
```

### "User not authorized" Error
→ User hasn't authorized yet
→ Send them the link from `!auth-link`

### Bot doesn't start
→ Check `.env` variables are correct
→ Check BOT_TOKEN is valid
→ Check you have all dependencies: `pip install -r requirements.txt`

## Security Notes
⚠️ Never share `BOT_CLIENT_SECRET`
⚠️ Add `.env` to `.gitignore`
⚠️ Keep `authorized_users.json` secure (has access tokens)

## Next Steps
- Read [OAUTH2_SETUP.md](OAUTH2_SETUP.md) for detailed setup
- Read [README.md](README.md) for full documentation
- Test with `!auth-link` command

That's it! 🎉 No more 403 errors!
