from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

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
    source_code = driver.find_element(By.CLASS_NAME, 'Jzru1c').get_attribute('innerHTML')
finally:
    driver.quit()

soup = BeautifulSoup(source_code,'html.parser')
tr = soup.find_all('tr')

header = tr[0].find_all('th')
header = [data.text.strip() for data in header]
header = header[2:len(header)-2]
print(header)

def clean_header(header: list[str]):
    new_header = []
    for data in header:
        if (data[1].islower()):
                new_data = data
        else:
            while (data[1].isupper()):
                data = data[1:]
            new_data = data        
        new_header.append(new_data)
    return new_header

header = clean_header(header)

df = pd.DataFrame(columns=header)

tr = tr[1:]
print(tr)

for data in tr:
    td = data.find_all('td')
    td_text = [td_text.text.strip() for td_text in td]
    df.loc[len(df)] = td_text[2:len(td_text)-3]

df['Peringkat'] = df.index + 1
df['Poin'] = (df['Menang'] * 3) + (df['Seri'])

