import attr 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging.config

loginipath = '/home/jay/projects/python_projects/revised-cfs/logging_config.ini'
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')

@attr.s
class DriverConfig:

    loading_strategy = attr.ib(default='normal')
    headless = attr.ib(default=True)
    
    def get_driver(self):
        chrome_options = Options()
        capa = DesiredCapabilities.CHROME
        if self.headless is instance(bool):
            if self.headless:
                chrome_options.add_argument('--headless')
        else:
            raise TypeError
        if self.loading_strategy.lower() is 'normal' or 'none':
            capa['pageLoadStrategy'] = loading_strategy.lower()
        else:
            raise ValueError
        return webdriver.Chrome(desired_capabilities=capa, options=chrome_options)
