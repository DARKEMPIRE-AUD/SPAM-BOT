from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import discord
import asyncio
import json
import os
from datetime import datetime
from oauth2 import oauth_manager

app = Flask(__name__)
CORS(app)

# Global stats
SPAM_STATS = {
    'total_sent': 0,
    'total_spam_messages': 0,
    'history': []
}

STATS_FILE = 'spam_stats.json'

def load_stats():
    global SPAM_STATS
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            SPAM_STATS = json.load(f)

def save_stats():
    with open(STATS_FILE, 'w') as f:
        json.dump(SPAM_STATS, f, indent=2)

def add_to_history(user_id, message, count, status):
    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': str(user_id),
        'message': message,
        'count': count,
        'status': status
    }
    SPAM_STATS['history'].append(entry)
    if len(SPAM_STATS['history']) > 100:  # Keep last 100 entries
        SPAM_STATS['history'] = SPAM_STATS['history'][-100:]
    save_stats()

# Discord client reference (will be set from main bot)
discord_client = None
bot_loop = None

def set_discord_client(client):
    global discord_client, bot_loop
    discord_client = client
    bot_loop = client.loop

async def send_spam_async(user_id, message, times):
    """Send spam messages to a user"""
    try:
        user = await discord_client.fetch_user(user_id)
        sent_count = 0
        
        for i in range(times):
            try:
                await user.send(message)
                sent_count += 1
                await asyncio.sleep(0.5)  # Rate limit
            except discord.Forbidden as e:
                # If forbidden, return error (no OAuth2 fallback)
                return sent_count, f"Forbidden: {str(e)}"
            except Exception as e:
                return sent_count, f"Error: {str(e)}"
        
        return sent_count, "Success"
    except discord.NotFound:
        return 0, "User not found"
    except Exception as e:
        return 0, f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/spam', methods=['POST'])
def spam():
    """API endpoint to send spam"""
    try:
        data = request.json
        user_id = int(data.get('user_id'))
        message = data.get('message', '')
        times = int(data.get('times', 1))
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        if times < 1 or times > 1000:
            return jsonify({'error': 'Times must be between 1 and 1000'}), 400
        
        # Schedule async function on bot's event loop from Flask thread
        if bot_loop is None:
            return jsonify({'error': 'Bot not initialized'}), 500
        
        try:
            future = asyncio.run_coroutine_threadsafe(send_spam_async(user_id, message, times), bot_loop)
            sent_count, status = future.result(timeout=30)  # Wait up to 30 seconds
        except Exception as e:
            add_to_history(user_id, message, times, f"Error: {str(e)}")
            return jsonify({'error': str(e), 'sent': 0, 'requested': times, 'status': f'Error: {str(e)}'}), 500
        
        # Update stats
        SPAM_STATS['total_sent'] += sent_count
        SPAM_STATS['total_spam_messages'] += times
        add_to_history(user_id, message, times, status)
        
        return jsonify({
            'success': True,
            'sent': sent_count,
            'requested': times,
            'status': status,
            'total_sent': SPAM_STATS['total_sent']
        })
    
    except ValueError as e:
        return jsonify({'error': f'Invalid user ID or times: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/stats')
def get_stats():
    """Get spam statistics"""
    return jsonify({
        'total_sent': SPAM_STATS['total_sent'],
        'total_messages': SPAM_STATS['total_spam_messages'],
        'history': SPAM_STATS['history'][-20:]  # Last 20 entries
    })

@app.route('/api/history')
def get_history():
    """Get full spam history"""
    return jsonify({
        'history': SPAM_STATS['history']
    })

@app.route('/api/authorized-users')
def get_authorized_users():
    """Get list of authorized users"""
    users = []
    for user_id, data in oauth_manager.authorized_users.items():
        users.append({
            'user_id': user_id,
            'username': data.get('username', 'Unknown'),
            'authorized_at': data.get('authorized_at', 'Unknown')
        })
    return jsonify({'users': users})

def start_web_server(port=5000):
    """Start Flask web server"""
    load_stats()
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

if __name__ == '__main__':
    load_stats()
    app.run(host='0.0.0.0', port=5000, debug=False)
