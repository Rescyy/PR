import requests
from bs4 import BeautifulSoup

url = "https://example.com"

try:
    response = requests.get(url)

    if response.status_code == 200:
        print("GET request ")
except:
    pass