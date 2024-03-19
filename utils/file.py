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

def create_unique_filename(dir, filename, extension):
    counter = 0
    if not os.path.exists(dir):
        os.makedirs(dir)
    file_path = os.path.join(dir, filename + extension)
    while os.path.exists(file_path):
            counter += 1
            file_path = os.path.join(dir, f"{filename}_{counter}{extension}")
    return file_path


def create_unique_imagename(existing_names, imagename):
    counter = 1
    base_name, extension = os.path.splitext(imagename)
    new_name = f'{base_name}_{counter}{extension}'

    while new_name in existing_names:
        counter += 1
        new_name = f'{base_name}_{counter}{extension}'
    return new_name
