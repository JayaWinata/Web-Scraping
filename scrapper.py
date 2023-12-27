import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = 'https://rb.gy/ab50wv'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.set_window_size(1366,768)
driver.get(url)

page = driver.find_element(By.CSS_SELECTOR,'[data-tab_type="STANDINGS"]')
page.click()
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Bagian Klasemen']"))
    )
    source_code = driver.find_element(By.TAG_NAME, 'table').get_attribute('innerHTML')
finally:
    driver.quit()

soup = BeautifulSoup(source_code,'html.parser')

print(soup.encode())
