import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from twisted.internet import reactor
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

class ContentSpider(scrapy.Spider):
    name = 'content_spider'

    def __init__(self, url=None, *args, **kwargs):
        super(ContentSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        # Save the scraped content to a file
        with open('scraped_content.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a URL to scrape.")
        sys.exit(1)

    url = sys.argv[1]

    try:
        settings = Settings({
            'TELNETCONSOLE_ENABLED': False,
            'RETRY_ENABLED': True,
            'RETRY_TIMES': 5,
            'DOWNLOAD_TIMEOUT': 60,
            'LOG_LEVEL': 'DEBUG',
        })

        process = CrawlerProcess(settings=settings)
        process.crawl(ContentSpider, url=url)
        process.start()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        logging.info(f"Reactor stopped")
        if reactor.running:
            reactor.callFromThread(reactor.stop)

