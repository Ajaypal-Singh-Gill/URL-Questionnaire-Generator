import scrapy
from scrapy.crawler import CrawlerProcess
import sys

class ContentSpider(scrapy.Spider):
    name = 'content_spider'

    def __init__(self, url=None, *args, **kwargs):
        super(ContentSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        # Save the scraped content to a file
        with open('scraped_content.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Scraped content saved for URL: {response.url}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a URL to scrape.")
        sys.exit(1)

    url = sys.argv[1]

    # Basic Scrapy process with minimal settings
    process = CrawlerProcess()
    process.crawl(ContentSpider, url=url)
    process.start()
