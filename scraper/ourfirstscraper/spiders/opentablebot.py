# -*- coding: utf-8 -*-
import scrapy


class OpentableSpider(scrapy.Spider):
    name = 'opentablebot'
    allowed_domains = ['opentable.com']
    start_urls = ['https://www.opentable.com/highway-restaurant-and-bar']

    def parse(self, response):
        reviews = response.css('.review-content p::text').extract()
        for review in reviews:
            yield {'Reviews': review}
