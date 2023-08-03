import discord
import random

# List of black card entries
black_cards = []

# Read entries from blackcards.txt file
with open("blackcards.txt", "r") as file:
    entries = file.read().split(".")

# Remove leading/trailing whitespace from entries
black_cards = [entry.strip() for entry in entries]

# List of white card entries
# Read entries from whitecards.txt file
with open("whitecards.txt", "r") as file:
    entries = file.read().split(",")

# Remove leading/trailing whitespace from entries
entries = [entry.strip() for entry in entries]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Dictionary to store the black and white cards for each player
player_cards = {}
current_black_card = ""

# List to store the white card submissions from players
white_card_submissions = []


# Function to generate a random white card
def generate_white_card():
    return random.choice(entries)


# Function to generate a random black card
def generate_black_card():
    return random.choice(black_cards)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')


@client.event
async def on_message(message):
    global current_black_card  # Declare current_black_card as a global variable

    if message.author == client.user:
        return

    if message.content == "!help":
        await message.channel.send(
            "**Here's how to play!**\n\n```CARDS AGAINST HUMANITY\n\nInstructions:\n1 - Start playing by typing: !play\n\n2 - After you start, you will be DM'd 6 'White Cards.'\n\n3 - Draw a 'Black Card' by typing: !b\n\n4 - Add your White Card to the Black Card by choosing the number corresponding with your White Card and typing: !c #, for example, !c 2\n\n5 - The used White Card will be deleted from your deck and a new one will be added.\n\n6 - Repeat steps 3-4 and have fun!\n\nType '!quit' at anytime to stop playing or restart.\n\nCommands:\n!play - start game or join game.\n!b - draw black card.\n!c # - add your card to the black card [eg !c 2].\n!quit - quit game.```")  # Display help message
        return

    if message.content.startswith('!p') or message.content.startswith('!s') or message.content.startswith(
            '!play') or message.content.startswith('!start'):
        if str(message.author.id) in player_cards:
            await message.channel.send('**You\'re already playing!**')
            return
        await message.channel.send(
            "**New Player Joined**!\nWhite Cards have been sent to your DMs!\n```Instructions:\n\n1 - Draw a 'Black Card' by typing: !b\n\n2 - Add your White Card to the Black Card by choosing the number corresponding with your White Card and typing: !c #, for example, !c 2\n\n3 - The used White Card will be deleted from your deck and a new one will be added.\n\n4 - Repeat steps 1-2 and have fun!\n\nType '!quit' at anytime to stop playing or restart.```")
        player_cards[str(message.author.id)] = []

        # Deal white cards
        for i in range(1, 7):
            white_card = generate_white_card()
            await message.author.send(f'{i} - White Card: {white_card}')
            player_cards[str(message.author.id)].append(white_card)

    elif message.content.startswith('!quit'):
        if str(message.author.id) not in player_cards:
            await message.channel.send('You are not part of the game.')
            return
        del player_cards[str(message.author.id)]
        await message.channel.send('You have quit the game.')

    elif message.content.startswith('!bc') or message.content.startswith('!b') or message.content.startswith(
            '!black') or message.content.startswith('!blackcard'):
        current_black_card = generate_black_card()
        await message.channel.send(f'Black Card: **{current_black_card}**')
        await message.channel.send('```waiting all players White Card submissions...```')

    elif message.content.startswith('!c') or message.content.startswith('!wc') or message.content.startswith('!card') or message.content.startswith(
            '!white') or message.content.startswith('!whitecard'):
        player_id = str(message.author.id)
        if player_id not in player_cards:
            await message.channel.send('You are not part of the game.')
            return

        # Get the specified white card number
        try:
            card_number = int(message.content.split(' ')[1])
        except (ValueError, IndexError):
            await message.channel.send('Invalid command format. Please use !c # (e.g., !c 2).')
            return

        # Check if the card number is within the player's card range
        if card_number < 1 or card_number > len(player_cards[player_id]):
            await message.channel.send('Invalid card number.')
            return

        # Get the chosen white card
        white_card = player_cards[player_id][card_number - 1]

        # Add the white card submission to the list
        white_card_submissions.append(white_card)

        # Generate a new white card with the same number
        new_white_card = generate_white_card()
        player_cards[player_id][card_number - 1] = new_white_card
        await message.author.send(f'{card_number} - White Card: {new_white_card}')

        # Delete the white card message from the user's DMs
        async for dm_message in message.author.dm_channel.history():
            if dm_message.content == f'{card_number} - White Card: {white_card}':
                await dm_message.delete()

        # Check if all players have submitted their white cards
        if len(white_card_submissions) == len(player_cards):
            # Randomize the order of white card submissions
            random.shuffle(white_card_submissions)

            # Combine the white and black cards to create responses
            responses = []
            for submission in white_card_submissions:
                response = f'Black Card: **{current_black_card}**\nWhite Card: **{submission}**'
                responses.append(response)

            # Send all the responses
            for response in responses:
                await message.channel.send(response)

            # Clear the white card submissions
            white_card_submissions.clear()

    else:
        await message.channel.send()


client.run('YOUR DISCORD BOT TOKEN')
