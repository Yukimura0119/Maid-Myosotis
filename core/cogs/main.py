import discord
from discord.ext import commands
from core.ext import cog_ext
import datetime as dt


class Main(cog_ext):

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'```\n{round(self.bot.latency*1000)} ms\n```')

    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send('```\n'+msg+'\n```')

    @commands.command()
    async def purge(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)

    @commands.command()
    async def hello(self, ctx):
        embed = discord.Embed(title="Discord Robot YuKiTaN",
                              description="Ya hello!!! My Name is YuKiTaN~~", color=0xfcc9b9,
                              timestamp=dt.datetime.utcnow())
        embed.set_author(name="YuKiTaN", url="https://github.com/Yukimura0119/DiscordBot_YuKiTaN",
                         icon_url="https://avatars.githubusercontent.com/u/35000486?v=4")
        embed.set_thumbnail(
            url="https://avatars.githubusercontent.com/u/35000486?v=4")
        embed.add_field(name="Author", value="Yukimura0119", inline=False)
        embed.add_field(name="Language", value="Python", inline=False)
        embed.add_field(name="Birthday", value="Sep 27, 2020 ", inline=False)
        embed.add_field(name="BloodType", value="A", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def website(self, ctx):
        await ctx.send('Here is my website~\nhttps://github.com/Yukimura0119/DiscordBot_YuKiTaN')


def setup(bot):
    bot.add_cog(Main(bot))
