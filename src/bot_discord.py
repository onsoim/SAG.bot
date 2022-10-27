
from bs4 import BeautifulSoup

import json
import requests

import config


ERROR_USERS = []


def simplified():
    infos = dict(sorted(
        json.loads(formatted()).items(),
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


def formatted():
    global ERROR_USERS
    
    with open("res/users.json", "r") as f: users = json.load(f)

    msg = {}
    for m in users['ADMINs'] + users['MEMBERs']:
        info    = {}
        url     = f'{config.URL_API}?boj={m}'
        res     = requests.get(url)

        if res.status_code == 200:
            soup                = BeautifulSoup(res.text, 'html.parser')
            info['tier']        = soup.select_one('svg > text.tier-text').get_text()
            info['rate']        = int(soup.select_one('svg > g:nth-child(6) > text.rate.value').get_text().replace(',', ''))
            info['solved']      = int(soup.select_one('svg > g:nth-child(7) > text.solved.value').get_text().replace(',', ''))
            info['class']       = soup.select_one('svg > g:nth-child(8) > text.class.value').get_text()
            info['percentage']  = int(soup.select_one('svg > text.percentage').get_text()[ : -1 ])
            msg[m] = info
        else:
            ERROR_USERS        += [ m ]

    return json.dumps(msg, indent=4)


def run():
    return simplified()


if __name__ == "__main__":
    print(run())
