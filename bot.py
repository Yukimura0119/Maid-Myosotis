import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='[')

@bot.event
async def on_ready():
    print(">> Bot is online <<")

bot.run("NzU5NjczMDIwNjgyOTkzNjY1.X3A6og.5fOU6WTY9q0NLXo9vS_cgFLS7sU")

