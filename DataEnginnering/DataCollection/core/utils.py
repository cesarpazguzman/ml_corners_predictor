from selenium.webdriver.chrome.options import Options

options = Options()
#options.headless = True
#options.add_argument('--blink-settings=imagesEnabled=false')

def check_exists_by_xpath(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath).text
    except:
        return False

def getNumber(_string):
    try:
        return int(_string)
    except:
        return 90