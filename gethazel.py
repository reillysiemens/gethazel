#!/usr/bin/env python3

import os
import shutil
from tempfile import gettempdir
import requests

BLOG = 'thingsonhazelshead.tumblr.com'
API_URL = 'https://api.tumblr.com/v2/blog'
HAZEL_DIR = os.path.join(gettempdir(), 'hazel')


def main():

    # We're gonna need this directory to download our Hazels.
    if not os.path.exists(HAZEL_DIR):
        os.makedirs(HAZEL_DIR)

    info_url = "{}/{}/info".format(API_URL, BLOG)
    info = requests.get(info_url).json()
    num_posts = int(info['response']['blog']['posts'])
    posts = []
    offset = 0

    while not offset >= num_posts:
        posts_url = "{}/{}/posts?offset={}".format(API_URL, BLOG, offset)
        req = requests.get(posts_url).json()
        posts.extend(req['response']['posts'])
        offset += 20

    image_posts = [p for p in posts if 'photos' in p.keys()]
    urls = [p['photos'][0]['original_size']['url'] for p in image_posts]

    for url in urls:
        img = requests.get(url, stream=True)
        if img.status_code == 200:
            file_path = os.path.join(HAZEL_DIR, url.split('/')[-1])
            with open(file_path, 'wb') as f:
                img.raw.decode_content = True
                shutil.copyfileobj(img.raw, f)

if __name__ == '__main__':
    main()
