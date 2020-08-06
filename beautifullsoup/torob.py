from bs4 import BeautifulSoup
import csv
import requests
import urllib
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
# you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
# you can also set number of user agents required by providing `limit` as parameter
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
# Get Random User Agent String.

search_key = input("write your product to see its price :\n  ").encode('utf-8')

products= []

def get_price(search_key):
    url = "https://torob.com/search/?query=%s"%search_key

    user_agent = user_agent_rotator.get_random_user_agent()
        
    headers = {
            'user-agent': user_agent,
            }
    try:
        page = urllib.request.urlopen(url,headers=headers)
    except :
        print("An error occured.")
    soup = BeautifulSoup(page, 'html.parser',from_encoding='utf-8')
    
    for row in soup.findAll('div',attrs={'class':'text-center product-card'}):
        product = {}
        product['value'] = row.findChild('div',attrs={'class':'price text-center'})1
        product['image'] = row.img['src']
        product['name'] = row.h5.text
        products.append(product)

    return products


filename = 'torob_product_search.csv'
with open(filename, 'w') as f:
    w = csv.DictWriter(f,['name','value','image'])
    w.writeheader()
    for quote in get_price(search_key):
        w.writerow(quote)
        
