# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class StarcrawlerItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    nation = scrapy.Field()
    bir = scrapy.Field()
    url = scrapy.Field()
    pic = scrapy.Field()