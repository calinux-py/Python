from discord import app_commands
import asyncio
import discord
import pytz
from datetime import datetime

intents = discord.Intents.default()
intents.message_content, intents.messages, intents.guilds = True, True, True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def get_pytz_timezone(tz_abbr):
    timezone_map = {
        'EST': 'US/Eastern',
        'EDT': 'US/Eastern',
        'CST': 'US/Central',
        'CDT': 'US/Central',
        'MST': 'US/Mountain',
        'MDT': 'US/Mountain',
        'PST': 'US/Pacific',
        'PDT': 'US/Pacific',
        'UTC': 'UTC'
    }
    return timezone_map.get(tz_abbr, tz_abbr)

class MeetingModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Schedule New Meeting")

        self.date = discord.ui.TextInput(label="Date (MM-DD-YYYY)", style=discord.TextStyle.short, placeholder="12-31-2023")
        self.add_item(self.date)

        # Updated to accept AM/PM
        self.time = discord.ui.TextInput(label="Time (HH:MM AM/PM)", style=discord.TextStyle.short, placeholder="03:00 PM")
        self.add_item(self.time)

        self.timezone = discord.ui.TextInput(label="Timezone", style=discord.TextStyle.short, placeholder="E.g., EST, PST")
        self.add_item(self.timezone)

    async def on_submit(self, interaction: discord.Interaction):
        meeting_date = self.date.value
        meeting_time = self.time.value
        meeting_timezone = self.timezone.value

        pytz_timezone = get_pytz_timezone(meeting_timezone)

        # Adjusted for 12-hour format with AM/PM
        dt_naive = datetime.strptime(f"{meeting_date} {meeting_time}", "%m-%d-%Y %I:%M %p")
        local_tz = pytz.timezone(pytz_timezone)
        dt_local = local_tz.localize(dt_naive)

        # Timezones to display
        timezones = ['US/Pacific', 'US/Eastern']
        timezone_times = []
        for tz in timezones:
            dt_tz = dt_local.astimezone(pytz.timezone(tz))
            formatted_time = dt_tz.strftime('%I:%M %p')  # 12-hour format
            timezone_times.append(f"{tz} - {formatted_time}")

        timezone_str = "\n".join(timezone_times)

        channel_id = 12345678  # Replace with your channel ID
        channel = client.get_channel(channel_id)

        if channel:
            message = await channel.send(f"@everyone\n--------------------------------------\n## Meeting Scheduled\n**{meeting_date}**\n\n{timezone_str}\n--------------------------------------\nReact with '**A**' to Accept. '**M**' for Maybe. '**D**' for Decline.")
            await message.add_reaction("\N{REGIONAL INDICATOR SYMBOL LETTER A}")
            await message.add_reaction("\N{REGIONAL INDICATOR SYMBOL LETTER M}")
            await message.add_reaction("\N{REGIONAL INDICATOR SYMBOL LETTER D}")
            await interaction.response.send_message("Meeting scheduled!", ephemeral=True)
        else:
            await interaction.response.send_message("Failed to find the channel.", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

@tree.command(name="new", description="Schedule a new meeting")
async def new_meeting(interaction: discord.Interaction):
    modal = MeetingModal()
    await interaction.response.send_modal(modal)


client.run("YOUR DISCORD TOKEN")
