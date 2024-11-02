from models import URLRecord, ContentRecord
from utils.scraping_utils import run_scrapy_spider, read_scraped_content
from services.intent_question_generator import clean_scraped_content, generate_intent_based_questions, parse_questions_and_options
import logging
import json
import pdb

def process_question_generation(db, url, save_to_db):
    logging.debug(f"Processing question generation for URL: {url}")

    # Check if URL is already in the database if saving is required
    if save_to_db:
        # pdb.set_trace() 
        url_record = db.query(URLRecord).filter(URLRecord.url == url).first()
        if url_record:
            if url_record.status == "completed":
                # Fetch and parse questions from JSON format
                content_record = db.query(ContentRecord).filter(ContentRecord.url_id == url_record.id).first()
                if content_record:
                    questions = json.loads(content_record.questions)  # Parse JSON
                    return {'questions': questions}
                
                # TODO: Handle In-progress flow as well.

        # Add a new URL record to track scraping status
        new_url_record = URLRecord(url=url, status="in_progress")
        db.add(new_url_record)
        db.commit()
        db.refresh(new_url_record)
    else:
        logging.debug(f"Skipping database save for URL {url}")

    # Run scraping and handle errors
    if not run_scrapy_spider(url):
        if save_to_db:
            new_url_record.status = "failed"
            db.commit()
            logging.error("Failed to scrape the URL. Please try again later.")
        return {'questions': []}

    # Process scraped content
    scraped_content = read_scraped_content()
    if scraped_content is None:
        if save_to_db:
            new_url_record.status = "failed"
            db.commit()
            logging.error("Failed to scrape the URL. Please try again later.")
        return {'questions': []}

    # Generate questions
    text_content = clean_scraped_content(scraped_content)
    response_message = generate_intent_based_questions(text_content)
    questions = parse_questions_and_options(response_message)

    if save_to_db:
        # Store questions in JSON format
        questions_json = json.dumps(questions)  # Convert list to JSON string
        new_content_record = ContentRecord(url_id=new_url_record.id, content='', questions=questions_json)
        db.add(new_content_record)
        
        # Update URL record status to "completed"
        new_url_record.status = "completed"
        db.commit()

    return {'questions': questions}
