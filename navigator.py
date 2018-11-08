import attr
from driver_config import DriverConfig 
import logging.config
from selenium.webdriver.support.ui import WebDriverWait as WDW 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC
import time

loginipath = '/home/jay/projects/python_projects/revised-cfs/logging_config.ini'
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class SeleniumNavigator():
    loading_strategy = attr.ib(default='normal')
    driver = attr.ib(init=False)
    #waiter = attr.ib(init=False)

    def __attrs_post_init__(self):
        try:
            DC = DriverConfig(self.loading_strategy, headless=True)
            self.driver = DC.get_driver()
            #self.waiter = WDW(self.driver, 10)
        except Exception as e:
            logging.info(e)

    def click_link(self, element_id):
        self.driver.find_element_by_id(element_id).click()

    def wait_for_contributions_id(self):
        contributions_id = 'ctl00_ContentPlaceHolder1_Name_Reports1_dgReports_ctl02_ViewCont'
        WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, contributions_id)))
        WDW(self.driver, 10).until(EC.element_to_be_clickable((By.ID, contributions_id)))
        logging.info('Link is clickable.')

    def wait_for_csv_link(self):
        link_id = "ctl00_ContentPlaceHolder1_Campaign_ByContributions_RFResults2_Export"
        WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, link_id)))
        WDW(self.driver, 10).until(EC.element_to_be_clickable((By.ID, link_id)))

    def expose_dropdown(self, element_id):
        WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, element_id)))
        self.click_link(element_id)

    def click_dropdown_initial(self):
        element_id = 'ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_Panel8'
        table_id = 'ctl00_ContentPlaceHolder1_Name_Reports1_TabContainer1_TabPanel1_dgReports'
        try:
            #AC(self.driver).move_to_element(element).click().perform()
            #time.sleep(2) 
            while True:
                self.driver.find_element_by_id(element_id).click()
                time.sleep(1)
                element = self.driver.find_element_by_id(table_id)
                if element.is_displayed():
                    time.sleep(1)
                    break
            logging.info('Dropdown clicked')
        except Exception as e:
            logging.info('Element cannot be clicked.')
            logging.info(e)

    def click_dropdown_subsequent(self):
        self.click_dropdown_initial()
        #self.click_link(element_id)

    def get_current_url(self):
        return self.driver.current_url 

    def page_source(self):
        return self.driver.page_source 
    
    def navigate(self, url):
        self.driver.get(url)

    def back(self):
        self.driver.back()

    def close_browser(self):
        self.driver.quit()
