# -*- coding: utf-8 -*-
import scrapy

from scrapy_redis.spiders import RedisSpider
class JdSpider(RedisSpider):
    name = 'jd'
    # allowed_domains = ['jd.com']

    redis_key = "jd:start_urls"

    # def start_requests(self):
    #     # https://search.jd.com/Search?keyword=%E9%BE%99%E6%97%8F&enc=utf-8&wq=%E9%BE%99%E6%97%8F&pvid=3461svmi.4lp0ch
    #     start_url = 'https://list.jd.com/list.html?cat=1713%2C3259%2C3333&page=1&s=209&click=0'
    #     start_url ='https://list.jd.com/list.html?cat=1713,3259,3330&ev=3184_66831&sort=sort_rank_asc&trans=1&JL=2_1_0#J_crumbsBar'
    #     yield  scrapy.Request(url=  start_url  ,   callback=  self.parse )
    #

    def parse(self, response):

        # 数据提取
        selectors = response.xpath('//div[@id="J_goodsList"]/ul/li')
        for selector in selectors:
            price = selector.xpath('.//div[@class="p-price"]//i/text()').get()
            title = selector.xpath('.//div[contains(@class,"p-name")]//em//text()').getall()
            productId = selector.xpath('./@data-sku').get()
            item = {
                'price': price,
                'title': ''.join(title),
                'productId': productId
            }
            comments_url = f'https://sclub.jd.com/comment/productPageComments.action?productId={productId}&score=0&sortType=5&page=0&pageSize=10'
            yield item
            yield scrapy.Request(comments_url, meta={'productId': productId}, callback=self.parseComment)

    def parseComment(self, response):

        import  re
        html =  response.body.decode()
        if html :
            import  json

            json_data = json.loads( html )
            for  line in  json_data.get("comments"):

                content =  line.get("content" , "")
                referenceId = line.get('referenceId' ,"")
                score = line.get('score' , 5 )

                items = {
                    'content': content,
                    'productId': referenceId ,
                    'score' : score,
                }
                print(items)
                yield items

            if json_data.get('maxPage'):
                maxPage = int(json_data['maxPage'])
                if maxPage>=2:
                    for page in range(1, maxPage):
                        maxPageUrl = re.sub('page=\d+', f'page={page}', response.url)
                        print(maxPageUrl)
                        yield scrapy.Request(maxPageUrl, callback=self.parseComment, meta={'productId': referenceId})

