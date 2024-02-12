from urllib.parse import urlparse
import os

def get_extension_from_url(u):
    parsed_url = urlparse(u)
    _,file_extension = os.path.splitext(parsed_url.path)
    return file_extension