from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pickle
import random
import pandas as pd
import numpy as np

'''
Using a previously generated list of makes and models, this program scrapes caranddriver.com for vehicle specs. 
A crawler delay of 10 seconds is requested, so various delays have been added to ensure at least 10 seconds are spent 
on a page before loading a new one. 
The program returns a dataframe of cars with a large number of attributes.
As the expected runtime of this program given nearly 900 makes and models is many hours, it is suggested to run slices 
of the list at a time to obtain many individual dataframes that can later be concatenated. 
'''

# Initial installation of driver.
'''
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
'''

'''
Previously-generated list of makes and models, in the format of a list of models for each make in a list of makes. 
Each individual list element is a tuple consisting of make and model. 
'''
with open('make_models.pkl', 'rb') as f:
    loaded = pickle.load(f)

# Flattens the list of lists of tuples into a single list of tuples.
squashed = [model for make in loaded for model in make]

'''
Global dataframe to collect individual car attributes. A dataframe is used here to maintain proper ordering and 
better handle missing or inconsistent attributes. The speed at which new rows are individually added to the dataframe 
is suboptimal but nowhere near a speed bottleneck as many much more significant delays must be built in regardless. 
Additionally, faster data structures like NumPy arrays cannot natively handle inconsistent attributes well. 
Missed results are also tracked. 
'''
all_cars = pd.DataFrame()
not_added = []
no_crash_results = []

# Headless option, can remove if desired.
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

# Waits if a target to click isn't yet available.
driver.implicitly_wait(3)


# Scrapes the given webpage and adds the attributes to the master dictionary.
def scrape_stats(page, make, model, style, trim):
    # Broad try/except is used because some pages are empty. These misses are tracked via the 'not_added' list.
    # Initializes the dictionary with known values.
    try:
        attrs = {'make': [make], 'model': [model], 'style': [style], 'trim': [trim],
                 'year': page.find_element(By.XPATH, '//*[@id="yearSelect"]/option[2]').text,
                 'price': page.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div[3]/div[2]/div[2]').text}

        # Some pages start on an earlier index; this identifies and adjusts them.
        lower = 2
        upper = 17
        if page.find_element(By.XPATH, '//*[@id="main-content"]/div[3]/div/div[1]').text:
            lower -= 1
            upper -= 1

        # Iterates through the locations where data will be expected.
        for i in range(lower, upper):
            branch_loc = '//*[@id="main-content"]/div[3]/div/div[' + str(i) + ']/div'
            branch_items = page.find_element(By.XPATH, branch_loc)
            items = [item.text for item in branch_items.find_elements(By.TAG_NAME, 'div')]
            # print(make, model, style, trim, items)

            attrs[items[1]] = items[2]

            n = len(items)
            if n > 3:
                for c in range(4, n-1, 3):
                    attrs[items[c]] = items[c+1]

        # Finds the location of crash test results, if present, and scrapes them.
        # If not present, added to 'no_crash_results' list.
        try:
            for i in range(18,30):
                crash_loc = '//*[@id="main-content"]/div[3]/div/div[' + str(i) + ']/div'
                crash_items = page.find_element(By.XPATH, crash_loc)
                items = [item.text for item in crash_items.find_elements(By.TAG_NAME, 'div')]
                if 'Overall Rating' in items:
                    break
                else:
                    pass

            # If crash ratings were not found, this will intentionally break the try clause.
            crash_items = page.find_element(By.XPATH, crash_loc)
            items = [item.text for item in crash_items.find_elements(By.TAG_NAME, 'div')]

            attrs[items[1]] = items[2]

            n = len(items)
            if n > 3:
                for c in range(4, n - 1, 3):
                    attrs[items[c]] = items[c + 1]

        except:
            global no_crash_results
            no_crash_results.append(make + ' ' + model + ' ' + style + ' ' + trim)

        # Converts the dictionary to a dataframe and appends it to the master dataframe.
        attrs = pd.DataFrame.from_dict(attrs)
        global all_cars
        all_cars = pd.concat([all_cars, attrs])

    except:
        global not_added
        not_added.append(make + ' ' + model + ' ' + style + ' ' + trim)

    return None


# Get a list of the possible styles/configurations.
def get_styles(page):
    page.find_element(By.XPATH, '//*[@id="styleSelect"]').click()
    time.sleep(2)
    style_dropdown = driver.find_element(By.XPATH, '//*[@id="styleSelect"]')
    styles = [style.text for style in style_dropdown.find_elements(By.TAG_NAME, 'option')]
    styles.pop(0)
    page.find_element(By.XPATH, '//*[@id="styleSelect"]').click()
    time.sleep(2)
    return styles


# Get a list of the possible trims.
def get_trims(page):
    page.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
    time.sleep(2)
    trim_dropdown = page.find_element(By.XPATH, '//*[@id="trimSelect"]')
    trims = [trim.text for trim in trim_dropdown.find_elements(By.TAG_NAME, 'option')]
    trims.pop(0)
    page.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
    time.sleep(2)
    return trims


# When given a new style page for a particular make and model, scrapes that page as well as the different trim pages.
def new_style_init(page, make, model, curr_style):
    curr_trims = get_trims(page)
    scrape_stats(page, make, model, curr_style, curr_trims.pop(0))

    if len(curr_trims) > 0:
        i = 3
        while len(curr_trims) > 0:
            page.find_element(By.XPATH, '//*[@id="trimSelect"]').click()
            time.sleep(2)
            path = '//*[@id="trimSelect"]/option[' + str(i) + ']'
            page.find_element(By.XPATH, path).click()
            time.sleep(2)

            scrape_stats(page, make, model, curr_style, curr_trims.pop(0))

            time.sleep(random.uniform(6.5, 7.6))

            i += 1


count = 1
for make_model in squashed[:5]:
    make = make_model[0]
    model = make_model[1]
    url = 'https://www.caranddriver.com/' + make + '/' + model + '/specs'
    driver.get(url)
    print(url)

    # If the page is blank, record the make and model and move on.
    try:
        curr_styles = get_styles(driver)
        curr_style = curr_styles.pop(0)
    except:
        not_added.append(make + ' ' + model)
        continue

    new_style_init(driver, make, model, curr_style)

    time.sleep(random.uniform(6.1, 6.9))

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

    # Every 10 makes and models, the data is saved.
    if count % 10 == 0:
        with open('all_cars.pkl', 'wb') as f:
            pickle.dump(all_cars, f)
    count += 1

print(all_cars)
print('Not added: ', not_added)
print('No crash results: ', no_crash_results)

# Pickles the dataframe.
with open('all_cars.pkl', 'wb') as f:
    pickle.dump(all_cars, f)

all_cars.to_csv('all_cars.csv')
