import discord
from discord.ext import commands

import youtube_dl
import asyncio
import math
import random
import itertools
import functools

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
        self.nowplaying = None
        self.playlist = SongList()

        async def audio_player_task():
            while True:
                next_song.clear()
                self.nowplaying = None
                self.nowplaying = await self.playlist.get()
                print(self.nowplaying['title'])
                self.vc.play(
                    discord.FFmpegPCMAudio(self.nowplaying['url'], **ffmpeg_opts), after=lambda x: self.bot.loop.call_soon_threadsafe(next_song.set))
                await next_song.wait()
        self.bg_task = self.bot.loop.create_task(audio_player_task())

    @commands.command()
    async def leave(self, ctx):
        self.playlist.clear()
        ctx.voice_client.stop()
        self.nowplaying = None
        await ctx.voice_client.disconnect()
        self.vc = None

    @commands.command()
    async def join(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        ch = ctx.author.voice.channel
        await ctx.send(message.codeblock(f'Connect to {ch}!'))
        await ch.connect()
        self.vc = ctx.voice_client

    @commands.command()
    async def play(self, ctx, url: str):
        if self.vc is None:
            await self.join(ctx)
        loop = asyncio.get_event_loop()
        partial = functools.partial(
            ydl.extract_info, url, download=False, process=False)
        file = await loop.run_in_executor(None, partial)

        if 'entries' in file:
            cnt = 0
            for song in file['entries']:
                cnt += 1
                song_info = ydl.extract_info(
                    'https://www.youtube.com/watch?v='+song['url'], download=False)
                await self.playlist.put(song_info)
                await asyncio.sleep(5)
            await ctx.send(message.codeblock('ADD {} songs'.format(cnt)))
        else:
            song = ydl.extract_info(file['webpage_url'], download=False)
            await self.playlist.put(song)
            await ctx.send(message.codeblock('ADD - {}'.format(song['title'])))

    @ commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send(message.codeblock('Song Resumed!'))

    @ commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send(message.codeblock('Song Paused!'))

    @ commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        await ctx.send(message.codeblock('Song Skipped!'))

    @commands.command()
    async def clear(self, ctx):
        self.playlist.clear()
        ctx.voice_client.stop()
        self.nowplaying = None
        await ctx.send(message.codeblock('Playlist Cleared!'))

    @ commands.command()
    async def shuffle(self, ctx):
        self.playlist.shuffle()
        await ctx.send(message.codeblock('Playlist shuffled!'))

    @commands.command()
    async def np(self, ctx):
        np = 'Now Playing : '
        if self.nowplaying is None:
            np += 'None'
        else:
            np += '[**{}**]({})'.format(
                self.nowplaying['title'], self.nowplaying['webpage_url'])

        embed = (discord.Embed(description=np, color=0xfcc9b9)
                 .set_footer(text='{} song in queue'.format(len(self.playlist))))
        await ctx.send(embed=embed)

    @ commands.command()
    async def queue(self, ctx, page: int = 1):

        np = 'Now Playing : '
        if self.nowplaying is None:
            np += 'None'
        else:
            np += '[**{}**]({})'.format(
                self.nowplaying['title'], self.nowplaying['webpage_url'])

        items_per_page = 10
        pages = math.ceil(len(self.playlist) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        if len(self.playlist) == 0:
            queue += ('Empty queue.\n')
        else:
            for i, song in enumerate(self.playlist[start:end], start=start):
                queue += '`{}.` [**{}**]({})\n'.format(i + 1,
                                                       song['title'], song['webpage_url'])

        embed = (discord.Embed(description=np+'\n\n**{} tracks:**\n\n{}'.format(len(self.playlist), queue), color=0xfcc9b9)
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
