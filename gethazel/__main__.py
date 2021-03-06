#!/usr/bin/env python3

import os
import shutil
from tempfile import gettempdir
from multiprocessing import Pool, cpu_count
import requests

BLOG = 'thingsonhazelshead.tumblr.com'
API_URL = 'https://api.tumblr.com/v2/blog'
API_KEY = os.environ['GETHAZEL_API_KEY']
BLOG_DIR = os.path.join(gettempdir(), BLOG)


def get_image(url):
    """Download an image at a given url.

    Args:
        url (str): A URL string.

    Returns:
        None
    """
    img = requests.get(url, stream=True)
    if img.status_code == 200:
        file_path = os.path.join(BLOG_DIR, url.split('/')[-1])
        with open(file_path, 'wb') as f:
            img.raw.decode_content = True
            shutil.copyfileobj(img.raw, f)


def main():
    """Main function.

    Args:
        None

    Returns:
        None
    """

    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)

    info_url = "{}/{}/info?api_key={}".format(API_URL, BLOG, API_KEY)
    info = requests.get(info_url).json()
    num_posts = int(info['response']['blog']['posts'])
    posts = []
    offset = 0

    while not offset >= num_posts:
        posts_url = "{}/{}/posts?offset={}&api_key={}".format(API_URL, BLOG,
                                                              offset, API_KEY)
        req = requests.get(posts_url).json()
        posts.extend(req['response']['posts'])
        offset += 20

    image_posts = [p for p in posts if 'photos' in p.keys()]
    urls = [p['photos'][0]['original_size']['url'] for p in image_posts]

    with Pool(cpu_count()) as p:
        p.map(get_image, urls)

if __name__ == '__main__':
    main()
