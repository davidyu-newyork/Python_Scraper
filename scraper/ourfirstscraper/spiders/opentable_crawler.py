# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

#CrawlSpider instead of scrapy.Spider because we want this bot to traverse many different links
class CrawlopenSpider(CrawlSpider):
    #When we reach a certain item count, we will stop
    #we can also set a time limit for it to run using closespider_timeout = x
    custom_settings = {   'CLOSESPIDER_ITEMCOUNT': 10000,
                       }
    name = 'opentable_crawler'
    allowed_domains = ['www.opentable.com']
    #where spider starts from
    start_urls = ['https://www.opentable.com/new-york-city-restaurants']

    #Rules for restricting what Links we want. LinkExtractor extracts every link in the page
    rules = (Rule(LinkExtractor(
        allow=(),
        deny=("book/","my/","start/")),
        callback='parse_review',
        follow=True),)

    #Gets link from LinkExtractor, then extracts the data we want and yields it to
    def parse_review(self, response):
        #extracts review comments
        reviews = response.xpath('//div[@class="review-content"]/p').extract()

        #cleans the data so we have the full review
        #without this the reviews would be broken up into two objects if reviewer used <br>(line breaks)
        if len(reviews) > 0:
            reviews = [item.replace("<br>", " ") for item in reviews]
            reviews = [item.replace("<p>", "") for item in reviews]
            reviews = [item.replace("</p>", "") for item in reviews]

        #extracts the ratings (x/5 stars)
        star_count = response.xpath('//div[@class="star-wrapper"]/div/@title').extract()

        #removes average rating (average rating for restaurant)
        if len(star_count) > 0:
            star_count.pop(0)

        #extracts the name of the reviewer
        names = response.xpath('//div[@class="review-diner-info"]//text()').extract()

        #extracts the location of reviewer and cleans it so it shows up as 'city'
        location = response.xpath('//span[@class="color-light"][2]/text()').extract()
        location = [item.replace('\xa0', '') for item in location]
        location = [item.replace('(', '') for item in location]
        location = [item.replace(')', '') for item in location]

        #takes all of our data and combines it into scraped_info so we can export it in one file
        for item in zip(reviews, star_count, names, location):
            scraped_info = {'Reviews': item[0],
                            'stars' : item[1],
                            'name' : item[2],
                            'location' : item[3]


                   }
            yield scraped_info


