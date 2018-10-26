import attr
from driver_config import DriverConfig 
import logging.config
from selenium.webdriver.support.ui import WebDriverWait as WDW 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

loginipath = '/home/jay/projects/python_projects/revised-cfs/logging_config.ini'
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class SeleniumNavigator():
    loading_strategy = attr.ib(default='normal')
    driver = attr.ib(init=False)
    waiter = attr.ib(init=False)

    def __attrs_post_init__(self):
        try:
            DC = DriverConfig(self.loading_strategy)
            self.driver = DC.get_driver()
            self.waiter = WDW(self.driver, 10)
            logging.info('driver and waiter initialized')
        except Exception as e:
            logging.info(e)

    def click_link(self, element_id):
        self.driver.find_element_by_id(element_id).click()

    def expose_dropdown(self, element_id):
        self.waiter.until(EC.presence_of_element_located((By.ID, element_id)))
        self.click_link(element_id)

    def click_dropdown_initial(self, element_id):
        self.waiter.until(EC.presence_of_element_located((By.ID, element_id)))
        self.waiter.until(EC.visibility_of_element_located((By.ID, element_id)))
        element = self.waiter.until(EC.element_to_be_clickable((By.ID, element_id)))
        element.click()

    def click_dropdown_subsequent(self, element_id):
        self.click_dropdown_initial(element_id)
        self.click_link(element_id)

    def navigate(self, url):
        self.driver.get(url)

    def back(self):
        self.driver.back()
