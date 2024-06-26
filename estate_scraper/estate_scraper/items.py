# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EstateScraperItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    pictures = scrapy.Field()
    rent_price = scrapy.Field()
    description = scrapy.Field()
    phone_number = scrapy.Field()
    email = scrapy.Field()
