
from datetime               import date
from discord                import Intents
from discord.ext.commands   import Bot

import asyncio
import os

import config


class SAG(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print("Bot is ready")

    async def load_extensions(self, cogs):
        for filename in os.listdir(f'./src/{cogs}'):
            if filename.endswith(".py"):
                await self.load_extension(f'{cogs}.{filename[:-3]}')


async def main():
    bot = SAG(
        command_prefix = '',
        intents = Intents.all()
    )

    await bot.load_extensions('discord_cogs')
    await bot.load_extensions('cogs')

    await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
