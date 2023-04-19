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
def scrape_stats(page, make, model, style, trim):
    #attrs = {'make': [make], 'model': [model], 'style': [style], 'trim': [trim]}
    attrs = {'style': [style], 'trim': [trim]}
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
    time.sleep(2)
    styles = [style.text for style in style_dropdown.find_elements(By.TAG_NAME, 'option')]
    styles.pop(0)
    page.find_element(By.XPATH, '//*[@id="styleSelect"]').click()
    return styles


# Get a list of the possible trims.
def get_trims(page):
    page.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
    time.sleep(2)
    trim_dropdown = page.find_element(By.XPATH, '//*[@id="trimSelect"]')
    trims = [trim.text for trim in trim_dropdown.find_elements(By.TAG_NAME, 'option')]
    trims.pop(0)
    page.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
    return trims


def new_style_init(page, make, model, curr_style):
    curr_trims = get_trims(page)
    scrape_stats(page, make, model, curr_style, curr_trims.pop(0))

    if len(curr_trims) > 0:
        i = 3
        while len(curr_trims) > 0:
            page.find_element(By.XPATH, '//*[@id="trimSelect"]').click()

            path = '//*[@id="trimSelect"]/option[' + str(i) + ']'
            page.find_element(By.XPATH, path).click()
            time.sleep(2)

            scrape_stats(page, make, model, curr_style, curr_trims.pop(0))

            time.sleep(random.uniform(8.5, 9.6))

            i += 1


for make_model in squashed[2:3]:
    make = make_model[0]
    model = make_model[1]
    url = 'https://www.caranddriver.com/' + make + '/' + model + '/specs'
    driver.get(url)

    curr_styles = get_styles(driver)
    curr_style = curr_styles.pop(0)

    new_style_init(driver, make, model, curr_style)

    time.sleep(random.uniform(8.5, 9.6))

    if len(curr_styles) > 0:
        i = 3
        while len(curr_styles) > 0:
            driver.find_element(By.XPATH, '//*[@id="styleSelect"]').click()

            path = '//*[@id="styleSelect"]/option[' + str(i) + ']'
            driver.find_element(By.XPATH, path).click()
            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
            driver.find_element(By.XPATH, '//*[@id="trimSelect"]/option[2]').click()

            new_style_init(driver, make, model, curr_styles.pop(0))

            i += 1


print(all_cars)

# Pickles the dataframe.
with open('all_cars.pkl', 'wb') as f:
    pickle.dump(all_cars, f)

with open('all_cars.pkl', 'rb') as f:
    loaded_df = pickle.load(f)

# Checks the integrity of the saved file.
integrity = '' if loaded_df == all_cars else 'not '
print(f'The saved file is {integrity}valid.')
