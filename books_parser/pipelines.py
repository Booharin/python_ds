from pymongo import MongoClient


class BooksParserPipeline:

    def __init__(self):
        self.mongo_client = MongoClient("mongodb://admin:12345@18.197.155.243/my_db")
        self.books = self.mongo_client.my_db.books

    def process_item(self, item, spider):
        item['old_price'] = int(item['old_price'])
        item['price_with_discount'] = int(item['price_with_discount'])
        item['rate'] = float(item['rate'])

        self.books.replace_one(item, item, upsert=True)

        return item
