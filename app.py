# Relevant imports
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

engine = create_engine()
Session = sessionmaker(bind=engine)
cralwer = Cralwer(Session)
crawler.crawl()
