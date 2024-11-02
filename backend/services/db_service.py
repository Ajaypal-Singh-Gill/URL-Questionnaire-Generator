from models import URLRecord, ContentRecord

def get_url_record(db, url):
    return db.query(URLRecord).filter(URLRecord.url == url).first()

def save_url_record(db, url, status):
    new_url_record = URLRecord(url=url, status=status)
    db.add(new_url_record)
    db.commit()
    return new_url_record

def save_content_record(db, url_id, questions_str):
    content_record = ContentRecord(url_id=url_id, content='', questions=questions_str)
    db.add(content_record)
    db.commit()
