from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import shutil
import time
import os

def getResponse():
    initPath='PATH_TO_DOWNLOAD'

    options = webdriver.ChromeOptions() 
    p = {'download.default_directory':initPath}
    options.add_experimental_option('prefs', p)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.get('https://login.fmls.com/samlsp?redirectUrl=https://www.fmls.com/memberhome')

    user_selector = driver.find_element_by_id("loginId")
    user_selector.send_keys('USERNAME')

    pass_selector = driver.find_element_by_id("password")
    pass_selector.send_keys('PWD')

    login_btn = driver.find_element_by_id('btn-login')
    login_btn.click()
    time.sleep(5)
    driver.get('https://matrix.fmlsd.mlsmatrix.com')
    
    eplus_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='TITLE'")))
    eplus_link.click()

    select_all = driver.find_element_by_css_selector('[title^="Check"]')
    select_all.click()

    export = driver.find_element_by_css_selector('.icon_export')
    export.click()

    dropdown = Select(driver.find_element_by_css_selector('#m_ddExport'))

    dropdown.select_by_value('ug41347')
    driver.find_element_by_css_selector('#m_tdExport').click()

    time.sleep(5)
    driver.quit()

    filename = max([initPath + "\\" + f for f in os.listdir(initPath)],key=os.path.getctime)
    shutil.move(filename,os.path.join(initPath,r"fmls.csv"))
    
    df = pd.read_csv('fmls.csv')
    os.remove(initPath + '\\fmls.csv')

    return df
