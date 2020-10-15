from selenium import webdriver
import pandas as pd

DRIVER_PATH = '/Users/vwong/Documents/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://imperial.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=553b3a2b-431d-47a9-ab09-ac5201301c0e')

a = driver.find_elements_by_class_name("span")
print(a)