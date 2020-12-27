# -*- coding: utf-8 -*-
import scrapy


class YelpbotSpider(scrapy.Spider):
    name = 'yelpbot'
    allowed_domains = ['seamless.com']
    start_urls = ['https://www.seamless.com/menu/royce-chocolate-32-w-40th-st-new-york/321581']
    def parse(self, response):
        titles = response.css('.review-container p::text').extract()
        for title in titles:
            yield {'Title' : title}
