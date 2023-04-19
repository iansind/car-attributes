from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
import random
import pandas as pd
import numpy as np

# Initial installation of driver.
'''from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))'''

with open('make_models.pkl', 'rb') as f:
    loaded = pickle.load(f)

# Flattens the list of lists of tuples into a single list of tuples.
squashed = [model for make in loaded for model in make]

# Global dataframe to collect individual car attributes.
all_cars = pd.DataFrame()

driver = webdriver.Chrome()
# Waits if a target to click isn't yet available.
driver.implicitly_wait(3)


# Scrapes the given webpage and adds the attributes to the master dictionary.
def scrape_stats(page, make, model):
    attrs = {'make': [make], 'model': [model]}
    attrs['year'] = page.find_element(By.XPATH, '//*[@id="yearSelect"]/option[2]').text
    attrs['price'] = page.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div[3]/div[2]/div[2]').text
    attrs = pd.DataFrame.from_dict(attrs)
    global all_cars
    all_cars = pd.concat([all_cars, attrs])
    return None


# Get a list of the possible styles/configurations.
def get_styles(page):
    page.find_element(By.XPATH, '//*[@id="styleSelect"]').click()
    style_dropdown = driver.find_element(By.XPATH, '//*[@id="styleSelect"]')
    time.sleep(1)
    styles = [style.text for style in style_dropdown.find_elements(By.TAG_NAME, 'option')]
    styles.pop(0)
    return styles


# Get a list of the possible trims.
def get_trims(page):
    page.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
    time.sleep(1)
    trim_dropdown = page.find_element(By.XPATH, '//*[@id="trimSelect"]')
    trims = [trim.text for trim in trim_dropdown.find_elements(By.TAG_NAME, 'option')]
    trims.pop(0)
    return trims


for make_model in squashed[:4]:
    make = make_model[0]
    model = make_model[1]
    url = 'https://www.caranddriver.com/' + make + '/' + model + '/specs'
    driver.get(url)
    curr_trims = get_trims(driver)
    curr_styles = get_styles(driver)
    scrape_stats(driver, make, model)

    if len(curr_trims) > 1:
        driver.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
        for i in range(3, len(curr_trims) + 2):
            driver.find_element(By.XPATH, '//*[@id="trimSelect"]').click()

            path = '//*[@id="trimSelect"]/option[' + str(i) + ']'
            driver.find_element(By.XPATH, path).click()
            time.sleep(2)

            scrape_stats(driver, make, model)





    print(curr_styles, curr_trims)
    time.sleep(random.uniform(10.5, 12.6))

    # Get page info
    # Go through the trims and get page info
    # Move onto the next style
    # Get page info
    # Move through the trims



'''driver.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
time.sleep(1)
trim_dropdown = driver.find_element(By.XPATH, '//*[@id="trimSelect"]')
trims = [trim.text for trim in trim_dropdown.find_elements(By.TAG_NAME, 'option')]'''
#trims.pop(0)
#trims.sort()
#print(trims)

print(all_cars)



# Do this if more than one trim level.

'''
driver.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
for i in range(3, len(trims)+1):
    driver.find_element(By.XPATH, '//*[@id="trimSelect"]').click()

    path = '//*[@id="trimSelect"]/option[' + str(i) + ']'
    driver.find_element(By.XPATH, path).click()
    time.sleep(random.uniform(1.5, 2.6))
    # run def to scrape page
    '''

# //*[@id="main-content"]/div[3]/div/div[5]
# //*[@id="main-content"]/div[3]/div/div[6]
# //*[@id="main-content"]/div[3]/div/div[6]/h3/button




'''driver = webdriver.Chrome()
driver.get('https://www.caranddriver.com/')
# Waits if a target to click isn't yet available.
driver.implicitly_wait(3)

# Sleeps are important to allow for dropdown fields to load.
# Clicks on the 'Makes and Models' button to make the dropdown available.
driver.find_element(By.XPATH, '//*[@id="__next"]/div/nav/div[1]/div[1]/button').click()
time.sleep(2)
# Clicks on the 'Make' dropdown to populate options of car makes.
driver.find_element(By.XPATH, '//*[@id="modal-root"]/div[2]/div/div[2]/select').click()
time.sleep(2)
# Obtains the populated 'Make' element and converts to a list.
dropdown1 = driver.find_element(By.XPATH, '//*[@id="modal-root"]/div[2]/div/div[2]/select')
makes = [make.get_attribute('value') for make in dropdown1.find_elements(By.TAG_NAME, 'option')]

# Generates list of tuples in the form (make, model) for each available combination.
# Iterates over each make to populate its associated models.
makes_models = []
for i in range(2, len(makes)+1):
    # Generation of element location.
    path = '//*[@id="modal-root"]/div[2]/div/div[2]/select/option[' + str(i) + ']'
    driver.find_element(By.XPATH, path).click()
    time.sleep(2)

    # Performs formatting that will be necessary when generating URLs.
    dropdown2 = driver.find_element(By.XPATH, '//*[@id="modal-root"]/div[2]/div/div[3]/select')
    curr_models = [(makes[i-1], model.get_attribute('value').replace(' ', '-').lower()) for model in
                   dropdown2.find_elements(By.TAG_NAME, 'option') if model.get_attribute('value') != '0']
    makes_models.append(curr_models)

# Count to ensure values were not dropped. Compare to repeated valued for consistency.
s = 0
for make in makes_models:
    print(make)
    s += len(make)'''

