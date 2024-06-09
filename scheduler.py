import asyncio
from aiocron import crontab
from subprocess import run


SPIDER_COMMAND = "scrapy crawl articles"


@crontab('0 8 * * *')
async def run_spider():
    run(SPIDER_COMMAND, shell=True)


async def main():
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
