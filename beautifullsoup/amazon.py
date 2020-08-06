from bs4 import BeautifulSoup
import urllib.request
import re

search_key = input("write your product to see its price :\n  ").encode('utf-8')
products= []
def get_price(search_key):
    url = "https://www.amazon.com/s?k=%s"%search_key
    try:
        page = urllib.request.urlopen(url)
    except:
        print("An error occured.")
    soup = BeautifulSoup(page, 'html.parser',from_encoding='utf-8')
    
    for row in soup.findAll('span',attrs={'class':'a-price-whole'}):
        product = {}
        product['value'] = row.text
        #product['name'] = row
        products.append(product)
    return "\n\nyour soup is ready for eating !!!  ;)"

print(products,get_price(search_key))