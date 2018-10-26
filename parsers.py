from abc import ABC, abstractmethod
import attr
from nameparser import HumanName
from lxml import html
from models import Candidate, Report, Office 
import logging.config

loginipath = '/home/jay/projects/python_projects/revised-cfs/logging_config.ini'
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class AbstractParser(ABC):
    page_content = attr.ib()

    @abstractmethod
    def parse(self):
        pass


class CandidateProfileParser(AbstractParser):

    def parse(self):
        _xpath = "//*[@id='ctl00_ContentPlaceholder1_NameInfo1_dlDOIs']/tbody/tr[@class!=gridviewheader]"
        tree = html.fromstring(self.page_content)
        body = tree.xpath(_xpath)
        # returns a tuple consisting of the dropdown link and an office orm object.
        dropdown_links = []
        offices = []
        if body is None:
            return [(),]
        for tr in body:
            try:
                filer_id = tr.xpath('.//td[1]/text()').pop()
                office_sought = tr.xpath('.//td[2]/span/text()').pop()
                dropdown_link = tr.xpath('.//td[3]/a/@id').pop()
                status = tr.xpath('.//td[4]/span/text()').pop()
                office = Office(filer_id=filer_id, office_sought=office_sought, status=status)
                offices.append(office)
                dropdown_links.append(dropdown_link)
            except Exception as e:
                logging.info(e)

        return [(dropdown_link, office) for dropdown_link, office 
                in zip(dropdown_links,offices)]

class DropdownParser(AbstractParser):

    def parse(self): 
        return 'ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_Label2'

class SearchResultsParser(AbstractParser):

    def parse(self):
        _xpath = "//*[@id='ctl00_ContentPlaceHOlder1_Search_List']/tbody/tr[@class!='gridviewheader']"
        # returns a list of parsed links containing the ids of candidate profile links
        tree = html.fromstring(self.page_content)
        body = tree.xpath(_xpath)
        candidates = []
        link_ids = []
        if body is None:
            return [(),]
        for tr in body:
            try:
                js_id = tr.xpath('.//td[2]/span/text()').pop()
                candidate_name = tr.xpath('.//td[2]/span/text()').pop()
                name = HumanName(candidate_name)
                candidate = Candidate(firstname=name.firstname, middlename=name.middlename, lastname=name.lastname)
                candidates.append(candidate)
                link_ids.append(js_id)
            except Exception as e:
                logging.info(e)

        return [(cand, _id) for cand, _id in zip(candidates, link_ids)] 

class ReportsTableParser(AbstractParser):

    def parse(self):
        _xpath = "//*[@id='ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_dgReports']/tbody/tr[@class!='gridviewheader']"
        tree = html.fromstring(self.page_content)
        body = tree.xpath(_xpath)
        links = []
        reports = []
        if body is None:
            return [(),]
        for tr in body:
            try:
                link = tr.xpath('.//td[1]/a/@id').pop()
                report_type = tr.xpath('.//td[2]/span/text()').pop()
                year = tr.xpath('.//td[3]/text()').pop()
                report_filed_date = tr.xpath('.//td[4]/text()').pop()
                report_received_by = tr.xpath('.//td[5]/span/text()').pop()
                report_received_date = tr.xpath('.//td[6]/span/text()').pop()
                links.append(link)
                report = Report(report_type=report_type,
                                year=year,
                                report_filed_date=report_filed_date,
                                report_received_by=report_received_by,
                                report_received_date=report_received_date)
                reports.append(report)
            except Exception as e:
                logging.info(e)
            
            return [(link, report) for link, report in zip(links, reports)]
