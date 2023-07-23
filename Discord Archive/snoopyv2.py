import discord

# Discord bot token
TOKEN = 'YOUR DISCORD BOT TOKEN HERE'

# File path for saving the channel information
FILE_PATH = 'PATH TO WHERE YOU WANT .txt FILE SAVED'

# Define the intents for the bot
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.guild_messages = True
intents.dm_messages = True

# Initialize the Discord client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    print('------')

    # Open the file in append mode with UTF-8 encoding
    with open(FILE_PATH, 'a', encoding='utf-8') as file:
        file.write('Channel Log\n')
        file.write('-----------\n')

        # Iterate through each guild (server)
        for guild in client.guilds:
            file.write(f'Guild: {guild.name}\n')
            file.write(f'Number of Channels: {len(guild.channels)}\n')
            file.write('\n' * 4)

            # Iterate through each channel in the guild
            for channel in guild.channels:
                file.write('\n'*15+f'Channel Name: {channel.name}\n')
                file.write(f'Channel ID: {channel.id}\n\n'+'----------'*10)

                # Check if the channel is a text channel
                if isinstance(channel, discord.TextChannel):
                    file.write('\n')  # Add an empty line before messages
                    file.write('Messages:\n')

                    # Fetch and log messages from the channel
                    async for message in channel.history(limit=None):
                        file.write(f'Time: {message.created_at}\n')
                        file.write(f'Author: {message.author}\n')
                        file.write(f'Content: {message.content}\n')
                        file.write('\n')  # Add an empty line between messages

                file.write('----------'*10)
            file.write('\n' * 4)

    print('Channel log saved successfully.')

# Start the bot
client.run(TOKEN)
