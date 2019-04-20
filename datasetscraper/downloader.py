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
import requests as req
import traceback
from multiprocessing.pool import ThreadPool
from fastprogress import progress_bar
import imghdr

class Downloader():
    def __init__(self, directory='images/', formats=['jpg', 'png', 'jpeg'],
                 default='jpg', nworkers=10, timeout=60):
        self.formats, self.default = formats, default
        self.directory = Path(directory)
        self.MBFACTOR = float(1 << 20)
        self.nworkers, self.timeout = nworkers, timeout
        if not os.path.exists(directory):
            os.makedirs(directory)

    def download(self, urls, timeout=200):
        self.timeout = timeout
        logger = logging.getLogger()
        urls = self.clean_urls(urls)
        with concurrent.futures.ThreadPoolExecutor(
                                    max_workers = self.nworkers) as ex:
            futures = [ex.submit(self.save_image, url['url'],
                       self.directory/f"{str(i) + url['format']}") for i,\
                       url in enumerate(urls)]
            for f in progress_bar(concurrent.futures.as_completed(futures),
                       total=len(urls)): pass
        self.verify()

    def save_file(self, file_name, response):
        with open(file_name, 'wb') as fh:
            for chunk in response.iter_content(1024 * 1024):
                fh.write(chunk)

    def save_image(self, url, file_name):
        logger = logging.getLogger()
        opener = request.build_opener()
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; \
        rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        try:
            opener.addheaders = [('User-agent', user_agent)]
            request.install_opener(opener)
            logger.info(f"[Downloading] {url} [AS FILE] {file_name}")
            response = req.get(url, timeout=self.timeout)
            self.save_file(file_name, response)
            try:
                size = int(response.headers['Content-Length'])/self.MBFACTOR
            except:
                size = 0
        except Exception as e:
            # logger.info(f"[FAILED] {file_name} - {url} because: \n{e}")
            # logger.info(f"[EXCEPTION]:{traceback.print_tb(e.__traceback__)}")
            if os.path.isfile(file_name): #Delete if urlretrieve fails
                os.remove(file_name)
            return #exit function
        # logger.info(f"[Downloading] {file_name}")
        logger.info(f"[Done] {file_name} with size: {round(size, 3)} MB")

    def clean_urls(self, urls):
        formats = [f'.{format}' for format in self.formats]
        default = f".{self.default}"
        furls = []
        for url in urls:
            found = False
            for format in formats:
                if format in url:
                    found = True
                    break
            if not found:
                continue
            furls.append({
                            'url':url,
                            'format':format,
                            })
        return furls

    def verify(self):
        print("Verifying download...")
        logger = logging.getLogger("Verifying download...")
        deleted = 0
        for file in os.listdir(self.directory):
            if not imghdr.what(self.directory/file):
                os.remove(self.directory/file)
                deleted += 1
        print(f"Deleted {deleted} corrupt/non-image files")
        logger = logging.getLogger(f"Deleted {deleted} corrupt/non-image files")
