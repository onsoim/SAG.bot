
from datetime               import date
from discord                import Intents
from discord.ext.commands   import Bot

import asyncio
import os

import bot_discord
import config


class SAG(Bot):
    def __init__(self, *args, **kwargs):
        # super().__init__(
        #   command_prefix = '',
        #   intents = discord.Intents.all()
        # )
        super().__init__(*args, **kwargs)

    async def load_extensions(self, cogs):
        for filename in os.listdir(f'./src/{cogs}'):
            if filename.endswith(".py"):
                await self.load_extension(f'{cogs}.{filename[:-3]}')

    async def on_ready(self):
        channel_id = 0
        for guild in self.guilds:
            if guild.name == config.DISCORD_GUILD_NAME:
                for channel in guild.channels:
                    if channel.name == config.DISCORD_CHANNEL_NAME:
                        channel_id = channel.id
                        break
            else: continue
        channel = self.get_channel(channel_id)

        msg = f'```js\n[{date.today()}]\n{bot_discord.run()}\n```'
        print(msg)

        for index in range(0, len(msg), 2000):
            await channel.send(msg[ index : index + 2000 ])


async def main():
    bot = SAG(
        command_prefix = '',
        intents = Intents.all()
    )

    await bot.load_extensions('discord_cogs')
    await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
