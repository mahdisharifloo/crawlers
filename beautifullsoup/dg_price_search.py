from bs4 import BeautifulSoup
import urllib.request
import re

url = "https://www.digikala.com/search/?q=chair"

page = urllib.request.urlopen(url) # conntect to website

try:
    page = urllib.request.urlopen(url)
except:
    print("An error occured.")

soup = BeautifulSoup(page, 'html.parser')
prices = soup.find_all('span',attrs={'class':'a-price-whole'})