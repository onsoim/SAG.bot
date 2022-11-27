
from datetime       import date
from discord.ext    import commands

import discord

import bot_discord
import config


def main():
    bot = commands.Bot(
        command_prefix = '/',
        intents = discord.Intents.all()
    )

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

        exit(0)

    bot.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
