# Relevant imports
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from crawler import Crawler

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()
crawler = Crawler(session)
crawler.crawl()
crawler.exit()
