import requests
import json
import urllib.request
from bs4 import BeautifulSoup
from pathlib import Path
import os


base_url = "https://www.flickr.com/services/rest/"
api_key = "4808f0ddc101f73dc08a184ce239856f"
format_json = "json"
name = "apple"


def get_photo_list():
    method = "flickr.photos.search"
    if not os.path.exists(name):
        os.makedirs(name)
        
    for page in range(1, 12):
        response = requests.get(
            base_url,
            params={
                "method": method,
                "api_key": api_key,
                "format": format_json,
                "tags" : name+",fruit",
                "tag_mod": "all",
                "sort": "relevance",
                "page": str(page),
                }
            )
        
        
        content_dict = json.loads(response.text[14:-1])
        photos = content_dict["photos"]
        print("page", photos["page"], "pages", photos["pages"] ,"totoal", photos["total"])
        photos_list = photos['photo']
        for index, photo in enumerate(photos_list):
            print(index, "of", len(photos_list))
            get_photo_detail(photo["id"])
        

def get_photo_detail(id):
    method = "flickr.photos.getInfo"
    response = requests.get(
        base_url,
        params={
            "method": method,
            "api_key": api_key,
            "photo_id": id,
            "format": format_json
            }
        )
        
    
    photot_dict = json.loads(response.text[14:-1])
    urls = photot_dict["photo"]["urls"]
    url = urls["url"]
    content = url[0]["_content"]
    print(content)
    
    try:
        src = link(content, id)
        p = Path(name + "/" + "_".join([name, id, ".jpg"]))
        urllib.request.urlretrieve(src, str(p))
        
        images_links.write(src + "\r\n")
    except Exception as e:
        print(e)
        
        
def link(url, id):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup)
    # div_photo = soup.find('div', id= 'main-photo-container')
    #print(div_photo)
    #imgs = div_photo.find_all('img')
    #print(imgs)
    images = soup.find_all("img", {"class": "main-photo"})
    img = images[0]
    src = "https:" + img['src']
    
    print(src)

    return src
    



file = open('labels.txt')  
lines = file.readlines()   

for name in lines:
  images_links = open(name + ".txt", "a+")
  get_photo_list()
  images_links.close()
#get_photo_detail("48840945736")

