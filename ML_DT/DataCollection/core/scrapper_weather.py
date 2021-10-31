import time

from DataCollection.core.driver_manager import DriverManager
import logging

class ScrapperWeather:

    def __init__(self):
        self.driverManager = DriverManager(adult_accept=False)
        self.logger = logging.getLogger("logs").getChild(__name__)

    def get_weather_data_historical(self, place_weather, date_match, time_match):
        url = f"https://www.worldweatheronline.com/{place_weather.replace('weather/', 'weather-history/')}" if \
            "history" not in place_weather else f"https://www.worldweatheronline.com/{place_weather}"

        self.driverManager.get(url, 1)

        year = date_match.split('-')[0]
        month = date_match.split('-')[1].split('-')[0]
        day = date_match.split('-')[2]

        self.driverManager.driver.find_element_by_id("ctl00_MainContentHolder_txtPastDate").send_keys(f"{month}-{day}-{year}")
        self.driverManager.click_button_by_id("ctl00_MainContentHolder_butShowPastWeather")
        time.sleep(1)

        hour = round(int(time_match.split(":")[0])*1.0/3, 0)
        init_count=14
        id_row = init_count+12*hour

        weather_info = self.driverManager.driver\
                .find_elements_by_xpath(f'//*[@id="aspnetForm"]/div[4]/main/div[4]/div[1]/div[3]/div/div[1]/div/div[2]/div/div[{id_row}]/img')[0].get_attribute("title")
        
        temperature = self.driverManager.driver\
                .find_elements_by_xpath(f'//*[@id="aspnetForm"]/div[4]/main/div[4]/div[1]/div[3]/div/div[1]/div/div[2]/div/div[{id_row+1}]')[0].text\
                    .replace(' °c','')

        wind = self.driverManager.driver\
                .find_elements_by_xpath(f'//*[@id="aspnetForm"]/div[4]/main/div[4]/div[1]/div[3]/div/div[1]/div/div[2]/div/div[{id_row+3}]')[0].text\
                    .split(' ')[0]
        
        rain = self.driverManager.driver\
                .find_elements_by_xpath(f'//*[@id="aspnetForm"]/div[4]/main/div[4]/div[1]/div[3]/div/div[1]/div/div[2]/div/div[{id_row+5}]')[0].text\
                    .split(' ')[0]
        
        humidity = self.driverManager.driver\
                .find_elements_by_xpath(f'//*[@id="aspnetForm"]/div[4]/main/div[4]/div[1]/div[3]/div/div[1]/div/div[2]/div/div[{id_row+6}]')[0].text\
                    .replace('%','')
        
        cloudy = self.driverManager.driver\
                .find_elements_by_xpath(f'//*[@id="aspnetForm"]/div[4]/main/div[4]/div[1]/div[3]/div/div[1]/div/div[2]/div/div[{id_row+7}]')[0].text\
                    .replace('%','')
        
        return weather_info, temperature, wind, rain, humidity, cloudy