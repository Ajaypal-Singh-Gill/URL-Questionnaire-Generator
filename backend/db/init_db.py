from backend.db.dbconfig import engine, Base
from models import URLRecord, ContentRecord

Base.metadata.create_all(bind=engine)
