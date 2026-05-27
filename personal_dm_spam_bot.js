// Personal DM Spam Bot in Node.js
// Only responds to your user ID in DMs
// Usage: !spam in DM, then reply with the message to spam

const { Client, GatewayIntentBits, Partials, Events } = require('discord.js');
require('dotenv').config();

const OWNER_ID = '1434471542187884565'; // Your Discord user ID
const TOKEN = process.env.BOT_TOKEN || 'YOUR_BOT_TOKEN_HERE';

const client = new Client({
    intents: [
        GatewayIntentBits.DirectMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages
    ],
    partials: [Partials.Channel]
});

const awaitingAuthorization = new Set();
const awaitingSpamMessage = new Set();

client.once(Events.ClientReady, () => {
    console.log(`Logged in as ${client.user.tag}`);
});

client.on(Events.MessageCreate, async (message) => {
    // Only respond in DMs
    if (message.guild) return;
    if (message.author.bot) return;

    // Anyone can use the command in DMs

    // If waiting for authorization
    if (awaitingAuthorization.has(message.author.id)) {
        awaitingAuthorization.delete(message.author.id);
        if (message.content.trim().toLowerCase() === 'yes') {
            awaitingSpamMessage.add(message.author.id);
            await message.channel.send('What message do you want to spam?');
        } else {
            await message.channel.send('Spam action cancelled.');
        }
        return;
    }

    // If waiting for spam message
    if (awaitingSpamMessage.has(message.author.id)) {
        awaitingSpamMessage.delete(message.author.id);
        const spamMsg = message.content;
        await message.channel.send(`Spamming this message 10 times:\n${spamMsg}`);
        for (let i = 0; i < 10; i++) {
            await message.channel.send(spamMsg);
        }
        return;
    }

    // !spam command
    if (message.content.trim() === '!spam') {
        awaitingAuthorization.add(message.author.id);
        await message.channel.send('Do you authorize this action? (yes/no)');
        return;
    }
});

client.login(TOKEN);
