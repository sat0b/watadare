import argparse
import json

import bs4
import requests
from loguru import logger


def download_image(query):
    url = "https://www.google.co.jp/search?q=" + query + "&source=lnms&tbm=isch"
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    res = requests.get(url, headers=header)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    result = soup.find_all('div', {'class': 'rg_meta'})
    for i, a in enumerate(result):
        image_url = json.loads(a.text)['ou']
        try:
            res = requests.get(image_url)
            image_name = './static/image/{}.jpg'.format(i)
            with open(image_name, 'wb') as f:
                f.write(res.content)
                logger.info("Save: {}".format(image_name))
        except:
            logger.warning("skip " + image_url)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', default="芸能人")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    download_image(args.query)
