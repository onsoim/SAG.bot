
from discord.ext.commands   import Cog
from json                   import load
from glob                   import glob
from random                 import sample

import os


class EveryKnowledgeIsUsefulSomeday(Cog):
    def __init__(self, bot):
        print(f'Init "{self.__class__.__name__}" Cog')
        self.bot        = bot

        if os.path.exists("res/channels.json"):
            with open("res/channels.json", "r") as j:
                channels  = load(j)
        if 'EKIUS' in channels:
              self.channel = channels["EKIUS"]
        else: self.channel = channels["기본"]

    @Cog.listener()
    async def on_ready(self):
        print(f'Ready "{self.__class__.__name__}" Cog')

        self.pData = "data/EKUIS.json"
        if os.path.exists(self.pData):
            with open(self.pData, "r") as j:
                self.old = load(j)
        else:   self.old = {}

        old = [ f'res/EKIUS/{old}.json' for old in self.old ]
        new = [ knowledge for knowledge in glob('res/EKIUS/*.json') if knowledge.split('/')[-1][:-5] not in self.old.keys()]
        self.today = sample(
            new if new else old,
            k = 1
        )
        print(self.today)


async def setup(bot):
    await bot.add_cog(EveryKnowledgeIsUsefulSomeday(bot))
