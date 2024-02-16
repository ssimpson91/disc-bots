from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)


# Your bot's token
TOKEN = 'MTIwNDU2NTUxOTg2OTY4MTc0NA.GL4flb.wijZGHk60BW2VoUFymG6ijrZcPJc9JgkeZd0SE'

# Categories and channels to create
structure = {
    "Game Development": ["general-discussion", "dev-logs", "design-discussion"],
    "Art": ["concept-art", "3d-modeling", "textures-and-materials", "animations"],
    "Programming": ["general-programming", "game-engine", "networking", "ui-ux"],
    "Sound": ["music", "sound-effects", "voice-acting"],
    "Marketing": ["announcements", "social-media", "press-kit"],
    "Testing": ["bug-reports", "playtesting-feedback"],
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='setupserver', help='Sets up the server with predefined categories and channels for game development.')
@commands.has_permissions(manage_channels=True)
async def setup_server(ctx):
    guild = ctx.guild

    for category_name, channels in structure.items():
        # Create category
        category = await guild.create_category(category_name)
        for channel_name in channels:
            # Create text channel within the category
            await guild.create_text_channel(channel_name, category=category)

    await ctx.send("Server setup complete!")

# Error handling for setup_server command
@setup_server.error
async def setup_server_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to manage channels.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

# Run the bot
bot.run(TOKEN)
