import subprocess
import logging
import os

logging.basicConfig(level=logging.DEBUG)

def run_scrapy_spider(url):
    """Run Scrapy spider as a subprocess."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        scrapy_script = os.path.join(current_dir, '../scrapy/run_scrapy.py')
        
        # Normalize the path to handle different operating systems
        scrapy_script = os.path.normpath(scrapy_script)
        subprocess.run(['python', scrapy_script, url], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Scrapy subprocess failed for URL {url}: {e}")
        return False
    return True

def read_scraped_content():
    """Read the content scraped by Scrapy from file."""
    try:
        with open('scraped_content.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logging.error("Failed to read scraped content from file.")
        return None
