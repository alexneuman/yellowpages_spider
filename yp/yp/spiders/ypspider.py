"""Finds the phone number and email of yellow pages search """

import scrapy


class YpspiderSpider(scrapy.Spider):
    name = 'ypspider'
    allowed_domains = ['yellowpages.com']
    start_urls = ['https://www.yellowpages.com/new-york-ny/real-estate-agents?fbclid=IwAR350sew49-JZhbPyle6iSMIXpIrSB71XVwwHee5_6cO_FV2pqISaePJuao/']

    def parse(self, response):
        for url in response.xpath('.//div[@class="v-card"]//a[contains(@class, "media-thumbnail")]/@href').getall():
            yield response.follow(url=url, callback=self.business_page)

        next_page = response.xpath('.//a[@class="next ajax-page"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    
    def business_page(self, response):
        email = response.xpath('.//a[@class="email-business"]/@href').get()
        yield {
        'name': response.css('.sales-info h1').get(),
        'phone': response.xpath('.//p[@class="phone"]/text()').get(),
        'email': email.replace('mailto:', '') if email else None
        }
