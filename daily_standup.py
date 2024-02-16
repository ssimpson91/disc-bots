import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# In-memory storage for stand-up logs
standup_logs = []

async def ask_question(channel, user, question):
    """Sends a question to the user and waits for their response."""
    await channel.send(question)  # Send question to the appropriate channel
    def check(m):
        # Check that the response is from the same user and in the correct channel
        return m.author == user and m.channel == channel
    message = await bot.wait_for('message', check=check)
    return message.content

@bot.command(name='dailystandup', help='Starts a daily stand-up process.')
async def daily_standup(ctx):
    user = ctx.author
    channel = ctx.message.channel  # Use the channel where the command was issued
    start_time = datetime.datetime.now()  # Capture the start time of the stand-up

    yesterday = await ask_question(channel, user, "What did you work on yesterday?")
    today = await ask_question(channel, user, "What are you planning to work on today?")
    blockers = await ask_question(channel, user, "Are there any blockers?")
    
    # Log the stand-up with date and time stamps
    standup_log = {
        'user': user.name,
        'channel': channel.id if isinstance(channel, discord.TextChannel) else 'DM',
        'date': start_time.strftime('%Y-%m-%d'),
        'time': start_time.strftime('%H:%M:%S'),
        'yesterday': yesterday,
        'today': today,
        'blockers': blockers
    }
    standup_logs.append(standup_log)
    
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await channel.send(f"Thank you for your update! Logged on {current_time}")

TOKEN = 'MTIwNjExNjk1NzM1OTcxMDIzMA.GXaCOR.QHQ3ms285b5aonbRR0d6i1mNTiz040jE1tnPxo'
bot.run(TOKEN)