from backend.db.dbconfig import engine, Base
from models import URLRecord, ContentRecord

# Create all tables
Base.metadata.create_all(bind=engine)
