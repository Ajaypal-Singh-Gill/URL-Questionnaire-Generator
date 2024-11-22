import subprocess
import logging
import os

logging.basicConfig(level=logging.DEBUG)

def run_scrapy_spider(url):
    """
    Runs a Scrapy spider script as a subprocess and captures its output.
    """
    try:
        logging.info(f"Inside scrapy spider: {url}")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        scrapy_script = os.path.join(current_dir, '../services/run_scrapy.py')
        scrapy_script = os.path.normpath(scrapy_script)
        logging.debug(f"Resolved Scrapy script path: {scrapy_script}")
        result = subprocess.run(
            ['python', scrapy_script, url],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            logging.info(f"Scrapy completed successfully for URL: {url}")
            print(f"Scraped content:\n{result.stdout}")  # Print the scraped content
            return result.stdout  # Return the scraped content
        else:
            logging.error(f"Scrapy failed for URL {url} with error: {result.stderr}")
            return None
    except Exception as e:
        logging.error(f"Error running Scrapy spider for URL {url}: {e}")
        return None


def read_scraped_content():
    """
    Reads the content scraped by Scrapy from the default file location.
    """
    try:
        with open('scraped_content.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logging.error("Failed to read scraped content from file.")
        return None