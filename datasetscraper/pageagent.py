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

SANDBOX_ERROR = """No usable sandbox for chrome.\nFor a quick fix try \
running: `sudo sysctl -w kernel.unprivileged_userns_clone=1` on your linux \
shell. You need to set up chrome sandbox, for more info check out: \nhttps\
://github.com/GoogleChrome/\
puppeteer/blob/master/docs/troubleshooting.md"""

class PageAgent():
    def __init__(self, engine, query, max=200, headless=True):
        self.engine = engine
        self.query = query
        self.max = max
        self.headless = headless
        # More search engine support coming soon, please update the INFO
        # dict below if you can.
        self.INFO = {
                "google":{
                            "nclick": 400,
                            "nscroll": 5,
                            "urlStart": "https://www.google.com/search?q=",
                            "urlEnd": "&source=lnms&tbm=isch",
                            "jClick": "document.getElementById(\"smb\").click();",
                            "jsFunc": "Array.from(document.querySelectorAll('.rg_di .rg_meta')).\
                                      map(el=>JSON.parse(el.textContent).ou);"
                },
                "yahoo":{
                            "nclick": 500,
                            "nscroll": 10,
                            "urlStart": "https://images.search.yahoo.com/search/images;?&p=",
                            "urlEnd": "&ei=UTF-8&iscqry=&fr=sfp",
                            "jClick": "document.getElementsByClassName(\"ygbt more-res\")[0].click();",
                            #jsFunc is pretty hard to write here
                            "jsFunc": "Array.from(document.querySelectorAll('a.iusc')).map(x=>x.attributes.m).map(x=>JSON.parse(x.nodeValue)[\"murl\"]);",
                },
                "bing":{
                            "nclick": 400,
                            "nscroll": 10,
                            "urlStart": "https://www.bing.com/images/search?q=",
                            "urlEnd": "&source=lnms&tbm=isch",
                            "jClick": "document.getElementsByClassName(\"btn_seemore cbtn mBtn\")[0].click();",
                            "jsFunc": "Array.from(document.querySelectorAll('a.iusc')).map(x=>x.attributes.m).map(x=>JSON.parse(x.nodeValue)[\"murl\"]);",
                },
                "duckduckgo":{
                            "nclick": 500,
                            "nscroll": 10,
                            "urlStart": "https://duckduckgo.com/?q=",
                            "urlEnd": "&t=h_&ia=images&iax=images",
                            "jClick": "document.getElementsByClassName(\"btn_seemore cbtn mBtn\")[0].click();",
                            "jsFunc": "Array.from(document.querySelectorAll('img.tile--img__img')).map(x=>x.src).map(x=>JSON.parse(x.nodeValue)[\"murl\"]);",
                },
                "baidu":{
                            "nclick": 500,
                            "nscroll": 25,
                            "urlStart": "https://image.baidu.com/search/index?tn=baiduimage&word=",
                            "urlEnd": "",
                            "jClick": "document.getElementsByClassName(\"btn_seemore cbtn mBtn\")[0].click();",
                            "jsFunc": "Array.from(document.querySelectorAll('li.imgitem')).map(x=>x.dataset.objurl);",
                },
        }

    async def scroll(self, page, nscroll):
        logger = logging.getLogger()
        jscroll = "window.scrollBy(0, document.body.scrollHeight);"
        logger.info(f"[SCROLLING PAGE..]")
        for x in range(nscroll):
            try:
                await page.evaluate(jscroll)
                await page.waitFor(2000)
            except:
                logger.info(f"Can't scroll")
                return

    async def click_more(self, page, nscroll, jClick, nclicks = 1):
        logger = logging.getLogger()
        logger.info(f"[NClicks: ] {nclicks}")
        if nclicks == 0:
            await self.scroll(page, nscroll)
            return

        for _ in range(nclicks):
            try:
                await self.scroll(page, nscroll)
                await page.evaluate(jClick, force_expr=True),
                await self.scroll(page, nscroll)
            except:
                return

    async def get_list(self):
        engine, query, max = self.engine, self.query, self.max
        info = self.INFO[engine]
        nclick = max // info['nclick'] + 1
        if nclick < 2:
            nclick = 0
        try:
            browser = await launch(headless=self.headless)
        except Exception as exception:
            print(SANDBOX_ERROR)
            sys.exit(0)
        if self.engine == 'baidu':
            nclick = 0
        page = await browser.newPage()
        await page.setUserAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64)\
                                AppleWebKit/537.36 (KHTML, like Gecko) \
                                Chrome/66.0.3359.181 Safari/537.36")
        url = info['urlStart'] + str(query) + info['urlEnd']
        await page.goto(url, timeout=0)
        await self.click_more(page, info['nscroll'], info['jClick'], nclick)
        urlList = await page.evaluate(info["jsFunc"], force_expr=True)
        await browser.close()
        return urlList
