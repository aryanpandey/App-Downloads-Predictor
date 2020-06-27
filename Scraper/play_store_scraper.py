# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

['NEW_FREE','NEW_PAID', 'TOP_FREE', 'TOP_PAID',
            'TOP_GROSSING', 'TRENDING']
['ANDROID_WEAR', 'ART_AND_DESIGN']

,'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
's','t','u','v','w','x','y','z'
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import time

url = 'https://play.google.com'

driver = webdriver.Chrome(executable_path = r'C:/Projects/App-Downloads-Predictor/Scraper/chromedriver.exe')

driver.implicitly_wait(2)
driver.maximize_window()
driver.get(url +'/store/apps')
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
           's','t','u','v','w','x','y','z']
hrefs =[]
for i in letters:
    driver.find_element_by_name('q').send_keys(Keys.BACKSPACE)
    time.sleep(0.5)
    driver.find_element_by_name('q').send_keys(i)
    time.sleep(1)
    driver.find_element_by_class_name('gbqfb').click()
    time.sleep(2.5)
    app = driver.find_elements_by_class_name('poRVub')
    for j in range(len(app)):
        hrefs.append(app[j].get_attribute('href'))

app_data = pd.DataFrame()
print(len(np.unique(np.asarray(hrefs))))
print('test')
c = 0
links = np.unique(np.asarray(hrefs))
for i in links:
    driver.get(i)
    time.sleep(0.5)
    
    print('{}\r '.format(c), end = "")
    c = c + 1
    
    try:
        rating = driver.find_element_by_class_name('BHMmbe').text
    except:
        rating = -1
    try:
        Number_reviews = driver.find_element_by_class_name('EymY4b').text
    except:
        Number_reviews = 0
    try:
        App_Name = driver.find_element_by_class_name('AHFaub').text
    except:
        App_Name = 'No Name'
    try:
        genre = driver.find_element_by_class_name('qQKdcc').text
    except:
        genre = 'Not Specified'
    
    details_topics = driver.find_elements_by_class_name('BgcNfc')
    details_values = driver.find_elements_by_class_name('htlgb')
    
    detail_dict = {}
    for i in range(len(details_topics)):
        detail_dict[details_topics[i].text] = details_values[2*i].text
    
    try:
        last_update = detail_dict['Updated']
    except:
        last_update = 'No Update'
        
    try:
        size = detail_dict['Size']
    except:
        size = -1
    
    try:
        Installs = detail_dict['Installs']
    except:
        Installs = -1
    
    try:
        version = detail_dict['Current Version']
    except:
        version = 'Not Given'
    
    try:
        android = detail_dict['Requires Android']
    except:
        android = 'Any version'
    
    try:
        Age = detail_dict['Content Rating']
    except:
        Age = 'Any Rating'
    
    try:
        Elements = detail_dict['Interactive Elements']
    except:
        Elements = 'No Interactive Elements'
    
    try:
        Purchases = detail_dict['In-app Products']
    except:
        Purchases = 'Completely free'
    
    try:
        Offered_by = detail_dict['Offered By']
    except:
        Offered_by = 'Not given'
        
    try:
        developer = detail_dict['Developer']
    except:
        developer = 'Not Specified'
        
    entry = {'App Name':App_Name, 'Last Update':last_update, 'Size':size, 'Genre':genre, 
             'Number of Installations':Installs, 'Version':version,
             'Required Android Version':android, 'Minimum Age':Age,
             'Interactive Elements':Elements, 'In-app Purchases': Purchases,
             'Offered By':Offered_by, 'Developer':developer,
             'Rating':rating, 'Number of Reviews': Number_reviews}
    
    entry = pd.Series(entry)
    app_data = app_data.append(entry, ignore_index = True)
    
    time.sleep(1.5)
    
app_data.to_csv('play_store_data.csv', index = False)
