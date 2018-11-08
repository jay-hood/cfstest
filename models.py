from sqlalchemy import Table, Column, String, Integer, ForeignKey, DateTime, create_engine 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base 

Base = declarative_base()


class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(45))
    middlename = Column(String(45))
    lastname = Column(String(45))
    offices = relationship('Office')

class Office(Base):
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    filer_id = Column(String(45))
    office_sought = Column(String(45))
    dropdown_link = Column(String(45))
    status = Column(String(45))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    reports = relationship('Report')

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    report_type = Column(String(45))
    year = Column(Integer)
    report_filed_date = Column(String(45))
    report_received_by = Column(String(45))
    report_received_date = Column(String(45))
    office_id = Column(Integer, ForeignKey('offices.id'))
    url = Column(String(200))

class ScrapeLog(Base):
    __tablename__ = 'scrapelogs'
    id = Column(Integer, primary_key=True)
    scrape_date = Column(DateTime)
    process_date = Column(DateTime)
    raw_data = Column(String(2147483647))
    page_url = Column(String(200))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    report_id = Column(Integer, ForeignKey('reports.id'))


if __name__ == '__main__':
    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)
