import asyncio
from pyppeteer import launch
import time
from pathlib import Path
import urllib
import urllib.request as request
import os
import logging
import concurrent.futures
import sys
from .downloader import Downloader
from .pageagent import PageAgent

class Scraper():
    def __init__(self, logLevel = logging.WARNING, headless=True):
        self.configure_logging(logLevel)
        self.patch_pyppeteer()
        self.headless = headless

    def patch_pyppeteer(self):
        import pyppeteer.connection
        original_method = pyppeteer.connection.websockets.client.connect
        def new_method(*args, **kwargs):
            kwargs['ping_interval'] = None
            kwargs['ping_timeout'] = None
            return original_method(*args, **kwargs)

        pyppeteer.connection.websockets.client.connect = new_method

    def configure_logging(self, logLevel):
        logger = logging.getLogger()
        pyppeteer_logger = logging.getLogger('pyppeteer')
        logger.setLevel(logLevel)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('[%(asctime)s %(levelname)s \
%(module)s]: %(message)s'))
        logger.addHandler(handler)
        return logger

    def fetch_urls(self, query, engine='google', maxlist=[200], format='jpg'):
        logger = logging.getLogger()
        print("Fetching URLs..")
        if type(engine) is not list: engine = [ engine ]
        if type(format) is not list: format = [ format ]
        if type(maxlist) is not list: maxlist = [ maxlist for e in engine ]
        assert len(maxlist) == len(engine), f"Length of max ({len(maxlist)}) not same as engine ({len(engine)})"
        self.engine, self.format = engine, format
        urlDict, totalLen = {}, 0
        for e, max in zip(engine, maxlist):
            logger.info(f"Fetching URLs from {e}")
            urlDict[e] = asyncio.get_event_loop().run_until_complete(
                                        self.launch_engine(e, query, max))
            totalLen += len(urlDict[e])
            logger.info(f"Fetched {len(urlDict[e])} URLs from {e}")
            print(f"Fetched {len(urlDict[e])} URLs from {e}")
        logger = logging.getLogger()
        logger.info(f"Total Number of URLs fetched: {totalLen}")
        urlSaved = self.mixUrls(urlDict, maxlist)
        logger.info(f"Number of URLs saving: {len(urlSaved)}")
        print(f"{len(urlSaved)} URLs fetched")
        return urlSaved

    def mixUrls(self, urlDict, maxlist):
        urls = []
        for key, max in zip(urlDict, maxlist):
            urlDict[key] = urlDict[key][:max]
            for url in urlDict[key]:
                if url not in urls:
                    urls.append(url)
        return urls

    def download(self, urls, directory='images/',
                formats=['jpg', 'png', 'jpeg'], default='jpg',
                nworkers=10, timeout=30):
        downloader = Downloader(directory, formats, default,
                                nworkers, timeout)
        downloader.download(urls)

    async def launch_engine(self, engine, query, max=200):
        agent = PageAgent(engine, query, max, self.headless)
        return await agent.get_list()
