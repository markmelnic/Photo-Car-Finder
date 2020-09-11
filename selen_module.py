
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests, time, re

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
GENERIC_URL = 'https://yandex.ru/images/'

def boot():
    # manage notifications
    opts = Options() 
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    #opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--window-size=1920,1080")
    #opts.set_headless(headless=True)
    opts.add_argument("--disable-gpu")
    
    dv = webdriver.Chrome(chrome_options = opts, executable_path = r"./chromedriver.exe")
    dv.minimize_window()
    
    return dv

def boot_u(car):
    # manage notifications
    opts = Options() 
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    #opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--window-size=1920,1080")
    #opts.set_headless(headless=True)
    opts.add_argument("--disable-gpu")

    dv = webdriver.Chrome(chrome_options = opts, executable_path = r"./chromedriver.exe")
    dv.maximize_window()

    dv.get("https://google.com")  
    time.sleep(1)
    searchField = dv.find_element_by_name("q")

    for ch in car:
        searchField.send_keys(ch)

    searchField.send_keys(Keys.ENTER)
    time.sleep(60)

def killd(dv):
    dv.quit()

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def finder(dv, photo):
    dv.get(GENERIC_URL)
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)

    # upload photo
    dv.find_element_by_xpath("/html/body/div[1]/div/div[1]/header/div/div[1]/div[2]/form/div[1]/span/span/span[2]").click()
    # input file location in local system
    dv.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/form[1]/input").send_keys(maindir + "\\photos" + "\\" + photo)
    time.sleep(5)

    # bs4
    response = requests.get(dv.current_url, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # get first title out of all suggestions
    car_titles = soup.find_all(class_ = "Button2-Text")[:len(car_titles)-2]
    titles = [title for title in car_titles if has_cyrillic(title) == False]

    return titles
