import datetime
import json
import os

import bs4
import requests
from environs import Env
from loguru import logger


def download_image(query, save_directory):
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
            image_name = './{}/{}.jpg'.format(save_directory, i)
            with open(image_name, 'wb') as f:
                f.write(res.content)
                logger.info("Save: {}".format(image_name))
        except Exception as e:
            logger.warning("skip {}, {}".format(url, e))


if __name__ == "__main__":
    env = Env()
    save_directory = env('SAVE_DIRECTORY')
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    query = env("QUERY")
    download_image(query, save_directory)

    image_timestamp_path = env("IMAGE_TIMESTAMP_PATH")
    with open(image_timestamp_path, 'w') as f:
        now = int(datetime.datetime.now().timestamp())
        f.write(str(now))
