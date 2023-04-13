
from datetime               import datetime, timedelta
from discord.ext.commands   import Cog
from random                 import randint, seed

import json


class Regulation(Cog):
    def __init__(self, bot):
        print('init regulation cog')
        self.bot        = bot
        self.regulate   = {}

        self.keywords   = ["금융", "대기업", "재택"]

    @Cog.listener()
    async def on_ready(self):
        with open("data/regulation.json", "r") as j: self.tier = json.load(j)

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # regulation of keywords
        msg = message.content.replace(" ", "")
        if any(keyword in msg for keyword in self.keywords):
            await self.timeout(message)

        # regulation of lines
        else:
            aID = str(message.author.id)
            cID = message.channel.id

            if cID in self.regulate.keys() and aID == self.regulate[cID]["prev_id"] and datetime.now().astimezone() < self.regulate[cID]["until"]:
                if self.regulate[cID]["cnt"] == (self.tier[aID] if aID in self.tier.keys() else 2):
                    self.regulate[cID]["cnt"] = -1

                    await self.timeout(message, msg = "등급이 너무 낮습니다. 등급 올려주세요.\n")

                self.regulate[cID]["cnt"] += 1
            else:
                self.regulate[cID] = {
                    "prev_id"   : aID,
                    "cnt"       : 1,
                    "until"     : datetime.now().astimezone() + timedelta(minutes=1),
                }

        await self.bot.process_commands(message)

    async def timeout(self, message, minutes = 0, msg = ""):
        if not minutes:
            seed(datetime.now())
            minutes = 10 + randint(0, 20)

        try:
            await message.channel.send(
                f"{msg}SAG 규정에 따라 {minutes}분 채금 조치합니다.\n이의가 있는 경우 다이아에게 문의하세요.",
                reference = message
            )

            await message.author.edit(
                timed_out_until = datetime.now().astimezone() + timedelta(minutes=minutes)
            )
        except Exception as e:
            print(f'[*] {e} => {message.content}\n{message}')


async def setup(bot):
    await bot.add_cog(Regulation(bot))
