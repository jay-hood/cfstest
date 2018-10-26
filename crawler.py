# Relevant imports
import attr
import string
from models import Report
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
class Crawler:
    session = attr.ib()
    candidate_list = attr.ib(init=False)
    navigator = attr.ib(init=False)
    
    def __attrs_post_init__(self):
        self.search_results_urls = ['http://media.ethics.ga.gov/search/Campaign/Campaign_Namesearchresults.aspx?CommitteeName=&LastName=a&FirstName=&Method=0']
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
        except Exception:
            self.session.rollback()
        return office.id
    
    def add_report_to_db(self, report):
        try:
            self.session.add(report)
            self.session.commit()
        except Exception:
            self.session.rollback()
        return report.id

    def crawl_reports_table(self, office_id):
        self.navigator.click_dropdown_initial()
        parser = ReportsTableParser(self.navigator.page_source())
        for report_link in parser.parse():
            self.navigator.follow_link(report_link)
            report = Report(url=self.navigator.current_url(), office_id=office_id)
            self.add_report_to_db(report)
            self.navigator.back()
            self.navigator.click_dropdown_subsequent()
    
    def crawl_candidate_profile(self, url, candidate_id):
        parser = CandidateProfileParser(self.navigator.page_source())
        for dropdown_link, office in parser.parse(candidate_id):
            office_id = self.add_office_to_db(office)
            self.navigator.expose_dropdown(dropdown_link)
            self.crawl_reports_table(office_id)
        self.navigator.navigate(url)
    
    def crawl_candidate_profile_links(self, url):
        self.navigator.navigate(url)
        parser = SearchResultsParser(self.navigator.page_source())
        for current_link, candidate in parser.parse():
            candidate_id = self.add_candidate_to_db(candidate)
            self.navigator.follow_link(current_link)
            self.crawl_candidate_profile(url, candidate_id)
    
    def crawl(self):
        for url in self.search_results_urls:
            self.crawl_candidate_profile_links(url)
