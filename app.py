# Relevant imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from first_pass_crawler import FirstPassCrawler as FPC
import logging.config

loginipath = '/home/jay/projects/python_projects/revised-cfs/logging_config.ini'
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()
logging.info('Initializing crawler.')
crawler = FPC(session)
logging.info('Crawling...')
crawler.crawl()
logging.info('Crawler exiting.')
crawler.exit()
