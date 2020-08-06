
from google_images_download import google_images_download
# documentation : https://google-images-download.readthedocs.io/en/latest/arguments.html


search_list = []
limit=20
response = google_images_download.googleimagesdownload()
keywords = input('input your search keywords :  ')
limit = int(input('input number of pics that you need download :  '))
arguments = {"keywords":keywords,"limit":limit,"print_urls":True}   #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function
print(paths)   #printing absolute paths of the downloaded images

#
#file = open('labels.txt')  
#lines = file.readlines()   
#
#for line in lines:
#    keywords = line
#    arguments = {"keywords":keywords,"limit":limit,"print_urls":True}   #creating list of arguments
#    paths = response.download(arguments)   #passing the arguments to the function
#    print(paths) 