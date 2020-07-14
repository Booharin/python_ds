import scrapy
from scrapy.http import HtmlResponse
from books_parser.items import BooksParserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/books/?page=1']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.pagination-next__text::attr(href)').extract_first()
        books_links = response.css('a.product-title-link::attr(href)').extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parser)

        yield response.follow(next_page, callback=self.parse)

    def book_parser(self, response: HtmlResponse):
        title = response.css('h1::text').extract_first()
        link = response.url
        authors = response.css('a[data-event-label=author]::text').extract()
        old_price = response.css('span[class=buying-priceold-val-number]::text').extract_first()
        price_with_discount = response.css('span[class=buying-pricenew-val-number]::text').extract_first()
        rate = response.css('div[id=rate]::text').extract_first()

        yield BooksParserItem(
            title=title,
            link=link,
            authors=authors,
            old_price=old_price,
            price_with_discount=price_with_discount,
            rate=rate
        )