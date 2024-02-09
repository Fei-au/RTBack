import requests
import math
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import Item_Category
from utils.currency import string_to_float_decimal


def get_image_urls(url):
    # Set the path to the Edge WebDriver executable
    edge_driver_path = "C:/Users/wangk/PycharmProjects/ExtractImage/msedgedriver.exe"

    # Set Edge WebDriver options
    edge_options = webdriver.EdgeOptions()
    edge_options.binary_location = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    # Replace with your actual path to Edge binary
    # edge_options.headless = True
    # Initialize Edge WebDriver with options
    driver = webdriver.Edge(options=edge_options)

    # Navigate to the webpage
    driver.get(url)

    if url[25:-1].isnumeric():
        image_element = driver.find_element(By.ID, 'landingImage')
        return [image_element.get_attribute('src')]
    else:

        try:
            # Find the thumbnail elements with class name "a-spacing-small item imageThumbnail a-declarative"
            thumbnail_elements = driver.find_elements(By.CSS_SELECTOR,
                                                    'li.a-spacing-small.item.imageThumbnail.a-declarative')

            # Interact with each thumbnail element and click the nested <span> with class name
            # "a-button a-button-thumbnail a-button-toggle"
            for i, thumbnail in enumerate(thumbnail_elements[:3], start=1):
                span_element = thumbnail.find_element(By.CSS_SELECTOR, 'span.a-button.a-button-thumbnail.a-button-toggle')
                ActionChains(driver).move_to_element(span_element).click().perform()

            # Use explicit wait to wait for the <li> elements with class prefix "image item item" to be present
            wait = WebDriverWait(driver, 4)
            li_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class^="image item item"]')))

            image_urls = []

            # Loop through the <li> elements and extract the image URLs
            for i, li_element in enumerate(li_elements[:3], start=1):
                image_element = li_element.find_element(By.TAG_NAME, 'img')
                image_url = image_element.get_attribute('src')
                image_urls.append(image_url)

            # Output the image URLs
            for idx, iURL in enumerate(image_urls, start=1):
                print(f"Image {idx}: {iURL}")

            return image_urls

        finally:
            # Close the browser when done
            driver.quit()

def download_images(image_urls, lot):
    # Folder where you want to save the images
    save_folder = PHOTO_FOLDER
    auction_num = AUCTION_NUM
    prefix = ''

    digits = int(math.log10(int(lot))) + 1
    if digits == 1:
        prefix = '000'
    elif digits == 2:
        prefix = '00'
    elif digits == 3:
        prefix = '0'

    # change_and_print_number(f"{auction_num}{prefix}{lot}")

    # Check if the folder exists, if not, create it
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Loop through the image URLs and download the images
    for i, image_url in enumerate(image_urls):
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Get the file extension from the URL
            file_extension = image_url.split(".")[-1]
            # Save the image to the specified folder
            image_name = os.path.join(save_folder, f"{auction_num}{prefix}{lot}_{str(i+1)}.{file_extension}")
            with open(image_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Image {} downloaded and saved as {}".format(i + 1, image_name))

    return True


def get_title(soup):
    span = soup.find('span', id='productTitle')
    if span:
        return span.text
    meta = soup.find('meta', name='title')
    if meta:
        return meta['content']
    meta2 = soup.find('meta', name='description')
    if meta2:
        return meta2['content']
    title = soup.find('title')
    if title:
        return title.text
    div = soup.find['titleSection']
    if div:
        h1 = div.find('h1', id='title')
        if h1:
            span_with_class = h1.find('span', class_='product-title-word-break')
            if span_with_class:
                return span_with_class.text
    return None




def get_description(soup):
    div = soup.find('div', id='productDescription')
    if div:
        p = div.find('p')
        if p:
            spans = p.find_all('span')
            if spans:
                text = ''
                for s in spans:
                    text += s.text + ' '
                return  text
    return None

def get_clses(soup):
    a_tags = soup.find_all('a', class_='a-link-normal a-color-tertiary')
    if a_tags:
        clses = []
        parent_cate = None
        for a in a_tags[:2]:
            text = a.text.replace('\n', '').strip()
            cates = None
            try:
                cates = Item_Category.objects.get(name=text)
            except Item_Category.DoesNotExist:
                print('do nothing')
            except Item_Category.MultipleObjectsReturned:
                cates = Item_Category.objects.filter(name=text)[0]
            if not cates:
                new_cate = Item_Category(name=text,parent_category=parent_cate)
                new_cate.save()
                parent_cate =  new_cate
            else:
                parent_cate = cates
                continue
        # return clses;
        return parent_cate
    return None

# def get_size(soup):
#     span_with_id = soup.find('span',id='native_dropdown_selected_size_name')
#     if span_with_id:
#         return  span_with_id.text
#     return  None

def get_color(soup):
    div_with_id = soup.find('div', id='variation_color_name')
    if div_with_id:
        spans = div_with_id.find_all('span', class_='selection')
        if spans:
            return  spans[0].text
    return None

def get_price(soup):
    span = soup.find('span',class_='a-price a-text-price a-size-medium apexPriceToPay')
    if span:
        s = span.find('span')
        return s.text
    span = soup.find('span', id='tp_price_block_total_price_ww')
    if span:
        s = span.find('span')
        return string_to_float_decimal(s.text[1:])
    return None

def get_bid_start_price(price):
    try:
        frt = "${:.2f}"
        if price < 6:
            return 1.00
        elif price >=6 and price <=10:
            return 2.00
        elif price>10 and price <=20:
            return 3.00
        elif price >20 and price <=50:
            return 5.00
        elif price >50 and price <=100:
            return 10.00
        else:
            v = int(price/100)*20
            return string_to_float_decimal(v)
    except:
        return None


# Return status and data if have
# status 0: url not found
# status 1: success
# status 2: url found but something error happended in process the data
# data: only have data for status 1, a dict including title, description ...
# message: status 0 or 2, error message

class TestResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

def scrap(code):
    # try:
        test = True
        response = None
        url = 'https://amazon.ca/dp/' + code + "/"
        if test:
            f = open('inventory/test', 'r', encoding='utf-8')
            response = TestResponse(200, f.read())
        else:
            response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = get_title(soup)
            description = get_description(soup)
            if not description:
                description = title
            b_code = code
            upc_code = None
            ean_code = None
            fnksu_code = None
            lpn_code = None
            pics = [] if test else get_image_urls(url)
            cls =get_clses(soup)

            customize_color = get_color(soup)
            price = get_price(soup)
            bid_start_price = None
            if price:
                bid_start_price = get_bid_start_price(price);
            return {
                'status':1,
                'data': {
                    'title': title,
                    'description': description,
                    'b_code':b_code,
                    'upc_code': upc_code,
                    'ean_code': ean_code,
                    'fnksu_code': fnksu_code,
                    'lpn_code': lpn_code,
                    'pics':pics,
                    'category': {'id': cls.id, 'name': cls.name} if cls else None,
                    'customize_color': customize_color,
                    'msrp_price': price,
                    'bid_start_price': bid_start_price,
                },
            }
        else:
            return {'status': 0, 'message': "Access to address " + 'https://amazon.ca/dp/' + code + "/" + " false."}
    # except Exception as e:
    #     print(e)
    #     return {'status': 2, 'message': 'Url found but some error happended in processing the data.'}