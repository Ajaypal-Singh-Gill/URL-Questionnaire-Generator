import logging
from utils.scraping_utils import read_scraped_content
from services.cache_service import set_cache_data
from services.db_service import update_url_record_status, create_content_record
from services.intent_question_generator import clean_scraped_content, generate_intent_based_questions, parse_questions_and_options
import json
from celery_config import app
from db.dbconfig import get_db
import requests

def scrape_and_save_content(url):
    """
    Scrapes the entire content of a webpage and saves it to a text file.
    
    Args:
        url (str): The URL of the webpage to scrape.
        file_name (str): The name of the file to save the content to.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Get raw HTML content
        html_content = response.text

        with open('scraped_content.txt', 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Full HTML content saved to scraped_content.txt")
        return True
    except Exception as e:
        print(f"Error fetching page: {e}")
        return False
    
@app.task(bind=True, max_retries=3)
def scrape_and_generate_questions(self, url, save_to_db, url_record_id=None):
    """
    Celery task to scrape content and generate questions, with retry on failure.
    """
    try:

        logging.info(f"Starting web scrapping for URL: {url}")
        # Step 1: Run the scraper
        if not scrape_and_save_content(url):
            raise Exception(f"Scraping failed for URL: {url}")

        # Step 2: Process scraped content
        scraped_content = read_scraped_content()
        if not scraped_content:
            raise Exception(f"No content found after scraping URL: {url}")

        # Step 3: Generate questions
        text_content = clean_scraped_content(scraped_content)
        response_message = generate_intent_based_questions(text_content)
        questions = parse_questions_and_options(response_message)
        

        # Step 4: Cache the results
        set_cache_data(url, {'status': "completed", 'questions': questions}, expiry=3600)

        # Step 5: Save to database (if enabled)
        if save_to_db and url_record_id:
            print("url_record_id", url_record_id)
            questions_json = json.dumps(questions)
            logging.info(f"Generated questions for URL: {questions_json}")
            db = next(get_db())
            create_content_record(db, url_record_id, questions_json)
            update_url_record_status(db, url_record_id, "completed")

        return {'status': 'completed', 'questions': questions}

    except Exception as e:
        logging.error(f"Error in scrape_and_generate_questions task: {str(e)}")

        # Retry on transient failures
        if self.request.retries < self.max_retries:
            self.retry(exc=e, countdown=5)  # Retry after 5 seconds

        # Final failure: Cache a temporary failure status
        # set_cache_data(url, {'status': "failed"}, expiry=300)  # Short TTL for failure
        # if save_to_db and url_record_id:
        #     update_url_record_status(None, url_record_id, "failed")
        raise e
