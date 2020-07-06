# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CommentscrawlerItem(scrapy.Item):
    comment_people = scrapy.Field()
    comment_time = scrapy.Field()
    text = scrapy.Field()
    stars_desc = scrapy.Field()
