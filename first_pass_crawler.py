# Relevant imports
import attr
import time
import string
from models import Candidate, Report, Office
from navigator import SeleniumNavigator
from parsers import (SearchResultsParser, 
                     DropdownParser, 
                     CandidateProfileParser, 
                     ReportsTableParser)
import logging.config
loginipath = '/home/jay/projects/python_projects/revised-cfs/logging_config.ini'
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class FirstPassCrawler:
    session = attr.ib()
    candidate_list = attr.ib(init=False)
    navigator = attr.ib(init=False)
    
    def __attrs_post_init__(self):
        self.search_results_urls = ['http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=q&FirstName=&Method=0',
                                    'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=x&FirstName=&Method=0',
                                    'http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=z&FirstName=&Method=0']
        # self.search_results_urls = (f'http://media.ethics.ga.gov/search/\
        #        Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=\
        #        {character}&FirstName=&Method=0' for character in string.ascii_lowercase)
        self.navigator = SeleniumNavigator()
        logging.info('attrs post init called')

    def exit(self):
        self.session.close()

    def add_candidate_to_db(self, candidate):
        try:
            self.session.add(candidate)
            self.session.commit()
        except Exception as e:
            logging.info(e)
        return candidate.id

    def add_office_to_db(self, office):
        try:
            self.session.add(office)
            self.session.commit()
        except Exception as e:
            logging.info(e)
            self.session.rollback()
        return office.id
    
    def add_report_to_db(self, report):
        try:
            self.session.add(report)
            self.session.commit()
        except Exception as e:
            logging.info(e)
            self.session.rollback()
        return report.id

    def crawl_reports_table(self, office_id):
        dropdown = DropdownParser(self.navigator.page_source())
        if dropdown.parse() is not None:
            try:
                self.navigator.click_dropdown_initial()
                parser = ReportsTableParser(self.navigator.page_source())
                res = parser.parse()
                for report_link, report in res:
                    try:
                        self.navigator.click_link(report_link)
                        self.navigator.wait_for_contributions_id()
                        #report = Report(url=self.navigator.current_url(), office_id=office_id)
                        report.url = self.navigator.get_current_url()
                        report.office_id = office_id
                        self.add_report_to_db(report)
                        self.navigator.back()
                        self.navigator.click_dropdown_subsequent()
                    except Exception as e:
                        logging.info(e)
            except Exception as e:
                logging.info(e)
    
    def crawl_candidate_profile(self, url, candidate):
        logging.info(f'Current page: {self.navigator.get_current_url()}')
        parser = CandidateProfileParser(self.navigator.page_source())
        for dropdown_link, office in parser.parse():
            if dropdown_link is None:
                continue
            candidate_id = self.add_candidate_to_db(candidate)
            office.candidate_id = candidate_id
            office_id = self.add_office_to_db(office)
            self.navigator.expose_dropdown(dropdown_link)
            try:
                self.crawl_reports_table(office_id)
            except Exception as e:
                logging.info(e)
        self.navigator.navigate(url)
    
    def crawl_candidate_profile_links(self, url):
        self.navigator.navigate(url)
        parser = SearchResultsParser(self.navigator.page_source())  
        for candidate, current_link in parser.parse():
            logging.info(f'Current link id: {current_link}')
            self.navigator.click_link(current_link)
            try:
                # Originally instantiated candidate and added to db here and
                # passed in the candidate_id to crawl_candidate_profile's parser
                self.crawl_candidate_profile(url, candidate)
            except Exception as e:
                logging.info(e)

    def crawl(self):
        for url in self.search_results_urls:
            logging.info(f'Crawling {url}')
            try:
                self.crawl_candidate_profile_links(url)
            except Exception as e:
                logging.info(e)
        self.navigator.close_browser()
