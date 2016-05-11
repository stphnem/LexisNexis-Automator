__author__ = 'Stephen Em'

import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LNAutomator:
    """LexisNexis search object to automate downloads from query
    
    [description]
    
    Public Methods:
        __author__  -- Stephen Em
        LNAutomator.__init__() -- Opens Chrome browser with LexisNexis Academic 
                                  Search Page
        LNAutomator.search() {[str]} -- Takes search query and performs search
        LNAutomator.download_all_docs() {[type]} -- Downloads the page of 
            documents until results are exhausted
    """

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

    def download_all_docs(self):
        self._download_page_of_docs()
        while (self._next_page_exists()):
            self._click_next_page()
            self._switch_to_main_frame()
            self._download_page_of_docs()

    def _download_page_of_docs(self):
        """Downloads 25 documents of current page
        
        Performs the automation steps to download a page of documents as listed 
        in the documenation. Refer to documentation for sequence of steps.
        """
        self._switch_to_results_frame()
        self._check_all_results()
        self._switch_to_nav_frame()
        self._click_download_doc()
        self._store_parent_window()
        self._switch_to_popup()
        self._select_text_download()
        self._click_download()
        self._click_download_link()
        self._close_window()
        self._select_parent_window()
        self._switch_to_content_from_popup()
        self._check_all_results()
        self._switch_to_nav_frame()

    def _switch_to_main_frame(self):
        """Switch to main iFrame that holds all other frames
        """
        element = WebDriverWait(self.driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it( (By.ID, "mainFrame") )
            )

    def _switch_to_results_frame(self):
        """Switch to results frame where search results are held
        
        Attempt to find the results frame and switch for 20 seconds. If found
        before 20 seconds, fra,e will switch context to results frame.
        """
        contentFrame = self.driver.find_element_by_css_selector("frame[title='Results Content Frame']")
        self.contentFrameName = contentFrame.get_attribute('name')
        print 'Switching to content frame', self.contentFrameName

        element = WebDriverWait(self.driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it( (By.NAME, self.contentFrameName) )
        )

    def _switch_to_nav_frame(self):
        """Switch to nav frame where download doc link is placed
        
        Attempt to find the nav frame and switch for 20 seconds. If found
        before 20 seconds, fra,e will switch context to nav frame.
        """
        self.navFrameName = self.contentFrameName.replace("Content", "Nav")
        self.driver.switch_to.parent_frame()
        print 'Switching to nav frame', self.navFrameName
        element = WebDriverWait(self.driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it( (By.NAME, self.navFrameName) )
        )

    def _check_all_results(self):
        """Click checkbox located in nav frame to select all search results
        """
        print "Clicking checkbox"
        checkbox = self.driver.find_element_by_id("frm_control_box")
        checkbox.click()

    def _click_download_doc(self):
        """Click floppy disk icon to download documents located in the nav frame
        """
        print "Clicking floppy disk download"
        downloadBtn = self.driver.find_element_by_css_selector('img[alt="Download Documents"]')
        downloadBtn.click()

    def _store_parent_window(self):
        self.parentWindow = self.driver.current_window_handle

    def _select_parent_window(self):
        print "Switching to parent window", self.parentWindow
        self.driver.switch_to.window(self.parentWindow);

    def _switch_to_popup(self):
        """Switch to popup window triggered when flopp disk icon is clicked
        
        Switch between window handles to find popup window and switch to popup
        """
        handles = self.driver.window_handles;
        for handle in handles:
            self.subWindowHandler = handle

        print "Switching to popup", self.subWindowHandler
        self.driver.switch_to.window(self.subWindowHandler)

    def _switch_to_content_from_popup(self):
        """Switch back to mainframe after ending popup
        
        After popup is closed, must switch back to mainframe and content frame
        """
        print "Switching to main frame"
        element = WebDriverWait(self.driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it( (By.ID, "mainFrame") )
        )
        element = WebDriverWait(self.driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it( (By.NAME, self.contentFrameName) )
        )

    def _next_page_exists(self):
        """Check if more pages of search results exist
        
        Check if the arrow for next page is present to find if next page exists
        
        Returns:
            [int] -- 0 if no next page, 1 otherwise
        """
        return self.driver.find_elements(By.CSS_SELECTOR, 'img[alt="View next document"]') > 0;

    def _select_text_download(self):
        """Select text format to download"
        
        Get dropdown element and select index/option 3 which corresponds to text
        """
        mySelect = Select(self.driver.find_element_by_css_selector('#delFmt'))
        mySelect.select_by_index(3)

    def _click_download(self):
        downloadBtn = self.driver.find_element_by_css_selector('img[alt="Download"]')
        downloadBtn.click()

    def _click_download_link(self):
        """Click download link in popup window
        """

        WebDriverWait(self.driver, 10).until(
            EC.title_contains('Download Documents')
        )
        downloadLink = self.driver.find_element_by_xpath('//*[@id="center"]/center/p/a')
        downloadLink.click()

    def _close_window(self):
        """Close popup window
        """
        closeBtn = self.driver.find_element_by_css_selector('img[alt="Close Window"]')
        closeBtn.click()

    def _click_next_page(self):
        """Click next page button located on nav frame
        """
        nextPage = self.driver.find_element(By.CSS_SELECTOR, 'img[alt="View next document"]')
        nextPage.click();