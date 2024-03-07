from urllib.parse import urlparse
import os
from datetime import datetime

def get_extension_from_url(u):
    parsed_url = urlparse(u)
    _,file_extension = os.path.splitext(parsed_url.path)
    return file_extension


def image_upload_to(filename):
    # Format the current date as YYYYMMDD
    date_prefix = datetime.now().strftime('%Y%m%d')
    # Return the path with the date prefix and the original filename
    return f'image/{date_prefix}/{filename}'

def get_extension(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension