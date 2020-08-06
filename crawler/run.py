# -*- coding: utf-8 -*-
'''
    we want to use utils for crawling and ruunnig this project in this file.
    
    NOTES : 
        url_category variable is main link stracture of product lists pages.
        so you should add page number at the very end of that.
        users should to input maximum of pages that he or she want.
        

'''
import os
from bs4 import BeautifulSoup
from utils import Utils
from image_data_enum import ColumnName
from time import sleep
from random  import randint
import pandas as pd 
import wget
import numpy as np 

utils = None
counter = 0
''' 
 for EXAMPLE : 
     https://www.digistyle.com/mel-and-moj-brand/?pageno=1
'''
#max_page_number = 2
#url_categorylist = 'https://www.digistyle.com/mel-and-moj-brand/?pageno='
#url = 'https://dkstatics-public.digikala.com/digikala-products/110077637.jpg?x-oss-process=image/resize,m_lfit,h_400,w_400/quality,q_100'
#des_path = '/home/mahdi/Pictures/test/crawler_download1.jpg'


    
def inintialize_meta_data(url_categorylist,max_page_number):
    page_urls = utils.product_list_urls(url_categorylist,max_page_number)
    for page_url in page_urls:
        product_paths = utils.product_extractor(page_url)
        print("len product in run ins", len(product_paths))
        for a in product_paths:
            pro_page = utils.product_link_extractor(a)
            utils.product_page_images(pro_page)
    # utils.image_data.to_csv("image_data.csv")
            
def create_dataframe(image_dataframe):
    image_dataframe.to_csv(utils.category + '_before.csv')

    image_dataframe.replace('', np.nan, inplace=True)
    image_dataframe = image_dataframe.dropna()
    image_dataframe = image_dataframe.reset_index()
    image_dataframe.to_csv(utils.category + '_after.csv')
    return image_dataframe


def downloader(image_dataframe):
    # don't donwlad if the file already exists
    for key, item in image_dataframe.iterrows():
        image_url = item[ColumnName.IMAGE_URL.value]
        image_absolute_path = item[ColumnName.IMAGE_ABSOLUTE.value]
        if not os.path.exists(image_absolute_path):
            print('[STATUS] >>> downloading', image_url)
            wget.download(url=image_url, out=image_absolute_path)
            print('[STATUS] >>> save as',image_absolute_path)
        else:
            print("[SKIP] >>> skip", image_absolute_path)


def run():
    global utils
    url_categorylist = input('input page category that you want extract all of it products \n for example : \n \t "https://www.digistyle.com/mel-and-moj-brand/?pageno="\n NOTE : \n \t * do not input the number of page.\n : ')
    max_page_number = int(input('input number of end list  : '))
    # url_categorylist = "https://www.digistyle.com/mel-and-moj-brand/?pageno="
    # max_page_number = 2
    # img_df = create_dataframe(url_categorylist,max_page_number)

    utils = Utils(url_categorylist)

    inintialize_meta_data(url_categorylist, max_page_number)
    create_dataframe(utils.image_data)
    downloader(utils.image_data)
    # download_folder = 'download'
    # download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), download_folder)
    # if not os.path.exists(download_path):
    #     os.makedirs(download_path)

    # for path in img_df[0]:
    #     image_name_start_index = path.find(start_of_image_name) + len(start_of_image_name)
    #     image_name_end_index = path.find(image_format) + len(image_format)
    #     image_name = path[image_name_start_index:image_name_end_index]
    #     des_path = os.path.join(download_path, image_name)
    #     downloader(path, des_path)
    #     counter +=1
            
if __name__ == "__main__":
    run()
