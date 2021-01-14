from bs4 import BeautifulSoup
import config
import json
import requests


def run():
    # with open("users.json", "r") as f: users = json.load(f)

    msg = {}
    for m in config.USERS:
        info    = {}
        url     = f'{config.URL_API}?boj={m}'
        text    = requests.get(url).text

        soup            = BeautifulSoup(text, 'html.parser')
        info['tier']    = soup.select_one('svg > text.tier-text').get_text()
        info['class']   = soup.select_one('svg > g:nth-child(6) > text.class.value').get_text()
        info['solved']  = soup.select_one('svg > g:nth-child(7) > text.solved.value').get_text()
        info['exp']     = soup.select_one('svg > g:nth-child(8) > text.something.value').get_text()
        msg[m] = info
    msg = json.dumps(msg, indent=4)

    return msg


if __name__ == "__main__":
    run()