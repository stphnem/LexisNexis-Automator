__author__ = 'Stephen Em'

import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LNAutomator:

    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.maximize_window()
        self.driver.get('http://www.lexisnexis.com/hottopics/lnacademic/')

    def search(self, text):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it( (By.ID, "mainFrame") )
            )
            self.driver.find_element_by_id('terms').send_keys(text)
            searchBtn = self.driver.find_element_by_id("srchButt").click()
        finally:
            print 'Done searching for', text

    def switch_to_main_frame(self):
        element = WebDriverWait(self.driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it( (By.ID, "mainFrame") )
            )

    def switch_to_results_frame(self):
        contentFrame = self.driver.find_element_by_css_selector("frame[title='Results Content Frame']")
        self.contentFrameName = contentFrame.get_attribute('name')
        print 'Switching to content frame', self.contentFrameName

        element = WebDriverWait(self.driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it( (By.NAME, self.contentFrameName) )
        )

    def switch_to_nav_frame(self):
        self.navFrameName = self.contentFrameName.replace("Content", "Nav")
        self.driver.switch_to.parent_frame()
        print 'Switching to nav frame', self.navFrameName
        element = WebDriverWait(self.driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it( (By.NAME, self.navFrameName) )
        )

    def check_all_results(self):
        print "Clicking checkbox"
        checkbox = self.driver.find_element_by_id("frm_control_box")
        checkbox.click()

    def click_download_doc(self):
        print "Clicking floppy disk download"
        downloadBtn = self.driver.find_element_by_css_selector('img[alt="Download Documents"]')
        downloadBtn.click()

    def store_parent_window(self):
        self.parentWindow = self.driver.current_window_handle

    def select_parent_window(self):
        print "Switching to parent window", self.parentWindow
        self.driver.switch_to.window(self.parentWindow);

    def switch_to_popup(self):
        handles = self.driver.window_handles;
        for handle in handles:
            self.subWindowHandler = handle

        print "Switching to popup", self.subWindowHandler
        self.driver.switch_to.window(self.subWindowHandler)

    def switch_to_content_from_popup(self):
        print "Switchin to main frame"
        element = WebDriverWait(self.driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it( (By.ID, "mainFrame") )
        )
        element = WebDriverWait(self.driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it( (By.NAME, self.contentFrameName) )
        )

    def next_page_exists(self):
        return self.driver.find_elements(By.CSS_SELECTOR, 'img[alt="View next document"]') > 0;

    def select_text_download(self):
        mySelect = Select(self.driver.find_element_by_css_selector('#delFmt'))
        mySelect.select_by_index(3)

    def click_download(self):
        downloadBtn = self.driver.find_element_by_css_selector('img[alt="Download"]')
        downloadBtn.click()

    def click_download_link(self):
        WebDriverWait(self.driver, 10).until(
            EC.title_contains('Download Documents')
        )
        downloadLink = self.driver.find_element_by_xpath('//*[@id="center"]/center/p/a')
        downloadLink.click()

    def close_window(self):
        closeBtn = self.driver.find_element_by_css_selector('img[alt="Close Window"]')
        closeBtn.click()

    def click_next_page(self):
        nextPage = self.driver.find_element(By.CSS_SELECTOR, 'img[alt="View next document"]')
        nextPage.click();

if __name__ == "__main__":
    LNAutomator = LNAutomator()
    LNAutomator.search("gun control")
    LNAutomator.switch_to_results_frame()
    LNAutomator.check_all_results()
    LNAutomator.switch_to_nav_frame()
    LNAutomator.click_download_doc()
    LNAutomator.store_parent_window()
    LNAutomator.switch_to_popup()
    LNAutomator.select_text_download()
    LNAutomator.click_download()
    LNAutomator.click_download_link()
    LNAutomator.close_window()
    LNAutomator.select_parent_window()
    LNAutomator.switch_to_content_from_popup()
    LNAutomator.check_all_results()
    LNAutomator.switch_to_nav_frame()
    while (LNAutomator.next_page_exists()):
        LNAutomator.click_next_page()
        LNAutomator.switch_to_main_frame()
        LNAutomator.switch_to_results_frame()
        LNAutomator.check_all_results()
        LNAutomator.switch_to_nav_frame()
        LNAutomator.click_download_doc()
        LNAutomator.store_parent_window()
        LNAutomator.switch_to_popup()
        LNAutomator.select_text_download()
        LNAutomator.click_download()
        LNAutomator.click_download_link()
        LNAutomator.close_window()
        LNAutomator.select_parent_window()
        LNAutomator.switch_to_content_from_popup()
        LNAutomator.check_all_results()
        LNAutomator.switch_to_nav_frame()