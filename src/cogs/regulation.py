
from datetime               import datetime, timedelta
from discord.ext.commands   import Cog
from random                 import randint

import json


class Regulation(Cog):
    def __init__(self, bot):
        self.bot            = bot
        self.prev_author    = None
        self.counter        = 0

        with open('data/regulation.json', 'r') as j: self.tier = json.load(j)

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author == self.prev_author:
            if self.counter == 2:
                self.prev_author = None

                if message.author.id not in self.tier:
                    try:
                        timeout = 10 + randint(0, 20)
                        await message.channel.send(
                            f"등급이 너무 낮습니다. 등급 올려주세요.\nSAG 규정에 따라 {timeout}분 채금 조치합니다. 이의가 있는 경우 다이아에게 문의하세요.",
                            reference = message
                        )
                        await message.author.edit(
                            timed_out_until = datetime.now().astimezone() + timedelta(minutes=timeout)
                        )
                    except Exception as e:
                        await print(f'[*] {e} => {message.content}\n{message}')

            self.counter += 1
        else:
            self.prev_author, self.counter = message.author, 1

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(Regulation(bot))
