
from datetime       import date
from discord.ext    import commands

import asyncio
import discord
import os

import bot_discord
import config


async def load_extensions():
    cogs_foldername = 'discord_cogs'
    for filename in os.listdir(f'src/{cogs_foldername}'):
        if filename.endswith(".py"):
            await bot.load_extension(f'{cogs_foldername}.{filename[:-3]}')

bot = commands.Bot(
    command_prefix = '/',
    intents = discord.Intents.all()
)

async def main():
    async with bot:
        @bot.event
        async def on_ready():
            channel_id = 0
            for guild in bot.guilds:
                if guild.name == config.DISCORD_GUILD_NAME:
                    for channel in guild.channels:
                        if channel.name == config.DISCORD_CHANNEL_NAME:
                            channel_id = channel.id
                            break
                else: continue
            channel = bot.get_channel(channel_id)

            msg = f'```js\n[{date.today()}]\n{bot_discord.run()}\n```'
            print(msg)

            for index in range(0, len(msg), 2000):
                await channel.send(msg[ index : index + 2000 ])

        @bot.command()
        async def ping(ctx):
            await ctx.send(f'pong! {round(round(bot.latency, 4) * 1000)}ms')

        await load_extensions()
        await bot.start(config.DISCORD_TOKEN)

asyncio.run(main())
