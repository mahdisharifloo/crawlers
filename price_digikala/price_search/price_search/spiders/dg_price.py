import scrapy
from os import path

class QuotesSpider(scrapy.Spider):
    name = "dg_price"

    def start_requests(self):
        x = input("pleas insert your pruduct name :  ")
        yield scrapy.Request('https://www.amazon.com/s?k=%s'%str(x))

    def parse_search_panel(self, response):
        for items in response.xpath('//span/text()'):
            yield item