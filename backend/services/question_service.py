import logging
import json
from services.cache_service import get_cached_data, set_cache_data
from services.db_service import (
    get_url_record,
    create_url_record,
    get_content_record,
)
from services.tasks import scrape_and_generate_questions
import re
import requests

def validate_url(url):
    """Validate the format of the URL and optionally test its reachability."""
    # Basic URL format validation using regex
    regex = re.compile(
        r'^(https?://)'  # http:// or https://
        r'([a-zA-Z0-9.-]+)'  # domain
        r'(\.[a-zA-Z]{2,})'  # top-level domain
        r'(:[0-9]{1,5})?'  # optional port
        r'(\/.*)?$'  # path
    )
    if not re.match(regex, url):
        return False, "Invalid URL format."

    # Optional: Check if URL is reachable
    try:
        response = requests.head(url, timeout=5)
        if response.status_code >= 400:
            return False, "URL is not reachable."
    except requests.RequestException as e:
        return False, f"URL is not reachable"
    
    return True, "URL is valid and reachable."

def process_question_generation(db, url, save_to_db):
    logging.info(f"Starting question generation for URL: {url}")

    # Validate URL before processing
    is_valid, validation_message = validate_url(url)
    if not is_valid:
        logging.error(f"URL validation failed: {validation_message}")
        return {'error': validation_message, 'status': False}
    
    # Step 1: Check Redis cache
    cached_data = get_cached_data(url)
    if cached_data:
        logging.info(f"Cache hit for URL: {url} - Status: {cached_data.get('status')}")
        if cached_data.get('status') == "completed":
            return {'questions': cached_data['questions'], 'status': True}
        elif cached_data.get('status') == "in_progress":
            logging.info(f"Scraping is still in progress for URL: {url}")
            return {'questions': [], 'status': True}  # Empty response while in progress
        elif cached_data.get('status') == "failed":
            logging.info(f"Scraping failed: {cached_data.get('error')}")
            return {'questions': [], 'status': False, 'error': cached_data.get('error')}  # Empty response while in progress
            
    # Step 2: Check database
    url_record = get_url_record(db, url)
    if url_record:
        logging.info(f"Database record found for URL: {url} - Status: {url_record.status}")
        if url_record.status == "completed":
            content_record = get_content_record(db, url_record.id)
            if content_record:
                questions = json.loads(content_record.questions)
                set_cache_data(url, {'status': "completed", 'questions': questions})
                return {'questions': questions, 'status': True}
        elif url_record.status == "in_progress":
            set_cache_data(url, {'status': "in_progress"})
            logging.info(f"Scraping is still in progress for URL: {url} (from database)")
            return {'questions': [], 'status': True}  # Empty response while in progress

    # Step 3: Create URL record (if needed)
    if save_to_db:
        url_record = create_url_record(db, url, "in_progress")

    # Step 4: Trigger Celery task
    logging.info(f"Triggering Celery task for URL: {url}")
    try:
        task = scrape_and_generate_questions.delay(url, save_to_db, url_record.id if url_record else None)
        set_cache_data(url, {'status': "in_progress", 'task_id': task.id}, expiry=3600)
    except Exception as e:
        logging.error(f"Error triggering Celery task for URL: {url}: {str(e)}")
        set_cache_data(url, {'status': "failed"}, expiry=300)  # Short TTL for failure
        return {'questions': [], 'status': False, 'error': f"Scrapping failed: {str(e)}"}  # Empty response on error

    return {'questions': []}  # Empty response while the task is running
