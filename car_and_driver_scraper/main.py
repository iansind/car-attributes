from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time

# Initial installation of driver.
'''from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))'''

driver = webdriver.Chrome()
driver.get('https://www.caranddriver.com/')
driver.implicitly_wait(3)

# Clicks on the 'Makes and Models' button to make the dropdown available.
# Sleeps are important to allow for fields to load.
driver.find_element(By.XPATH, '//*[@id="__next"]/div/nav/div[1]/div[1]/button').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="modal-root"]/div[2]/div/div[2]/select').click()
time.sleep(0.5)
dropdown1 = driver.find_element(By.XPATH, '//*[@id="modal-root"]/div[2]/div/div[2]/select')

makes = [make.get_attribute('value') for make in dropdown1.find_elements(By.TAG_NAME, 'option')]

makes_models = []
for i in range(2, len(makes)+1):
    time.sleep(0.5)
    path = '//*[@id="modal-root"]/div[2]/div/div[2]/select/option[' + str(i) + ']'
    driver.find_element(By.XPATH, path).click()
    time.sleep(0.5)

    dropdown2 = driver.find_element(By.XPATH, '//*[@id="modal-root"]/div[2]/div/div[3]/select')
    curr_models = [(makes[i-1], model.get_attribute('value')) for model in dropdown2.find_elements(By.TAG_NAME, 'option')
                   if model.get_attribute('value') != '0']
    makes_models.append(curr_models)

for make in makes_models:
    print(make)
