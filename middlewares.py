# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # 等待一个元素加载完成
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import requests

import pyppeteer
import asyncio
import os

pyppeteer.DEBUG = False

UA = UserAgent()


class RotateUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = UA.random
        print(ua)
        spider.logger.info('Current UserAgent: ' + ua)
        request.headers.setdefault('User-Agent', ua)


class seleniumdownloadMiddleware(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 浏览器不提供可视化页面
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        self.ua = UA.random
        options.add_argument("User-Agent=" + self.ua)
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.TIME_OUT = 10
        self.wait = WebDriverWait(self.driver, self.TIME_OUT)

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        if request.url.startswith('https://list.jd.com/list.html'):
            self.driver.get(request.url)
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//ul[@class="gl-warp clearfix"]//li')
                )
            )
            import time
            time.sleep(1)
            return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
                                status=200)
        else:
            headers = {
                'User-Agent': self.ua
            }
            count = 0
            while True:
                try:
                    text = requests.get(request.url, headers=headers).text
                    return HtmlResponse(url=request.url, body=text, request=request, encoding='utf-8',
                                        status=200)
                except TimeoutError:
                    count += 1
                if count >= 3:
                    break
            return None


class FundscrapyDownloaderMiddleware(object):

    def __init__(self):
        print("Init downloaderMiddleware use pypputeer.")
        os.environ['PYPPETEER_CHROMIUM_REVISION'] = '588429'
        # pyppeteer.DEBUG = False
        print(os.environ.get('PYPPETEER_CHROMIUM_REVISION'))
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.getbrowser())
        loop.run_until_complete(task)
        self.ua = UA.random

        # self.browser = task.result()
        # print(self.browser)
        # print(self.page)
        # self.page = await browser.newPage()

    async def getbrowser(self):
        self.browser = await pyppeteer.launch()
        self.page = await self.browser.newPage()

    async def getnewpage(self):
        return await self.browser.newPage()

    def process_request(self, request, spider):
        if request.url.startswith('https://list.jd.com/list.html'):
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(self.usePypuppeteer(request))
            loop.run_until_complete(task)
            # return task.result()
            return HtmlResponse(url=request.url, body=task.result(), encoding="utf-8", request=request)
        else:
            headers = {
                'User-Agent': self.ua
            }
            count = 0
            while True:
                try:
                    text = requests.get(request.url, headers=headers).text
                    return HtmlResponse(url=request.url, body=text, request=request, encoding='utf-8',
                                        status=200)
                except TimeoutError:
                    count += 1
                if count >= 3:
                    break
            return None


    async def usePypuppeteer(self, request):
        # print(request.url)
        # page = await self.browser.newPage()
        await self.page.goto(request.url)
        content = await self.page.content()
        return content
