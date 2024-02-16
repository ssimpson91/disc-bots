import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Simple in-memory storage for tasks
tasks = []

@bot.command(name='addtask', help='Adds a new task. Format: !addtask [Category] [Priority] [Description] [Deadline in YYYY-MM-DD]')
async def add_task(ctx, category: str, priority: str, description: str, deadline: str):
    # Convert deadline to a date object
    deadline_date = datetime.datetime.strptime(deadline, '%Y-%m-%d').date()
    task = {
        'category': category,
        'priority': priority,
        'description': description,
        'deadline': deadline_date,
        'created_at': datetime.date.today()
    }
    tasks.append(task)
    await ctx.send(f"Task added: {description} with priority {priority} in category {category}, due by {deadline_date}")

@bot.command(name='listtasks', help='Lists all tasks, optionally filtered by category or priority.')
async def list_tasks(ctx, filter_by: str = None, filter_value: str = None):
    filtered_tasks = tasks
    if filter_by and filter_value:
        if filter_by.lower() in ['category', 'priority']:
            filtered_tasks = [task for task in tasks if task[filter_by].lower() == filter_value.lower()]
        else:
            await ctx.send("Invalid filter. Use 'category' or 'priority'.")
            return
    if not filtered_tasks:
        await ctx.send("No tasks found.")
        return
    for task in filtered_tasks:
        await ctx.send(f"{task['description']} - Priority: {task['priority']}, Category: {task['category']}, Deadline: {task['deadline']}")

TOKEN = 'MTIwNjEwNTE1MzU0ODA1ODcxNA.GITpVx.ILm1taWP6HTgZnCczfUQs-_ImDz9lpAqcdAimk'
#TOKEN = 'MTIwNDU2NTUxOTg2OTY4MTc0NA.GL4flb.wijZGHk60BW2VoUFymG6ijrZcPJc9JgkeZd0SE'

bot.run(TOKEN)
