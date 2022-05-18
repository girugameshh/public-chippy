import os
import discord
import nacl
import ffmpeg
import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class LilChippy(discord.Client):

    def __init__(self, *args, **kwargs):
        super(LilChippy, self).__init__(*args, **kwargs)
        self.client = None
        self.last_played = datetime.datetime.now()

    async def on_ready(self):
        print('Logged on as', self.user)
        channel=self.get_channel(445253726165270543)
        self.client=await channel.connect()

    async def on_message(self, message):
        current_time=datetime.datetime.now()
        delta = current_time - self.last_played
        if message.content.lower()=='omg' and self.client is not None\
                and not self.client.is_playing() and delta.seconds>3:
            audio = discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="omg.mp3", options='-filter:a "volume=0.1"')
            self.client.play(audio)
            self.last_played=current_time

    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None and after.channel.name=="General":
            current_time = datetime.datetime.now()
            delta = current_time - self.last_played
            if self.client is not None \
                    and not self.client.is_playing() and delta.seconds > 3:
                audio = discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="omg.mp3", options='-filter:a "volume=0.1"')
                self.client.play(audio)
                self.last_played = current_time


intents=discord.Intents.default()
intents.voice_states=True
client = LilChippy(intents=intents)
client.run(TOKEN)

