
from bs4                    import BeautifulSoup
from datetime               import date
from discord.ext.commands   import Cog

import json
import requests

import sys
sys.path.append('../')
import config


class Baekjoon(Cog):
    def __init__(self, bot):
        print('init baekjoon cog')
        self.bot    = bot

    @Cog.listener()
    async def on_ready(self):
        channel_id = 0
        for guild in self.bot.guilds:
            if guild.name == config.DISCORD_GUILD_NAME:
                for channel in guild.channels:
                    if channel.name == config.DISCORD_CHANNEL_NAME:
                        channel_id = channel.id
                        break
            else: continue
        channel = self.bot.get_channel(channel_id)

        msg = f'```js\n[{date.today()}]\n{self.update()}\n```'
        print(msg)

        for index in range(0, len(msg), 2000):
            await channel.send(msg[ index : index + 2000 ])

    def update(self):
        infos       = {}
        regulate    = {}
        ERROR_USERS = []

        MAX_LINEs   = 100

        with open("res/users.json", "r") as f: users = json.load(f)

        for m in users.keys() :
            info    = {}
            res     = requests.get(f'{config.URL_API}?boj={m}')

            if res.status_code == 200:
                soup                = BeautifulSoup(res.text, 'html.parser')
                info['tier']        = soup.select_one('svg > text.tier-text').get_text()
                info['rate']        = int(soup.select_one('svg > g:nth-child(6) > text.rate.value').get_text().replace(',', ''))
                info['solved']      = int(soup.select_one('svg > g:nth-child(7) > text.solved.value').get_text().replace(',', ''))
                info['percentage']  = int(soup.select_one('svg > text.percentage').get_text()[ : -1 ])

                infos[m] = info

                if info['rate'] >= 1600:
                    regulate[users[m]] = MAX_LINEs
                elif info['rate'] >= 1250:
                    regulate[users[m]] = 3
                else:
                    regulate[users[m]] = 2

            else:
                ERROR_USERS        += [ m ]
                regulate[users[m]] = MAX_LINEs

        with open("data/regulation.json", "w") as f:
            json.dump(regulate, f, indent=4)

        infos = dict(sorted(
            infos.items(),
            key = lambda user: user[1]['rate'],
            reverse=True
        ))

        msg   = []
        for user in infos.keys():
            info = infos[user]
            msg += [ f"{user:12s} : {info['tier']:9s} ({info['percentage']:02d}%) {info['solved']:4d}" ]

        if not len(ERROR_USERS):
            return '\n'.join(msg)
        return '\n'.join(msg) + f'\n[*] An Error Occured on "{", ".join(ERROR_USERS)}"'


async def setup(bot):
    await bot.add_cog(Baekjoon(bot))
