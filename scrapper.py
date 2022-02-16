from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import urllib
import requests
import csv
from tqdm import tqdm
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as ureq
import random
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import csv
import pandas as pd

class AlliedOffsetScrapper(object):
    def __init__(self):
        self.host = "https://alliedoffsets.com/#/directory"
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "Authorization": "Bearer 8hCH4MuPCa5t6ra8wtAz8xOQfJdjLvDVZk07ib60TZ",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "carbon-registry.herokuapp.com",
            "Origin": "https://alliedoffsets.com",
            "Referer": "https://alliedoffsets.com/",
            "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
        }
        
        columns = ["Name", "Code", "CountryCode", "Description", "Methodology", "AnnualEmission", "Price", "Location"]
        
#         with open('projects.csv', 'w') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames = columns)
#             writer.writeheader()
            
    def scrape(self):
        
        countries = pd.read_csv("countries.csv")
        projects = pd.read_csv("projects.csv")
#         print(projects)
        for index, country in countries.iterrows():
            try:
                url = "https://carbon-registry.herokuapp.com/1.0/provider/search?&country="+country["code"]+"&female_focus=0&q=&max_results=12&page=1"
                r = requests.get(url, headers=self.headers)
                json = r.json()
                for data1 in json["_items"]:
                    print(data1["provider_id"])
                    if not projects.isin([data1["provider_id"]]).any().any():
                        print('Testing', projects.loc[projects.Code==data1["provider_id"]])
                        name, description, annual_emission_reduction, direct_price, methodology = self.test(data1)
                        location = self.test2(data1)
                        print("name", name, description, annual_emission_reduction, direct_price, methodology, location)
                        print("")
                        with open('projects.csv','a') as fd:
                            writer = csv.writer(fd)
                            writer.writerow([name, data1["provider_id"], country["code"], description, methodology, annual_emission_reduction, direct_price, location])

            except:
                pass

        return "All data has been Scraped"
        
        
    def get_countries(self):
        r = requests.get("https://carbon-registry.herokuapp.com/1.0/country?&max_results=2000&page=1", headers=self.headers)
        countries=[]
        items = r.json()
        items = items["_items"]
        columns = [column for column in items[0].keys()]
        for item in items:
            countries.append(item)
        with open('countries.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = columns)
            writer.writeheader()
            writer.writerows(countries)
            
    def test(self, data1):
        try:
            projectUrl="https://carbon-registry.herokuapp.com/1.0/provider/"+str(data1["provider_id"])+"?embedded={%22provider_capital_types%22:1,%22provider_capital_types.capital_type%22:1,%22provider_countries%22:1,%22provider_countries.country%22:1,%22contacts%22:1,%22contacts.office%22:1,%22provider_currencies%22:1,%22provider_currencies.currency%22:1,%22provider_languages%22:1,%22provider_languages.language%22:1,%22offices%22:1,%22offices.country%22:1,%22provider_sectors%22:1,%22provider_sectors.sector%22:1,%22provider_social_medias%22:1,%22provider_social_medias.social_media%22:1,%22provider_provider_types%22:1,%22provider_provider_types.provider_type%22:1,%22provider_stats%22:1,%22provider_stats.stat%22:1,%22provider_descriptions%22:1,%22provider_descriptions.description%22:1,%22relationships%22:1,%22relationships.description%22:1,%22provider_statuses%22:1,%22provider_statuses.status%22:1}"
            projectR = requests.get(projectUrl, headers=self.headers)
            json = projectR.json()
            name = json["name"]
            description = json["description"]
            annual_emission_reduction=""
            for data in json["provider_stats"]:
                if(data["stat"]["code"]=="est_annual_emission_redct"):

                    annual_emission_reduction = data["value"]

                if(data["stat"]["code"]=="estimated_direct_price"):
                    direct_price = data["value"]
            for data in json["provider_descriptions"]:
                # methodology=""
                if(data["description"]["code"]=="methodology"):
                    methodology = data["value"]

            return name, description, annual_emission_reduction, direct_price, methodology
        except:
            # self.test(data1)
            pass

    def test2(self, data1):
        try:
            site_url = "https://alliedoffsets.com/#/profile/"+str(data1["provider_id"])
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(site_url)
            try:


                locationElem = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/div/div/div[1]/article/div/div/div[1]/div[1]/div/div[14]/div/a'))
                )

                location = locationElem.get_attribute("href")
                print(location)
                return location

            finally:
                driver.quit()
        except:
            self.test2(data1)
        




if __name__== '__main__':
    scraper = AlliedOffsetScrapper()
#     scraper.get_countries()
    scraper.scrape()