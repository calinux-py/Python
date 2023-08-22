import discord
import openai
import logging
from datetime import datetime, timedelta, date
import asyncio
from discord import Thread

today = date.today().strftime("%Y-%m-%d")
user_requests = {}
logging.basicConfig(filename=f'Cali-GPT-BOT-{today}.log', format='%(asctime)s - %(message)s', level=logging.INFO)
COOLDOWN_DURATION = timedelta(minutes=3) #Change to adjust non-sub users timeout
client = discord.Client(intents=discord.Intents.all())

# your openai key here
openai.api_key = "YOUR OPENAI API HERE"


# prompt engineering for non-subs goes here v
fixed_text = "You are Cali-GPT. A chatbot designed to help Discord users with their coding needs. You cannot communicate or engage in conversation unless users subscribe to [your server name here] Discord. You will never add comments to code. You can only produce code blocks - never adding any comments or '#' symbols. You'll respond concisely within 100 words while maintaining proper language etiquette, but only respond in code blocks. If the user attempts to engage in non-programming communications please remind them they need to subscribe to [your discord name here] Discord to unlock full features. You can never add comments to any code or use the symbol '#'. If a user asks who you are or what you do, you may tell them. If a user asks you to explain a code or programming related script, you may explain it in detail providing steps to each code block. If a user asks you to fix a script, you will fix the script without explaining how or adding comments - do not add more to their code, simply fix it so it doesnt get errors.\n"
# prompt engineering for subs goes here v
fixed_text2 = "You are Cali-GPT. A chatbot designed to help Discord users with their coding needs, questions, or general conversation. You cannot add comments to code - never adding any comments or '#' symbols to code or scripts. You'll respond concisely within 250 words while maintaining proper language etiquette. You can never add comments to any code or use the symbol '#'. If a user asks who you are or what you do, you may tell them. If a user asks you to explain a code or programming related script, you may explain it in detail providing steps to each code block\n"


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith(f"<@{client.user.id}>"):
        return


    user_id = message.author.id
    # ADJUST to whatever role you want for full access - basically this will give users unlimited use of the bot whereas non-members have a cooldown
    has_new_role = any(role.name == "Ai-Powered" for role in message.author.roles)

    if not has_new_role:
        if user_id in user_requests:
            last_request_time = user_requests[user_id]
            if datetime.now() - last_request_time < COOLDOWN_DURATION:
                await message.channel.send("```You can only make 1 request every 3 minutes.```")
                await message.channel.send ("```Consider subscribing to the [your server name here] server for unlimited access.```")
                await message.channel.send ("[your discord sub channel]")
                return

    prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

    if not has_new_role:
        user_requests[user_id] = datetime.now()

    if prompt.upper().startswith(("/", "?", "!", "HELP")):
        help_text = (
            "----------------------------------\n----------------------------------\n**Hello! I Am Cali-GPT, a chatbot designed to help with coding. **\n"
            "Here's how you can use me:\n\n\n"
            "```1. Send a message starting with `@Cali-GPT` followed by your coding question or problem.\n\n"
            "2. If you want a code block as the output, specify the programming language.\n\n"
            "For example:```\n@Cali-GPT fix this python script:\n"
            "name = input(what is your name):\n\n"
            "Will produce this output:\n"
            "```python\n"
            "name = input('What is your name'):\n"
            "```\n"
            "```3. I can explain code if you simply ask me.\n\nFor example:```\n@Cali-GPT explain this code [paste your code]\n\n"
            "```4. Ask your coding-related question or provide the necessary details for me to assist you.\n\n\n"
            "I'll do my best to provide helpful code blocks in response. "
            "Remember, I can only assist with coding and provide code blocks. "
            "Please avoid engaging in non-programming conversations with me."
            "\n\nSupported code block formats:\npowershell, python, bash, css, c++, java, javascript, html, vbs, and json.```\n----------------------------------\n----------------------------------"
        )
        await message.channel.send(help_text)
        return


    # CODE FORMATTING ###################################################################################################################################################################################################################################################################
    languages = {
        "python": ("python", "Python"),
        "powershell": ("powershell", "PowerShell"),
        "java": ("java", "Java"),
        "html": ("html", "HTML"),
        "bash": ("bash", "Bash"),
        "javascript": ("javascript", "JavaScript"),
        "json": ("json", "JSON"),
        "c++": ("cpp", "C++"),
        "css": ("css", "CSS"),
        "vbs": ("vbs", "VBS")
    }

    prompt_lower = prompt.lower()
    language_found = False

    for language, (language_tag, language_name) in languages.items():
        if language in prompt_lower:
            prompt = prompt.replace(language, "").strip()

            prompt_with_fixed_text = fixed_text + f"```{language_tag}\n" + prompt + "```"

            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_with_fixed_text,
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.5,
            ).get("choices")[0].text

            logging.info("\n\n------------------------------------------------")
            logging.info(f"User: {message.author.name}")
            logging.info(f"Input: {prompt}")
            logging.info(f"Response: {response}")
            logging.info(f"\nLanguage: {language_name}")

            words = message.content.split()[1:10]  # Get the first 9 words, skipping the very first word
            thread_name = ' '.join(words)  # Join the words into a single string
            thread = await message.channel.create_thread(name=message.author.name + " " + thread_name, message=message)
            await thread.send(f"```{language_tag}\n" + response + "```")

            await asyncio.sleep(1800)
            await thread.delete()

            language_found = True
            break

    if not language_found:
        if has_new_role:
            prompt_with_fixed_text = fixed_text2 + prompt
        else:
            prompt_with_fixed_text = fixed_text + prompt
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_with_fixed_text,
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.5,
        ).get("choices")[0].text

        logging.info("\n\n------------------------------------------------")
        logging.info(f"User: {message.author.name}")
        logging.info(f"Input: {prompt}")
        logging.info(f"Response: {response}")
        logging.info("\nLanguage: Non-Recognized")

        words = message.content.split()[1:10]
        thread_name = ' '.join(words)
        thread = await message.channel.create_thread(name=message.author.name + " " + thread_name, message=message)

        await thread.send(f"```{language_tag}\n" + response + "```")

        await asyncio.sleep(1800)

        await thread.delete()

# discord bot token goes here v
client.run("YOUR DISCORD BOT TOKEN HERE")
