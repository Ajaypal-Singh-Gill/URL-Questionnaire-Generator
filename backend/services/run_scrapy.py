import scrapy
from scrapy.crawler import CrawlerProcess
import logging

logging.basicConfig(level=logging.DEBUG)


class ContentSpider(scrapy.Spider):
    name = 'content_spider'

    def __init__(self, url=None, *args, **kwargs):
        super(ContentSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        # Save the scraped content to a file
        filename = f"scraped_content_{hash(response.url)}.txt"  # Unique file per URL
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        logging.info(f"Scraped content saved for URL: {response.url}")


def run_scrapy_spider(url):
    """
    Run the Scrapy spider programmatically.
    """
    logging.info(f"Starting Scrapy spider for URL: {url}")
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'DEBUG',  # Set Scrapy log level
    })
    process.crawl(ContentSpider, url=url)
    process.start()  # Block until the spider completes
    logging.info(f"Scrapy spider finished for URL: {url}")
