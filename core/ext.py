import discord
from discord.ext import commands


class cog_ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
