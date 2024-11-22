from models import URLRecord, ContentRecord

def get_url_record(db, url):
    """Retrieve a URL record from the database."""
    return db.query(URLRecord).filter(URLRecord.url == url).first()


def create_url_record(db, url, status):
    """Create a new URL record."""
    new_url_record = URLRecord(url=url, status=status)
    db.add(new_url_record)
    db.commit()
    db.refresh(new_url_record)
    return new_url_record


def update_url_record_status(db, url_record_id, status):
    """
    Update the status of a URL record by its ID.
    """
    url_record = db.query(URLRecord).filter_by(id=url_record_id).first()
    if not url_record:
        raise ValueError(f"No URL record found with ID: {url_record_id}")

    url_record.status = status
    db.commit()

def get_content_record(db, url_id):
    """Retrieve content record based on URL ID."""
    return db.query(ContentRecord).filter(ContentRecord.url_id == url_id).first()


def create_content_record(db, url_id, questions_json):
    """Create a new content record."""
    new_content_record = ContentRecord(url_id=url_id, content='', questions=questions_json)
    db.add(new_content_record)
    db.commit()
