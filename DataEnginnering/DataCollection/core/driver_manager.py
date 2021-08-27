from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class DriverManager:

    driver = None
    c = None
    soup = None

    def __init__(self, adult_accept=True):
        options = Options()
        options.headless = True
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("--disable-popup-blocking")
        self.driver = webdriver.Chrome("C:/Users/Cesar/Documents/Apuestas/chromedriver.exe")

        if adult_accept: self.version_18()

    def version_18(self):
        self.get("https://mismarcadores.com",1.3)
        self.driver.find_elements_by_class_name("button___1wCBhNg")[0].click()
        time.sleep(1.5)
        self.driver.find_elements_by_class_name("confirmationButton___38WagOL")[0].click()

    def click_button_by_id(self, button_id):
        try:
            button = self.driver.find_element_by_id(button_id)
            if button:
                button.click()
                time.sleep(1.5)
        except: pass

    def get(self, url, wait_seconds=2):
        self.driver.get(url)
        time.sleep(wait_seconds)

        self.c = self.driver.page_source
        self.soup = BeautifulSoup(self.c, "html.parser")

    def quit(self):
        self.driver.quit()
        self.driver = None
        self.c = None
        self.soup = None

