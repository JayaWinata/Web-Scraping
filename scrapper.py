import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://rb.gy/ab50wv'
page = requests.get(url, timeout=10)
soup = BeautifulSoup(page.content, 'html.parser')

table_soup = soup.find('table')

print(table_soup)