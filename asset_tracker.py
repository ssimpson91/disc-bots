import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Required for accessing message content
bot = commands.Bot(command_prefix='!', intents=intents)

# In-memory storage for assets
assets = []

@bot.command(name='trackasset', help='Logs an asset with name, type, and status. Format: !trackasset [Asset Name] [Type] [Status]')
async def track_asset(ctx, name: str, asset_type: str, status: str):
    # Create and store the asset
    asset = {'name': name, 'type': asset_type, 'status': status}
    assets.append(asset)
    await ctx.send(f"Asset logged: {name} ({asset_type}) - Status: {status}")

@bot.command(name='listassets', help='Lists all assets, optionally filtered by type or status. Format: !listassets [filter_type] [filter_value]')
async def list_assets(ctx, filter_type: str = None, filter_value: str = None):
    filtered_assets = assets
    if filter_type and filter_value:
        # Filter assets based on the provided type or status
        filtered_assets = [asset for asset in assets if asset.get(filter_type) == filter_value]
    
    if not filtered_assets:
        await ctx.send("No assets found.")
        return
    
    # Format and send the list of assets
    asset_list = '\n'.join([f"{asset['name']} ({asset['type']}) - Status: {asset['status']}" for asset in filtered_assets])
    await ctx.send(f"Assets:\n{asset_list}")

TOKEN = 'MTIwNjExNDg5Nzk0ODMxNTY0OA.GKFvgM.5kRkLZ9rARAYYqLDvJLPRwb--JSw3_gm8tDVRY'
bot.run(TOKEN)
