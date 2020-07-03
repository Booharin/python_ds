import requests
from pprint import pprint
from pymongo import MongoClient
from lxml import html


class NewsScrapper:
    mongo_client = MongoClient("mongodb://admin:12345@18.197.155.243/my_db")
    my_db = mongo_client.my_db
    news = my_db.news

    header = {'User-Agent':
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    def get_news_from_mail(self):
        mail_news_url = 'https://news.mail.ru/'

        response = requests.get(mail_news_url, headers=self.header)
        dom = html.fromstring(response.text)

        news = dom.xpath("//ul[@class='list list_type_square list_half js-module']/li")
        print(len(news))
        for new_item in news:
            new_data = {
                'source': mail_news_url,
                'name': new_item.xpath(".//a[@class='list__text']/text()")[0].replace('\xa0', ' '),
                'link': mail_news_url + new_item.xpath(".//a[@class='list__text']/@href")[0]
            }

            # date of publication
            new_response = requests.get(new_data['link'], headers=self.header)
            new_dom = html.fromstring(new_response.text)
            time = new_dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
            if len(time) > 0:
                new_data['public_date'] = time[0]

            self.news.replace_one(new_data, new_data, upsert=True)

    def get_news_from_lenta(self):
        lenta_news_url = 'https://lenta.ru/'

        response = requests.get(lenta_news_url, headers=self.header)
        dom = html.fromstring(response.text)

        news = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']")
        print(len(news))
        for new_item in news:
            new_data = {
                'source': lenta_news_url,
                'name': new_item.xpath(".//a//text()")[1].replace('\xa0', ' '),
                'link': lenta_news_url + new_item.xpath(".//a/@href")[0],
                'public_date': new_item.xpath(".//a//@datetime")[0]
            }

            self.news.replace_one(new_data, new_data, upsert=True)

    def get_news_from_yandex(self):
        yandex_news_url = 'https://yandex.ru/'
        response = requests.get(yandex_news_url, headers=self.header)
        dom = html.fromstring(response.text)
        news = dom.xpath("//ol[@class='list news__list']/li")

        for new_item in news:

            new_data = {
                'source': yandex_news_url,
                'name': new_item.xpath(".//span[@class='news__item-content ']/text()")[0],
                'link': new_item.xpath(
                    ".//a[@class='home-link list__item-content list__item-content_with-icon home-link_black_yes']/@href")[
                    0],
            }

            self.news.replace_one(new_data, new_data, upsert=True)

        # animated news
        news_animated = dom.xpath("//ol[@class='list news__list news__animation-list']/li")
        print(len(news) + len(news_animated))

        for new_item in news_animated:
            new_data = {
                'source': yandex_news_url,
                'name': new_item.xpath(".//span[@class='news__item-content ']/text()")[0],
                'link': new_item.xpath(
                    ".//a[@class='home-link list__item-content list__item-content_with-icon home-link_black_yes']/@href")[
                    0],
            }

            self.news.replace_one(new_data, new_data, upsert=True)


news_scrapper = NewsScrapper()
# news_scrapper.news.delete_many({})

news_scrapper.get_news_from_mail()
news_scrapper.get_news_from_lenta()
news_scrapper.get_news_from_yandex()

count = 0
for new in news_scrapper.news.find({}):
    print(new)
    count += 1
print(count)
