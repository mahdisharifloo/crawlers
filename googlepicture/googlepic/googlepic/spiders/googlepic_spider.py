import scrapy
import urllib
from googlepic.items import GooglepicItem
import json

class GoogleSearchSpider(scrapy.Spider):
    name = "googlepic"
    key_word='دستمال کاغذی'
    page_cnt=3 # return count=page_cnt*rsz

    params = {
            'v': '1.0',
            'q': key_word,
            'rsz': 8, # range 1 to 8
            'start': 0,
            'as_filetype': 'jpg'
    }

    start_urls = []
    for i in range(0,page_cnt):
        start_urls.append('https://ajax.googleapis.com/ajax/services/search/images?'+ urllib.request.urlopen(params))
        params['start']+=params['rsz']

    def parse(self, response):
        response =json.loads(response.body)
        for result in response['responseData']['results']:
            item = GooglepicItem()
            item['host']=self.name
            item['s']=self.key_word
            img = result['unescapedUrl']
            if img.find('?') > 0:
                img = img[:img.find('?')]
            item['src_link']=img
            yield item