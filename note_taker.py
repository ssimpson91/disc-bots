import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# In-memory storage for notes
notes = []

@bot.command(name='note', help='Jots down a note with a category. Format: !note [Category] [Content]')
async def add_note(ctx, category: str, *, content: str):
    # Create and store the note
    note = {'category': category.lower(), 'content': content}
    notes.append(note)
    await ctx.send(f"Note added in category '{category}': {content}")

@bot.command(name='getnotes', help='Retrieves notes by category. Format: !getnotes [Category]')
async def get_notes(ctx, category: str):
    # Filter notes by category
    category = category.lower()
    filtered_notes = [note for note in notes if note['category'] == category]
    
    if not filtered_notes:
        await ctx.send(f"No notes found in category '{category}'.")
        return
    
    # Format and send the list of notes
    notes_content = '\n'.join([note['content'] for note in filtered_notes])
    await ctx.send(f"Notes in category '{category}':\n{notes_content}")

TOKEN = 'MTIwNjEyMTg3MjYyNjk1MDIwNw.GieqZt.wanhwFIwzVh02XQOX4w2N4SqeSpvxpF6cKFArs'
bot.run(TOKEN)
