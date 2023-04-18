from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle

# Initial installation of driver.
'''from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))'''

driver = webdriver.Chrome()
driver.get('https://www.caranddriver.com/')
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
    s += len(make)

print(f'A total of {s} variations of make and model were obtained.')

# Pickles the file. Used over JSON to preserve tuple type.
with open('make_models.pkl', 'wb') as f:
    pickle.dump(makes_models, f)

with open('make_models.pkl', 'rb') as f:
    loaded = pickle.load(f)

# Checks the integrity of the saved file.
integrity = '' if loaded == makes_models else 'not '
print(f'The saved file is {integrity}valid.')
