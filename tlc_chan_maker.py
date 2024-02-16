from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Your bot's token - Remember to keep it secure and not hard-code it in your script
TOKEN = 'MTIwNDU2NTUxOTg2OTY4MTc0NA.GL4flb.wijZGHk60BW2VoUFymG6ijrZcPJc9JgkeZd0SE'




intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent for handling messages
bot = commands.Bot(command_prefix='!', intents=intents)

# Enhanced structure with additional channels for specific needs
structure = {
    "Project Management 📋": ["asset-tracking 🛠️", "task-assignments 📌", "milestones 🏁"],
    "Art & Design 🎨": ["concept-art 🖌️", "3d-modeling 🖥️", "textures-materials 🧱", "animations 🔄", "ui-design 🖼️"],
    "Development 💻": ["general-programming 👨‍💻", "houdini-procedural 🪄", "unreal-engine-5 🎮", "networking 🌐", "version-control 🔄"],
    "Sound Design 🎵": ["music-composition 🎼", "sound-effects 🔊", "voice-overs 🎙️"],
    "Playtesting & Feedback 🕹️": ["internal-testing 🧪", "community-feedback 💬", "bug-reports 🐞"],
    "Marketing & Release 🚀": ["announcements 📢", "social-media-updates 💡", "press-materials 📰"],
}

@bot.command(name='wipeserver', help='WARNING: This will delete all channels and preserve bot and admin roles.')
@commands.has_permissions(administrator=True)
async def wipe_server(ctx):
    guild = ctx.guild

    # Delete all channels
    for channel in list(guild.channels):
        try:
            await channel.delete()
            print(f'Deleted channel: {channel.name}')
        except Exception as e:
            print(f'Failed to delete channel {channel.name}: {str(e)}')

    # Delete all roles (except @everyone, bot roles, and roles with administrator permission)
    for role in list(guild.roles):
        if role.name != "@everyone" and not role.permissions.administrator:
            # Check if the role is a bot role
            is_bot_role = any(member.bot and role in member.roles for member in guild.members)
            if not is_bot_role:
                try:
                    await role.delete()
                    print(f'Deleted role: {role.name}')
                except Exception as e:
                    print(f'Failed to delete role {role.name}: {str(e)}')
            else:
                print(f'Preserved bot role: {role.name}')
        elif role.permissions.administrator:
            print(f'Preserved admin role: {role.name}')

    await ctx.send("Server wiped. All channels and non-admin/non-bot roles have been deleted.")


# Command to post updates or links to new assets
@bot.command(name='postasset', help='Posts an update with a link to a new asset in the specified channel.')
@commands.has_permissions(manage_messages=True)
async def post_asset(ctx, channel_name: str, asset_link: str, description: str = ''):
    # Find the channel by name
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if channel:
        # Post the asset link and description
        message = f"New Asset Posted: {asset_link}\nDescription: {description}"
        await channel.send(message)
    else:
        await ctx.send(f"Channel '{channel_name}' not found.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
@bot.command(name='updatechannels', help='Updates channel names with emojis.')
@commands.has_permissions(manage_channels=True)
async def update_channels(ctx):
    guild = ctx.guild

    for category_name, channels in structure.items():
        # Find or create category
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            category = await guild.create_category(category_name)

        for channel_name in channels:
            # Check if the channel exists (without considering emojis)
            existing_channel = discord.utils.get(category.channels, name=channel_name.split(' ')[0])
            if existing_channel:
                # Update channel name if it doesn't match the desired name (with emoji)
                if existing_channel.name != channel_name:
                    await existing_channel.edit(name=channel_name)
            else:
                # Create the channel if it doesn't exist
                await guild.create_text_channel(channel_name, category=category)

    await ctx.send("Channel names updated with emojis!")


@bot.command(name='setupserver', help='Sets up the server with predefined categories and channels for game development.')
@commands.has_permissions(manage_channels=True)
async def setup_server(ctx):
    guild = ctx.guild

    for category_name, channels in structure.items():
        # Create category
        category = None
        for existing_category in guild.categories:
            if existing_category.name == category_name:
                category = existing_category
                break
        if not category:
            category = await guild.create_category(category_name)

        for channel_name in channels:
            # Create text channel within the category if it does not already exist
            if not discord.utils.get(guild.channels, name=channel_name):
                await guild.create_text_channel(channel_name, category=category)

    await ctx.send("Server setup enhanced for 'The Last City' development!")

# Error handling for commands
@setup_server.error
async def setup_server_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to manage channels.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

# Run the bot
bot.run(TOKEN)
