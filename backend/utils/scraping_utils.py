import logging
logging.basicConfig(level=logging.DEBUG)

def read_scraped_content():
    """
    Reads the content scraped by Scrapy from the default file location.
    """
    try:
        logging.info("Inside read_scraped_content.")
        with open('scraped_content.txt', 'r', encoding='utf-8') as f:
            return f.read()
        with open('scraped_content.txt', 'w', encoding='utf-8') as f:
            f.write('')
        return content
    except FileNotFoundError:
        logging.error("Failed to read scraped content from file.")
        return None
    