from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import time
import pandas as pd
import urllib.parse
from MainClass import *

browser = webdriver.Firefox()
# telecom="http://odp.org/Business/Telecommunications"
finance="http://odp.org/Business/Financial_Services"
browser.get(finance)
time.sleep(3)
subcategories=browser.find_element_by_id("triple").find_elements_by_tag_name("a")
subcats=[]
hostname=urllib.parse.urlparse(finance).hostname
TBS=TheBigScrape()
for i in subcategories:
    subcats.append(i.get_attribute("href"))

for sub in subcats[:5]:
    browser.get(sub)
    time.sleep(2)
    various_links=browser.find_elements_by_css_selector("li.listings a")
    for link in various_links:

        TBS.StoreUrl(link.get_attribute("href"))
        print("Okay Stored the url",link.get_attribute("href"))
        TBS.FetchRssList()
        if TBS.RssCount>0:
            print("This one is having feeds it seems")
            TBS.FetchRssData()
    print("one more category done")
    print(len(TBS.DataDict["title"]))

df=pd.DataFrame(TBS.DataDict)
df["label"]="finance"

df.to_csv("test2.csv",index=False)
browser.close()
    
            
    


