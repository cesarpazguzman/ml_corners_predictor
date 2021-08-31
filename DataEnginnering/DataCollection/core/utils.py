from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument('--blink-settings=imagesEnabled=false')

def getNumber(_string: str) -> int:
    try:
        return int(_string)
    except:
        return 90