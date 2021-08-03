import discord
import youtube_dl as ydl
from discord.ext import commands
from core.ext import cog_ext


class Music(cog_ext):
    @commands.command()
    async def join(self, ctx):
        ch = ctx.author.voice.channel
        await ch.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Music(bot))
