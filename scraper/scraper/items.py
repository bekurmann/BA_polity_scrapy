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

class AffairItemOW(scrapy.Item):
    title = scrapy.Field()
    identifier = scrapy.Field()
    date = scrapy.Field()
    politican = scrapy.Field()
    affair_type = scrapy.Field()
    session = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    path = scrapy.Field()

class SessionItemOW(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    path = scrapy.Field()
