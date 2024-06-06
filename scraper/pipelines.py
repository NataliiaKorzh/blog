# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


class PostgresDemoPipeline:

    def __init__(self):
        hostname = os.environ["POSTGRES_HOST"]
        username = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        database = os.environ["POSTGRES_DB"]

        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        self.cur = self.connection.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS scraped_articles(
            id serial PRIMARY KEY, 
            title text,
            url text,
        )
        """)

    def process_item(self, item, spider):

        self.cur.execute("select * from scraped_articles where title = %s", (item["title"],))
        result = self.cur.fetchone()

        if result:
            spider.logger.warn("Item already in database: %s" % item["title"])

        else:
            self.cur.execute(""" insert into scraped_articles (title, url) values (%s,%s,%s)""", (
                item["title"],
                item["url"]
            ))

            self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
