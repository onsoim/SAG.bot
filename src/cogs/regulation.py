
from datetime               import datetime, time, timedelta
from discord.ext.commands   import Cog, command
from discord.ext.tasks      import loop
from random                 import sample, randint, seed

import json
import os


class Regulation(Cog):
    prefixes = ['/', '!', '.', '?']

    def __init__(self, bot):
        print('init regulation cog')
        self.bot        = bot
        self.regulate   = {}

        self.pData = "data/keywords.json"
        if os.path.exists(self.pData):
            with open(self.pData, "r") as j:
                self.jKeywords = json.load(j)
        else:   self.jKeywords = { "init": [ "출근", "재택", "대기업" ] }

        self.keywords   = sample(
            list(set([ _ for kw in self.jKeywords.values() for _ in kw ])),
            k = 3
        )
        print(self.keywords)
        self.revealKeywords.start()

    @Cog.listener()
    async def on_ready(self):
        with open("data/regulation.json", "r") as j: self.tier = json.load(j)

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # regulation of keywords
        msg = message.content.replace(" ", "")
        cnt = sum(keyword in msg for keyword in self.keywords)

        aID = str(message.author.id)
        if cnt:
            if aID not in self.tier or self.tier[aID] < 100:
                await self.timeout(message, iter = cnt, msg = "```scss\n[키워드] 오늘의 키워드가 포함되어 있습니다.\n```\n")

        # regulation of lines
        else:
            cID = message.channel.id

            if cID in self.regulate.keys() and aID == self.regulate[cID]["prev_id"] and self.now() < self.regulate[cID]["until"]:
                if self.regulate[cID]["cnt"] == (self.tier[aID] if aID in self.tier.keys() else 2):
                    self.regulate[cID]["cnt"] = -1

                    await self.timeout(message, msg = "```scss\n[등급]이 너무 낮습니다. 등급을 올려주세요.\n```\n")

                self.regulate[cID]["cnt"] += 1
            else:
                self.regulate[cID] = {
                    "prev_id"   : aID,
                    "cnt"       : 1,
                    "until"     : self.now(1),
                }

        await self.bot.process_commands(message)

    def now(self, minutes = 0):
        return datetime.now().astimezone() + timedelta(minutes=minutes)

    async def timeout(self, message, minutes = 0, iter = 1, msg = ""):
        if not minutes:
            seed(self.now())
            minutes = 10
            for _ in range(iter):
                minutes += randint(0, 20)

        try:
            await message.channel.send(
                f"{msg}SAG 규정에 따라 {minutes}분 채금 조치합니다.\n이의가 있는 경우 다이아에게 문의하세요.",
                reference = message
            )

            await message.author.edit(
                timed_out_until = self.now(minutes)
            )
        except Exception as e:
            print(f'[*] {e} => {message.content}\n{message}')

    @command( aliases = [ f'{prefix}kadd' for prefix in prefixes ] )
    async def kadd(self, ctx, keyword):
        aID = str(ctx.author.id)

        if aID not in self.jKeywords:
            if self.tier[aID] > 10:
                self.jKeywords[aID] = [ keyword ]
        elif keyword not in self.jKeywords[aID]:
            self.jKeywords[aID] += [ keyword ]

            with open(self.pData, "w") as f:
                json.dump(self.jKeywords, f, indent = 4)

    @command( aliases = [ f'{prefix}kdel' for prefix in prefixes ] )
    async def kdel(self, ctx, keyword):
        aID = str(ctx.author.id)

        if aID in self.jKeywords and keyword in self.jKeywords[aID]:
            self.jKeywords[aID].remove(keyword)

            with open(self.pData, "w") as f:
                json.dump(self.jKeywords, f, indent = 4)

    @loop(time = time(tzinfo=datetime.now().astimezone().tzinfo))
    async def revealKeywords(self):
        await self.bot.get_channel(968372280528883712).send(f'오늘의 키워드\n{self.keywords}')


async def setup(bot):
    await bot.add_cog(Regulation(bot))
