import subprocess
import logging
import os

logging.basicConfig(level=logging.DEBUG)

def run_scrapy_spider(url):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        scrapy_script = os.path.join(current_dir, '../services/run_scrapy.py')
        scrapy_script = os.path.normpath(scrapy_script)

        process = subprocess.Popen(
            ['python', scrapy_script, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Monitor progress
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            logging.info(f"Scrapy completed successfully for URL: {url}")
            return True
        else:
            logging.error(f"Scrapy failed for URL {url} with error: {stderr.decode()}")
            return False
    except Exception as e:
        logging.error(f"Failed to run Scrapy subprocess for URL {url}: {e}")
        return False


def read_scraped_content():
    """Read the content scraped by Scrapy from file."""
    try:
        with open('scraped_content.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logging.error("Failed to read scraped content from file.")
        return None
