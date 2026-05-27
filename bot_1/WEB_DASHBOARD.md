# 🔥 Web Dashboard - Spam Dashboard Guide

## What is This?

**Professional Web Dashboard** to send unlimited Discord DMs without Discord commands!

```
Browser Dashboard 
    ↓
Flask Web Server (http://localhost:5000)
    ↓
Discord Bot (via Discord.py)
    ↓
User's DM ✅
```

---

## Features

✅ **Send DMs to ANY user, anytime**  
✅ **No Discord commands needed**  
✅ **Unlimited spam capability** (1-1000 messages)  
✅ **Live counter** - Track messages sent  
✅ **Spam history** - See all sent messages  
✅ **Authorized users list** - Quick click to DM  
✅ **Beautiful UI** - Modern dark dashboard  
✅ **Mobile responsive** - Works on phone too  

---

## Setup

### Step 1: Install Dependencies

```bash
cd d:\spam bot\bot_1
pip install -r requirements.txt
```

### Step 2: Start Bot

```bash
python bot_1.py
```

**Expected Output:**
```
=== BOT IS ONLINE ===
Logged on as: KICK ASS CORP
[OAuth2] Callback server running on http://localhost:8080/callback
[Web Dashboard] Started on http://localhost:5000
```

### Step 3: Open Dashboard

Open in browser:
```
http://localhost:5000
```

---

## How to Use

### 1️⃣ **Send Spam**

1. Open dashboard
2. Enter **User ID** (e.g., 1434471542187884565)
3. Enter **Message** to spam
4. Set **Times** (1-1000)
5. Click **🚀 SEND SPAM**

Done! Message sent! ✅

### 2️⃣ **View History**

Click **📊 History** tab to see:
- When message was sent
- Target user
- Message content
- Number of times
- Success/Error status

### 3️⃣ **Quick Select Users**

Click **👥 Authorized Users** tab to see all OAuth2-authorized users. Click on any user to auto-fill their ID!

---

## Features Explained

### 💬 Send Spam Tab
- **User ID**: Discord user's unique ID
- **Message**: What to send (no limits!)
- **Times**: How many times to send (1-1000)
- **Send**: One-click sending!

### 📊 History Tab
- Last 20 spam actions
- Timestamps, user IDs, messages, counts
- Success/failure status
- Helps track what was sent

### 👥 Authorized Users Tab
- All users who authorized via OAuth2
- Click to auto-fill user ID
- Shows authorization time
- Live count of authorized users

### 📈 Stats Dashboard
- **Messages Sent**: Total DMs delivered
- **Total Spam Count**: Sum of all spam counts
- **Authorized Users**: Users who authorized

---

## How Spam Works

### If User is Authorized (OAuth2):
✅ Uses stored access token  
✅ Can DM anytime  
✅ No mutual guild needed  

### If User NOT Authorized:
❌ Needs mutual server with bot  
❌ Shows error if not possible  

---

## Examples

### Example 1: Send 5 messages
```
User ID: 1434471542187884565
Message: SPAM TEST
Times: 5
```
Result: 5 identical messages sent!

### Example 2: Send 100 messages
```
User ID: 1434471542187884565
Message: HELO
Times: 100
```
Result: 100 DMs (with 0.5s delay between each)

### Example 3: Long message
```
User ID: 1434471542187884565
Message: This is a very long message that can have emojis 🔥🚀
Times: 10
```
Result: Message sent 10 times!

---

## Finding User ID

### Method 1: Developer Mode
1. Enable Developer Mode in Discord (User Settings → Advanced)
2. Right-click user → Copy User ID
3. Paste in dashboard!

### Method 2: Using Dashboard
1. Go to **👥 Authorized Users** tab
2. Click on user
3. Auto-filled! Ready to send!

---

## Stats Tracking

Dashboard tracks:
- ✅ Total messages sent
- ✅ Spam history (last 100 entries)
- ✅ Authorized users count
- ✅ Timestamps

All saved in `spam_stats.json` file!

---

## Troubleshooting

### "User not found"
❌ Invalid user ID  
✅ Check user ID is correct

### "Cannot send message"
❌ User blocked bot or DMs closed  
✅ User must have DMs enabled

### "No mutual guild"
❌ User not in any server with bot  
✅ Authorize user via OAuth2 first

### Dashboard won't load
❌ Port 5000 in use  
✅ Try different port in bot startup

### Bot won't start
❌ Dependencies missing  
✅ Run: `pip install -r requirements.txt`

---

## Ports

- **5000**: Web Dashboard (http://localhost:5000)
- **8080**: OAuth2 Callback (http://localhost:8080/callback)
- **Discord**: Bot token (via Discord API)

---

## API Endpoints

If you want to use programmatically:

```bash
# Send spam
POST http://localhost:5000/api/spam
{
  "user_id": "1434471542187884565",
  "message": "SPAM",
  "times": 5
}

# Get stats
GET http://localhost:5000/api/stats

# Get history
GET http://localhost:5000/api/history

# Get authorized users
GET http://localhost:5000/api/authorized-users
```

---

## Security Notes

⚠️ **Run locally only!**  
⚠️ **Not for production!**  
⚠️ **Bot tokens can be stolen!**  

---

## Commands Still Work

Discord slash commands still work:
- `!auth-link` - Get OAuth2 link
- `!auth-list` - List authorized users
- `!spam <id> <msg> <times>` - Send via Discord

But dashboard is **MUCH EASIER!** 🚀

---

## Support

**Dashboard Features:**
- ✅ Unlimited spam
- ✅ No authorization needed (for mutual guilds)
- ✅ Beautiful UI
- ✅ Mobile friendly
- ✅ Live stats
- ✅ History tracking

**Ready to spam?** 🔥
