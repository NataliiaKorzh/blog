# Blog API
This is API service, which helps to read and create articles.
Also, you can use Telegram bot for getting info about the latest article.
There is a scraper, which scrapes more articles, if you need.

# Structure
- RESTful API: you can create your own account, manage it, create articles in your blog and operate them as you want.
- Telegram Bot: helps you to know latest updates.
- Scraper: Get another articles from https://news.ycombinator.com/ every day.

# Used technologies
- Programming language: Python
- Frameworks: Django, DRF
- Telegram bot: aiogram
- Scraping: Scrapy
- Database: PosgreSQL

# How to use
To clone this project from GitHub, follow these steps:

Open your terminal or command prompt.
```shell
git clone git@github.com:NataliiaKorzh/blog.git

```
Run the following commands:
```shell
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

```

Fill your .env file using .env.sample as example

Register your TG bot and get a token you can here.
You can find your Telegram ID using this bot.
Find information about how you can adjust your email for sending mails from app you can here.

# Run with Docker

Docker should be installed
```shell
docker-compose build
docker-compose up
```
# Run scraper
```shell
scrapy crawl articles -a output=database
```
or if you want to scrape data into csv file
```shell
scrapy crawl articles -O articles.csv
```

# Features
- JWT authentication
- Admin panel /admin/
- Documentation is located on /api/doc/swagger/
