# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImageItemOW(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    jurisdiction = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    path = scrapy.Field()
