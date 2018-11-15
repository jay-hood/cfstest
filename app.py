# Relevant imports
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from first_pass_crawler import FirstPassCrawler as FPC
import logging.config
import os

loginipath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logging_config.ini'))
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


# engine = create_engine('postgresql+psycop2:///TestDB')
try:
    engine = create_engine('sqlite:///database.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    logging.info('Initializing crawler.')
    crawler = FPC(session)
    logging.info('Crawling...')
    crawler.crawl()
    logging.info('Crawler exiting.')
    crawler.exit()
except Exception as e:
    logging.info(e)
