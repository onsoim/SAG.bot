
from datetime               import datetime, timedelta
from discord.ext.commands   import Cog
from random                 import randint

import json


class Regulation(Cog):
    def __init__(self, bot):
        print('init regulation cog')
        self.bot        = bot
        self.regulate   = {}

    @Cog.listener()
    async def on_ready(self):
        with open("data/regulation.json", "r") as j: self.tier = json.load(j)

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        aID = str(message.author.id)
        cID = message.channel.id

        if cID in self.regulate.keys() and aID == self.regulate[cID]["prev_id"]:
            if self.regulate[cID]["cnt"] == (self.tier[aID] if aID in self.tier.keys() else 2):
                self.regulate[cID]["cnt"] = -1

                try:
                    timeout = 10 + randint(0, 20)
                    await message.channel.send(
                        f"등급이 너무 낮습니다. 등급 올려주세요.\nSAG 규정에 따라 {timeout}분 채금 조치합니다.\n이의가 있는 경우 다이아에게 문의하세요.",
                        reference = message
                    )
                    await message.author.edit(
                        timed_out_until = datetime.now().astimezone() + timedelta(minutes=timeout)
                    )
                except Exception as e:
                    print(f'[*] {e} => {message.content}\n{message}')

            self.regulate[cID]["cnt"] += 1
        else:
            self.regulate[cID] = {
                "prev_id"   : aID,
                "cnt"       : 1,
            }

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(Regulation(bot))
