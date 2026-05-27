# Bot 1 - Simple Discord Spam Bot

एक simple और easy-to-use Discord bot spam commands के लिए with OAuth2 authorization.

## Features

- **!spam <id> <message> <times>** - किसी user/channel को spam करो (with OAuth2 support)
- **!spam** (DM only) - DM में simple spam करो
- **!stspam <text>** - Continuous spam शुरु करो
- **!spspam** - Spam बंद करो
- **!auth-link** - OAuth2 authorization link generate करो (share with users)
- **!auth-list** - सभी authorized users को देखो (owner only)

## Setup Instructions

### 1. Discord Developer Portal Setup

1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to OAuth2 → General
4. Copy `CLIENT ID` and `CLIENT SECRET`
5. In OAuth2 → URL Generator:
   - Select `identify` and `email` scopes
   - Set Redirect URL: `http://localhost:8080/callback`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configuration

Create/Update `..\.env` file with these settings:

```
BOT_TOKEN=your_discord_bot_token_here
BOT_CLIENT_ID=your_client_id_here
BOT_CLIENT_SECRET=your_client_secret_here
OAUTH_REDIRECT_URI=http://localhost:8080/callback
```

### 4. Authorized Users

Bot_1.py में `AUTHORIZED_USERS` और `OWNER_ID` को अपने Discord ID से update करो:

```python
AUTHORIZED_USERS = [your_id_1, your_id_2]
OWNER_ID = your_id
```

### 5. Run the Bot

```bash
python bot_1.py
```

## How OAuth2 Works

1. **Generate Link**: अपने authorized users से `!auth-link` command से link generate करो
2. **User Authorizes**: Target users को link click करने दो और authorize करने दो
3. **Send DMs**: अब आप उन्हें बिना किसी "mutual guild" requirement के DM कर सकते हो
4. **No 403 Errors**: Discord की 50278 error अब नहीं आएगी!

## Commands

| Command | Usage | Description |
|---------|-------|-------------|
| !spam | `!spam <id> <message> <times>` | User/Channel को spam करो |
| !spam | DM में `!spam` | DM में manual message spam करो |
| !stspam | `!stspam <message>` | Continuous spam शुरु करो |
| !spspam | `!spspam` | Spam बंद करो |
| !auth-link | `!auth-link` | OAuth2 authorization link generate करो (authorized users only) |
| !auth-list | `!auth-list` | सभी authorized users देखो (owner only) |

## Notes

- केवल authorized users ही commands use कर सकते हैं
- DM commands केवल owner के लिए
- Bot को servers में sufficient permissions होने चाहिए
