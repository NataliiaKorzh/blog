# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()


class PostgresqlPipeline:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT')
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            spider.logger.error(f"Error connecting to PostgreSQL: {e}")

    def close_spider(self, spider):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            spider.logger.error(f"Error closing PostgreSQL connection: {e}")

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "INSERT INTO news (headline, url) VALUES (%s, %s)",
                (item["headline"], item["url"])
            )
            self.connection.commit()
        except Exception as e:
            spider.logger.error(f"Error saving item to PostgreSQL: {e}")
        return item
