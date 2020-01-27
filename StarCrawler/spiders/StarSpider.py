# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from StarCrawler.items import StarcrawlerItem

class StarspiderSpider(scrapy.Spider):
    name = 'StarSpider'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/fenlei/%E6%98%8E%E6%98%9F',
        'http://baike.baidu.com/fenlei/%E7%83%AD%E7%82%B9%E4%BA%BA%E7%89%A9',
        'http://baike.baidu.com/fenlei/%E4%BD%93%E8%82%B2%E4%BA%BA%E7%89%A9',
        'http://baike.baidu.com/fenlei/%E5%A8%B1%E4%B9%90%E4%BA%BA%E7%89%A9']

    def __init__(self):
        self.id = 1

    def parse(self, response):
        base_url = "https://baike.baidu.com"
        url_list = response.xpath("//*[@id='content-main']/div[3]/div[2]/div[1]/div[2]/div[1]/a/@href").extract()
        for url in url_list:
            for i in range(1,30):
                yield Request(base_url + url + "?limit=30&index={}&offset={}#gotoList".format(i, (i-1)*30), callback=self.parse_category)

    def parse_category(self, response):
        base_url = "https://baike.baidu.com"
        url_list = response.xpath("//a[@class='title nslog:7450']/@href").extract()
        for url in url_list:
            yield Request(base_url + url, callback=self.parse_name)

    def parse_name(self, response):
        items = StarcrawlerItem()

        items['id'] = self.id
        self.id += 1

        items['name'] = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()[0]
        
        nation = response.xpath('//dt[@class="basicInfo-item name" and contains(text(),"国\xa0\xa0\xa0\xa0籍")]/following-sibling::dd[1]/text()').extract_first("").split()
        if nation != []:
            items['nation'] = nation[0] 
        elif response.xpath('//dt[@class="basicInfo-item name" and contains(text(),"国\xa0\xa0\xa0\xa0籍")]/following-sibling::dd[1]/a/text()').extract_first("").split() != []:
            items['nation'] = response.xpath('//dt[@class="basicInfo-item name" and contains(text(),"国\xa0\xa0\xa0\xa0籍")]/following-sibling::dd[1]/a/text()').extract_first("").split()[0]
        else:
            items['nation'] = ""

        bir = response.xpath('//dt[@class="basicInfo-item name" and contains(text(),"出生日期")]/following-sibling::dd[1]/text()').extract_first("").split()
        items['bir'] = bir[0] if bir != [] else ""

        items['url'] = response.url

        items['pic'] = response.xpath("//div[@class='summary-pic']/a/img/@src").extract_first("")

        yield items
