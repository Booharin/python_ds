import scrapy


class BooksParserItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    authors = scrapy.Field()
    old_price = scrapy.Field()
    price_with_discount = scrapy.Field()
    rate = scrapy.Field()
