from enum import Enum

class ColumnName(Enum):
    NAME = 'name' 
    IMAGE_RELETIVE = 'image_path'
    IMAGE_ABSOLUTE = 'image_absolute'
    IMAGE_URL = 'image_url'
    PRODUCT_ID = 'product_id'
    PRODUCT_URL = 'prdouct_url'