import imaplib
import email
import discord
import asyncio
from discord.ext import commands

# Email account details
email_account = "YOUR EMAIL"
email_password = "YOUR GOOGLE APP PASSWORD"
imap_server = "imap.gmail.com"
imap_port = 993
sender_email = "EMAIL YOU WANT CONTENT EXTRACTED"

# Discord bot details
discord_token = "DISCORD TOKEN GOES HERE"
discord_channel_id = channel id goes here

# Set up the Discord bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    await check_emails()

async def check_emails():
    seen_messages = set()

    while True:
        # Connect to the IMAP server
        try:
            mail = imaplib.IMAP4_SSL(imap_server, imap_port)
            mail.login(email_account, email_password)
            mail.select("inbox")
        except imaplib.IMAP4.error as e:
            print(f'Error connecting to the IMAP server: {e}')
            await asyncio.sleep(5)
            continue

        # Search for unseen emails from the specified sender
        result, data = mail.search(None, f'(UNSEEN FROM "{sender_email}")')
        if result != 'OK':
            print(f'Error searching for emails: {result}')
            mail.logout()
            await asyncio.sleep(5)
            continue

        # Process each unseen email found
        for num in data[0].split():
            if num in seen_messages:
                continue

            result, data = mail.fetch(num, "(RFC822)")
            if result != 'OK':
                print(f'Error fetching email: {result}')
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Get the email content
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode()
                        break
            else:
                content = msg.get_payload(decode=True).decode()

            # Post the email content to Discord
            channel = bot.get_channel(discord_channel_id)
            if channel:
                await channel.send(content)

            seen_messages.add(num)

        mail.logout()
        await asyncio.sleep(30)# Checkevery 30 seconds or whatever

bot.run(discord_token)
