import discord
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from typing import *
from config import HOME_GUILD_ID

HOME_CHANNEL_ID = 930471825668988959
FOURTWENTY_GUILD_ID = HOME_GUILD_ID
FOURTWENTY_CHANNEL_ID = 930471947563855882

class InsideJokes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.running = False
        self.fourtwenty: Optional[discord.Channel] = None
        self.home: Optional[discord.Guild] = None
        self.sendwarn = []
        if self.bot.is_ready():
            asyncio.create_task(self.on_ready())

    def cog_unload(self):
        self.running = False

    @commands.Cog.listener()
    async def on_ready(self):
        self.fourtwenty = self.bot.get_guild(FOURTWENTY_GUILD_ID).get_channel(FOURTWENTY_CHANNEL_ID)
        self.home = self.bot.get_guild(HOME_GUILD_ID)
        self.home_channel = self.home.get_channel(HOME_CHANNEL_ID)
        if not self.running:
            await self.run()

    async def run(self):
        self.running = True
        while self.running:
            try:
                now = datetime.now()

                if now.hour == 4 and now.minute == 20:
                    await self.fourtwenty.send("420")

                for user in self.home.members:
                    if user.activity and user.activity.name == 'League of Legends':
                        if user.id not in self.sendwarn and user.activity.start and (now - user.activity.start) > timedelta(minutes=50):
                            self.sendwarn.append(user.id)
                    elif user.id in self.sendwarn:
                        await self.home_channel.send(f'{user.mention} that was a long ass match, did you win?')
                        self.sendwarn.remove(user.id)
            except Exception as error:
                print(error)

            await asyncio.sleep(60)

def setup(bot: commands.Bot):
    bot.add_cog(InsideJokes(bot))
