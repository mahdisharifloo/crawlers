# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from image_data_enum import ColumnName


class Utils:

    image_format = '.jpg'
    start_of_image_name = 'digikala-products/'
    download_folder = 'download'

    def __init__(self, url_categorylist):
        """
        Args:
            url_categorylist (str/url) product list page url, help to craete corresponding directory
        """
        self.page_list = []
        self.base_url = 'https://www.digistyle.com'
        self.full_links = []
        self.images = []

        

        self.category = self.find_name_between_this(url_categorylist, 'www.digistyle.com/', '/?pageno=', False)

        self.download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.download_folder, self.category)
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        self.columns = [ColumnName.NAME.value,
                        ColumnName.IMAGE_RELETIVE.value, ColumnName.IMAGE_ABSOLUTE.value, ColumnName.IMAGE_URL.value,
                        ColumnName.PRODUCT_ID.value, ColumnName.PRODUCT_URL.value]
        self.image_data = pd.DataFrame(columns=self.columns)
        
    def product_list_urls(self,url_category_list,max_page_number):
        '''
            you should input base url that you want to search and navigate hover on pages number
            
            NOTE:
                    Don't input page number of products whene you want to initialize base_url it should be automated
                    input number end page of product list 
        '''
        self.page_list =[]
        
        for i in range(1,max_page_number):
            url = url_category_list+str(i)
            self.page_list.append(url)
        return self.page_list
    
    def page_reader(self,page_url):
        '''
            this two function give page url address and make soup for dinner.
            
            NOTE:
                    be careful that maybe your soup is hot !!!
        '''
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    
    def product_extractor(self,page_url):
        '''
            this madule can extract every product segments on list page of some category
        '''
        soup = self.page_reader(page_url)
        product_paths = soup.findAll('a', {'class': 'c-product-item__image-wrapper'},href=True)
        print("number of products in this page are", len(product_paths))
        return product_paths
    
    def product_link_extractor(self,a):
        '''
            this madule can extract links of products to navigate programe to product page
        '''
        #self.full_links = []
        product_link = a['href']
        full_link = self.base_url+product_link
        print('full_link', full_link)
        self.full_links.append(full_link)
        print("len(self.full_links)", len(self.full_links))
        return full_link
    
    def product_page_images(self, product_page):
        '''
            this madule can extract images of product that stored on product single page
        '''
        #self.images = []
        # for product_page in self.full_links:
        print('[READING PAGE]\n'+product_page)
        soup = self.page_reader(product_page)
        print('\nok')    
        # this div is the left side div with all the images thumbnail
        # and the name of the original image is the same as the thumbnail image
        div_image = soup.find('div',{'class':'c-swiper-quick-view-gallery__thumbs-container c-swiper-quick-view-gallery__thumbs-container--pdp'})
        # iterate over images in this div and change images url to a high quality image
        for image in div_image.findAll('img', {'class': 'c-product-item__image'}):
            src = image.get('src')
            # dl_image_src = src[:src.rfind('resize')] + "resize,w_1600/quality,q_80"
            dl_image_src = src[:src.rfind('resize')] + "resize,h_500,w_500/quality,q_80"
            self.images.append(dl_image_src)
            self.add_image_to_data_frame(product_page, dl_image_src)

        print("images number ", len(self.images))
        return self.images
            
        
        

    def add_image_to_data_frame(self, product_page, image_url):
        """Add all the data about the current image to a dataFrame.
        data include in [self.columns]
        self.columns=['name', 'image_path', 'image_absolute', 'image_url', 'product_id', 'prdouct_url'].

        Args:
            product_page (str): current product being extraxted
            image_url (str): one of the image from the product_page

        """


        
        # Find image name.
        # start of the name is in image url strat after digikala-product 
        # adding the second part len(start_of_image) is necessary, it cause the image name start
        # after the variable [start_of_iamge_name] ends
        # end if image is the image format which is .jpg
        # find image name based on the start and end of the image name in url
        # image_name_start_index = image_url.find(start_of_image_name) + len(start_of_image_name)
        # image_name_end_index = image_url.find(image_format) + len(image_format)
        # image_name = image_url[image_name_start_index:image_name_end_index]
        image_name = self.find_name_between_this(image_url, self.start_of_image_name, self.image_format, True)

        # base on [image_name]
        absolute_path = os.path.join(self.download_path, image_name)
        reletive_path = os.path.join(self.download_folder, self.category, image_name)


        # product ID appeared in product_url,
        # this ID works only on digistyle url style
        product_page_product = 'product/'
        # prodcut_id_start = product_page.find() + len(product_page_product)
        # product_id_end = product_page.find('-')
        # prodcut_id = product_page[prodcut_id_start:product_id_end]
        prodcut_id = self.find_name_between_this(product_page, product_page_product, '-', False)

        # create a pd.Series from the data to add to the [self.image_data]
        sample = pd.Series(data={ColumnName.NAME.value: image_name, ColumnName.IMAGE_RELETIVE.value : reletive_path,
                            ColumnName.IMAGE_ABSOLUTE.value: absolute_path, ColumnName.IMAGE_URL.value: image_url,
                            ColumnName.PRODUCT_ID.value: prodcut_id, ColumnName.PRODUCT_URL.value: product_page})

        self.image_data = self.image_data.append(sample, ignore_index=True)
        print("imagedata len", len(self.image_data))


    def find_name_between_this(self, string, start, end, inclue_end=False):
        """From the given string find the world in between start and end.  

        Parameters
        ----------  
        string : str 
            string to performe slicing on it.
        start : str 
            specify the start of slicing.
        end : str 
            specify where the slicing should end.
        include_end : bool, default=False
            if end string should be included in the sliced substring.

        Returns
        -------
        str
            A sub string start from @start and end in @end.
        """
        start_index = string.find(start) + len(start)
        end_index = string.find(end) 
        if inclue_end == True:
            # add this cause slicing to add end string 
            end_index += len(end)
        return string[start_index:end_index]