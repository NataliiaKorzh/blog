@echo off
cd C:\Users\natal\blog\blog
call .venv\Scripts\activate
scrapy crawl articles -a output=database
