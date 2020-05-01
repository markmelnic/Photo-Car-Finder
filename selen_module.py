
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests
import random
import time
import os
import re 


GENERIC_URL = 'https://yandex.ru/images/'

maindir = os.getcwd()

# ================== driver boot procedure
def boot():
    # manage notifications
    opts = Options() 
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    #opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--window-size=1920,1080")
    #opts.set_headless(headless=True)
    opts.add_argument("--disable-gpu")

    dv = webdriver.Chrome(chrome_options = opts, executable_path = r"./chromedriver.exe")

    return dv


# ================== kill the driver
def killd(dv):
    dv.quit()
    
    
# ================== check for cyrilic characters
def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


# ================== website processes
def finder(dv, photo):
    dv.get(GENERIC_URL)
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    
    # upload photo
    dv.find_element_by_xpath("/html/body/div[1]/div/div[1]/header/div/div[1]/div[2]/form/div[1]/span/span/span[2]").click()
    # input file location in local system
    dv.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/form[1]/input").send_keys(maindir + "\\photos" + "\\" + photo)
    time.sleep(5)
    currentURL = dv.current_url

    # bs4
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(currentURL, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # get first title out of all suggestions
    carTitles = soup.find_all(class_ = "Button2-Text")
    for i in range(2):
        carTitles.pop(-1)
    titles = []
    for title in carTitles:
        title = title.get_text()
        if has_cyrillic(title) == False:
            titles.append(title)
    
    return titles