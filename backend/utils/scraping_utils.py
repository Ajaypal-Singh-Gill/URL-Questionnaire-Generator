import subprocess
import logging
import os

logging.basicConfig(level=logging.DEBUG)

def run_scrapy_spider(url):
    """
    Runs a Scrapy spider script as a subprocess and captures its output.
    """
    try:
        # Resolve the path to the Scrapy script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        scrapy_script = os.path.join(current_dir, '../services/run_scrapy.py')
        scrapy_script = os.path.normpath(scrapy_script)

        # Launch the Scrapy script as a subprocess
        process = subprocess.Popen(
            ['python', scrapy_script, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for the process to complete and capture its output
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            logging.info(f"Scrapy completed successfully for URL: {url}")
            return stdout.decode()  # Return the scraped content or success message
        else:
            logging.error(f"Scrapy failed for URL {url} with error: {stderr.decode()}")
            return None
    except Exception as e:
        logging.error(f"Failed to run Scrapy subprocess for URL {url}: {e}")
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