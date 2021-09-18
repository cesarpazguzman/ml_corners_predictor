from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from DataCollection.properties import properties


class DriverManager:

    def __init__(self, adult_accept=True, headless=True):
        options = Options()
        options.headless = headless
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("--disable-popup-blocking")
        self.driver = webdriver.Chrome(properties.path_exec_chrome, options=options)

        if adult_accept:
            self.version_18()

    def version_18(self):
        self.get("https://mismarcadores.com",1.3)
        self.driver.find_elements_by_class_name("button___1wCBhNg")[0].click()
        time.sleep(1.5)
        self.driver.find_elements_by_class_name("confirmationButton___38WagOL")[0].click()

    def click_button_by_id(self, button_id: str) -> bool:
        try:
            button = self.driver.find_element_by_id(button_id)
            button.click()
            time.sleep(1.5)
            return True
        except Exception as ex:
            print("Some wrong has happened -> {0}".format(ex))
            return False

    def click_button_by_class(self, class_name: str) -> bool:
        try:
            button = self.driver.find_element_by_class_name(class_name)
            button.click()
            time.sleep(1.5)
            return True
        except Exception as ex:
            print("Some wrong has happened -> {0}".format(ex))
            return False

    def get(self, url: str, wait_seconds: int = 2):
        self.driver.get(url)
        time.sleep(wait_seconds)

        self.c = self.driver.page_source
        self.soup = BeautifulSoup(self.c, "html.parser")

    def quit(self):
        self.driver.quit()
        self.driver = None
        self.c = ""
        self.soup = ""

    def check_exists_by_xpath(self, driver: webdriver, xpath: str) -> str:
        try:
            return driver.find_element_by_xpath(xpath).text
        except NoSuchElementException:
            return ""

    def click_path(self, driver: webdriver, xpath: str) -> bool:
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            time.sleep(5)
            return True
        except:
            return False

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

    def find_elem(self, driver: webdriver, tag_name: str, class_name:str,
                  feature_name:str, index: int = -1) -> webdriver:
        try:
            elem: list = driver.find_all(tag_name, {"class": class_name})
            return elem if index == -1 else elem[index]
        except Exception as ex:
            print("Error scrapping the feature {0} - {1}".format(feature_name, ex))
            return None
