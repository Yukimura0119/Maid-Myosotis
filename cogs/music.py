import discord
from discord.ext import commands

import youtube_dl
import asyncio
import math
import random
import itertools

from youtube_dl.utils import RegexNotFoundError

from extension.cog import CogExtension
from tools import message

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '/data/music/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}
ffmpeg_opts = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    'options': '-vn'
}

ydl = youtube_dl.YoutubeDL(ydl_opts)

next_song = asyncio.Event()


class SongList(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class Music(CogExtension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vc = None
        self.playlist = SongList()

        async def audio_player_task():
            while True:
                next_song.clear()
                current = await self.playlist.get()
                print(current['title'])
                self.vc.play(
                    discord.FFmpegPCMAudio(current['url'], **ffmpeg_opts), after=lambda x: self.bot.loop.call_soon_threadsafe(next_song.set))
                await next_song.wait()
        self.bg_task = self.bot.loop.create_task(audio_player_task())

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def join(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        ch = ctx.author.voice.channel
        await ctx.send(message.codeblock(f'connect to {ch}'))
        await ch.connect()
        self.vc = ctx.voice_client

    @commands.command()
    async def play(self, ctx, url: str):
        if self.vc is None:
            await self.join(ctx)
        file = ydl.extract_info(url, download=False)
        title = file['title']
        await self.playlist.put(file)
        await ctx.send(message.codeblock(f'ADD - {title}'))

    @ commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send(message.codeblock('Song Resumed.'))

    @ commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send(message.codeblock('Song Paused.'))

    @ commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        await ctx.send(message.codeblock('Song Skipped.'))

    @commands.command()
    async def clear(self, ctx):
        self.playlist.clear()
        await ctx.send(message.codeblock('Playlist cleared.'))

    @ commands.command()
    async def queue(self, ctx, page: int = 1):
        if len(self.playlist) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(self.playlist) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(self.playlist[start:end], start=start):
            queue += '`{}.` {}\n'.format(i + 1, song['title'])

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(self.playlist), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
