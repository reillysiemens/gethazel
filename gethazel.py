#!/usr/bin/env python3

import asyncio
import os

import aiohttp
import click
from yarl import URL


class Blog:
    """ TODO """

    def __init__(self, name, api_key, session):
        self.name = name
        self._session = session
        self._api_key = api_key
        self._base_url = URL.build(scheme="https", host="api.tumblr.com")

    def _photo_posts_url(self, params=None):
        """ TODO """
        path = f"/v2/blog/{self.name}/posts/photo"
        params = dict(api_key=self._api_key, **params or {})
        return self._base_url.with_path(path).with_query(params)

    async def _fetch(self, url):
        async with self._session.get(url) as response:
            return await response.json()

    def _photos(self, response):
        if "posts" in response:
            for post in response["posts"]:
                if "photos" in post:
                    for photo in post["photos"]:
                        yield photo

    async def photos(self):
        """ TODO """
        url = self._photo_posts_url()
        data = await self._fetch(url)
        response = data["response"]
        for photo in self._photos(response):
            yield photo

        while "_links" in response:
            url = self._photo_posts_url(
                params=response["_links"]["next"]["query_params"]
            )
            data = await self._fetch(url)
            response = data["response"]
            for photo in self._photos(response):
                yield photo

    async def download_photos(self):
        """ TODO """
        async for photo in self.photos():
            print(photo["original_size"]["url"])


async def _main(name, api_key):
    """ TODO """
    async with aiohttp.ClientSession() as session:
        blog = Blog(name=name, api_key=api_key, session=session)
        await blog.download_photos()


@click.command()
@click.argument("blog")
def main(blog):
    """ TODO """
    api_key = os.getenv("TUMBLR_TOKEN")
    if not api_key:
        click.ClickException("Missing Tumblr API key")

    asyncio.run(_main(name=blog, api_key=api_key))


if __name__ == "__main__":
    main()
