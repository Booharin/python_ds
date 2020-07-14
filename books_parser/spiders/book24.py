import scrapy
from scrapy.http import HtmlResponse
from books_parser.items import BooksParserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/novie-knigi/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//*[contains(text(), 'Далее')]/@href").extract_first()
        books_links = response.css('a.book__title-link::attr(href)').extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parser)

        yield response.follow(next_page, callback=self.parse)

    def book_parser(self, response: HtmlResponse):
        title = response.css('h1::text').extract_first()
        link = response.url
        authors = response.xpath("//div[@class='item-tab__chars-list']/div[1]//a/text()").extract()
        old_price = str(response.css('div[class=item-actions__price-old]::text').extract_first()).replace(' р.', '')
        price_with_discount = response.css('div[class=item-actions__price] b::text').extract_first()
        rate = response.css('span[class=rating__rate-value]::text').extract_first().replace(',', '.')

        yield BooksParserItem(
            title=title,
            link=link,
            authors=authors,
            old_price=old_price,
            price_with_discount=price_with_discount,
            rate=rate
        )
