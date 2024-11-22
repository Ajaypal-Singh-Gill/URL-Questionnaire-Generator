import logging
import json
from services.cache_service import get_cached_data, set_cache_data
from services.db_service import (
    get_url_record,
    create_url_record,
    get_content_record,
)
from services.tasks import scrape_and_generate_questions

def process_question_generation(db, url, save_to_db):
    logging.info(f"Starting question generation for URL: {url}")

    # Step 1: Check Redis cache
    cached_data = get_cached_data(url)
    if cached_data:
        logging.info(f"Cache hit for URL: {url} - Status: {cached_data.get('status')}")
        if cached_data.get('status') == "completed":
            return {'questions': cached_data['questions']}
        elif cached_data.get('status') == "in_progress":
            logging.info(f"Scraping is still in progress for URL: {url}")
            return {'questions': []}  # Empty response while in progress
            
    # Step 2: Check database
    url_record = get_url_record(db, url)
    if url_record:
        logging.info(f"Database record found for URL: {url} - Status: {url_record.status}")
        if url_record.status == "completed":
            content_record = get_content_record(db, url_record.id)
            if content_record:
                questions = json.loads(content_record.questions)
                set_cache_data(url, {'status': "completed", 'questions': questions})
                return {'questions': questions}
        elif url_record.status == "in_progress":
            set_cache_data(url, {'status': "in_progress"})
            logging.info(f"Scraping is still in progress for URL: {url} (from database)")
            return {'questions': []}  # Empty response while in progress

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
        return {'questions': []}  # Empty response on error

    return {'questions': []}  # Empty response while the task is running
