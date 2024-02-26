import requests
import math
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .models import Item_Category, Item, Image
from utils.currency import string_to_float_decimal
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from utils.file import get_extension_from_url
from django.conf import settings
from urllib.parse import urljoin
from .serializers import ItemCategorySerializer
import re
import time


def get_image_urls(url):
    # Set the path to the Edge WebDriver executable
    # edge_driver_path = "C:/Users/wangk/PycharmProjects/ExtractImage/msedgedriver.exe"

    # Set Edge WebDriver options
    edge_options = webdriver.EdgeOptions()
    edge_options.binary_location = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    # Replace with your actual path to Edge binary
    # edge_options.headless = True
    # Initialize Edge WebDriver with options
    driver = webdriver.Edge(options=edge_options)

    # Navigate to the webpage
    driver.get(url)
    # driver.implicitly_wait(10)
    raw_html = driver.page_source
    current_url = driver.current_url



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

            return image_urls, raw_html, current_url

        finally:
            # Close the browser when done
            driver.quit()

def getRawHtmlByNumCode(driver, code, amz_url):

    driver.get(amz_url)

    # input number code and start search
    input_element = driver.find_element(By.ID, 'twotabsearchtextbox')
    input_element.clear()
    input_element.send_keys(code)

    submit_button = driver.find_element(By.ID, 'nav-search-submit-button')
    submit_button.click()

    # wait until find the first result
    try:
        wait = WebDriverWait(driver, 4)
        result_title_div = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-cel-widget="search_result_0"]')))
        title = result_title_div.find_element(By.CSS_SELECTOR, '.a-size-medium-plus')
        if title.text != 'Results':
            raise TimeoutException('Not find the product')
        first_result = driver.find_element(By.XPATH, '//*[@data-cel-widget="search_result_1"]')
        # click the first result to go to the product page
        first_img_link = first_result.find_element(By.TAG_NAME, value='a')
        first_img_link.click()
        wait2 = WebDriverWait(driver, 4)
        product_page = wait2.until(EC.presence_of_element_located((By.ID, 'productTitle')))

    except (TimeoutException, NoSuchElementException) as e:
        print('here in the exception')
        if amz_url.find('.ca') != -1:
            return getRawHtmlByNumCode(driver, code, 'https://www.amazon.com/')
        else:
            return 'Code not found in both amazon.ca and amazon.com'
    except:
        return 'Error happend'

    # get first three imgs
    image_urls = []
    raw_html = None
    current_url = None
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


        # Loop through the <li> elements and extract the image URLs
        for i, li_element in enumerate(li_elements[:3], start=1):
            image_element = li_element.find_element(By.TAG_NAME, 'img')
            image_url = image_element.get_attribute('src')
            image_urls.append(image_url)

        # Output the image URLs
        for idx, iURL in enumerate(image_urls, start=1):
            print(f"Image {idx}: {iURL}")

    finally:
        # get raw source
        raw_html = driver.page_source
        current_url = driver.current_url
        # Close the browser when done
        driver.quit()

    return image_urls, raw_html, current_url
def scrpByHtml(urls, text, c_r):
    b_code = getCodeByUrl(c_r)
    upc_ean_code = None
    # remove following codes
    # upc_code = None
    # ean_code = None
    # fnksu_code = None
    # lpn_code = None
    pics = []
    for u in urls:
        img_instance = download_image(u)
        pics.append({'id': img_instance.id,
                     'url': urljoin('http://192.168.2.79:8000/', 'inventory' + img_instance.local_image.url),
                     'has_saved': True})
    soup = BeautifulSoup(text, 'html.parser')
    title = get_title(soup)
    description = title
    # set description same as title
    # description = get_description(soup)
    # if not description:
    #     description = title
    cls = get_clses(soup)
    customize_color = get_color(soup)
    price = get_price(soup)
    print('price', price)
    bid_start_price = None
    if price:
        bid_start_price = get_bid_start_price(price);
    return {
        'status': 1,
        'data': {
            'title': title,
            'description': description,
            'b_code': b_code,
            'upc_ean_code': upc_ean_code,
            # 'upc_code': upc_code,
            # 'ean_code': ean_code,
            # 'fnksu_code': fnksu_code,
            # 'lpn_code': lpn_code,
            'pics': pics,
            'category': {'id': str(cls.id), 'name': cls.name} if cls else None,
            'customize_color': customize_color,
            'msrp_price': price,
            'bid_start_price': bid_start_price,
        },
    }
def scrapInfoByNumCodeService(code):
    start_time = time.time()
    # Set Edge WebDriver options
    edge_options = webdriver.EdgeOptions()
    edge_options.binary_location = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    # Replace with your actual path to Edge binary
    # edge_options.headless = True
    # Initialize Edge WebDriver with options
    driver = webdriver.Edge(options=edge_options)
    # get imgs and raw html
    res = getRawHtmlByNumCode(driver, code, 'https://www.amazon.ca/')
    if isinstance(res, tuple):
        img_urls, raw_html, current_url = res
        mid_time = time.time()
        print(f"****************Scrp time in web took {mid_time - start_time:.2f} seconds.")
        # gather product info
        result = scrpByHtml(img_urls, raw_html, current_url)
        end_time = time.time()
        print(
            f"****************Gather all info including download imgs processing took {end_time - mid_time:.2f} seconds.")
        return result;
    else:
        # not find the product
        msg = res
        return {'status': 0, 'message':msg }


def get_title(soup):
    span = soup.find('span', id='productTitle')
    if span:
        return span.text.replace('\n', '').strip()
    meta = soup.find('meta', name='title')
    if meta:
        return meta['content']
    meta2 = soup.find('meta', name='description')
    if meta2:
        return meta2['content']
    title = soup.find('title')
    if title:
        return title.text.replace('\n', '').strip()
    div = soup.find['titleSection']
    if div:
        h1 = div.find('h1', id='title')
        if h1:
            span_with_class = h1.find('span', class_='product-title-word-break')
            if span_with_class:
                return span_with_class.text.replace('\n', '').strip()
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
        for a in a_tags[:1]:
            text = a.text.replace('\n', '').strip()
            try:
                cates = Item_Category.objects.get(name=text)
                return cates
            except Item_Category.DoesNotExist:
                ic = Item_Category(name=text)
                ic.save()
                return   ic
            except Item_Category.MultipleObjectsReturned:
                cates = Item_Category.objects.filter(name=text)[0]
                return cates

            # if not cates:
            #     new_cate = Item_Category(name=text,parent_category=parent_cate)
            #     new_cate.save()
            #     parent_cate =  new_cate
            # else:
            #     parent_cate = cates
            #     continue
        # return clses;
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
            return  spans[0].text.replace('\n', '').strip()
    return None

def get_price(soup):
    span = soup.find('span',class_='priceToPay')
    # span = soup.find('span',class_='a-price aok-align-center reinventPricePriceToPayMargin priceToPay')
    if span:
        s = span.find('span', class_='a-offscreen')
        if s:
            t = s.text[1:].strip()
            if t:
                print('priceToPay is', t)
                return string_to_float_decimal(t)
    spans = soup.find_all('span', class_='apexPriceToPay')
    # For price pattern like $18.30 - $20.55, return highest price
    if spans:
        if len(spans) > 1:
            span = spans[-1]
            s = span.find('span', class_='a-offscreen')
            if s:
                print('apexPriceToPay is', s)
                return string_to_float_decimal(s.text[1:])
        else:
            span = spans.find('span', class_='a-offscreen')
            if span:
                print('apexPriceToPay is', span)
                return string_to_float_decimal(span.text[1:])
    span = soup.find('span', class_='a-price-whole')
    if span:
        print('a-price-whole is', span)
        return string_to_float_decimal(span.text)
    # span = soup.find('span', id='tp-tool-tip-subtotal-price-value')
    # print('span3', span3)
    # if span3:
    #     s = span3.find('span')
    #     print('return2', s.text)
    #     return string_to_float_decimal(s.text[1:])
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

def download_image(image_url):
    image_instance = Image()
    extension = get_extension_from_url(image_url)
    image_instance.external_url = image_url
    response = requests.get(image_instance.external_url)
    if response.status_code == 200:
        # Create a temporary file
        img_temp = NamedTemporaryFile()
        img_temp.write(response.content)
        img_temp.flush()
        img_temp.seek(0)
        # Load the content into a Django File
        img_file = ContentFile(img_temp.read(), name='temp_name'+extension)
        # Save the image to the model's ImageField
        image_instance.local_image.save(img_file.name, img_file, save=True)
        image_instance.save()
        print('new downloaded image_instance', image_instance.id)
        img_temp.close()
        return  image_instance

def set_image_fk(img_id, item_id):
    img_instance = Image.objects.get(id=img_id)
    img_instance.item_id = item_id
    img_instance.save()
    return img_instance

def create_img_with_fk(img, item_id):
    i = Image(local_image=img, item_id=item_id)
    return HttpResponse(i.id)

def getUrl(code):
    return 'https://amazon.ca/dp/' + code + "/"

def getCodeByUrl(url):
    match = re.search(r"dp\/([A-Za-z0-9]+)", url)
    if match:
        result = match.group(1)
        return result
    else:
        return None




def scrap(**kwargs):
    print('here in scrap')
    print('scrap', kwargs)
    url = kwargs.get('url')
    print('pass url')
    code = kwargs.get('code')
    print('pass code')
    # try:
    print('here')

    if not code:
        code =getCodeByUrl(url)
    test = False
    text = None
    if test:
        f = open('inventory/test', 'r', encoding='utf-8')
        text = f.read()
    else:
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        #     "Accept-Language": "en-US,en;q=0.9",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "origin": "https://www.amazon.ca",
        #     "Referer": "https://www.amazon.ca/dp/B0CLNSHRMP/ref=sspa_dk_detail_3?psc=1&pd_rd_i=B0CLNSHRMP&pd_rd_w=TppfT&content-id=amzn1.sym.feb8168a-837d-4479-a008-abb92f74a28b&pf_rd_p=feb8168a-837d-4479-a008-abb92f74a28b&pf_rd_r=57NXXZ8723HJBANB1899&pd_rd_wg=xBLcW&pd_rd_r=f88e047f-542a-49e7-b732-46113de6ea57&s=shoes&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM",
        #     "Connection": "keep-alive",
        # }
        # print('url2', url)
        # response = requests.get(url)
        # print()
        print('url is', url)
        urls, text, c_r = get_image_urls(url)
        if not code:
            code = getCodeByUrl(c_r)
        b_code = code
        upc_ean_code = None
        # remove following codes
        # upc_code = None
        # ean_code = None
        # fnksu_code = None
        # lpn_code = None
        pics = []
        for u in urls:
            img_instance = download_image(u)
            pics.append({'id': img_instance.id,
                         'url': urljoin('http://192.168.2.79:8000/', 'inventory' + img_instance.local_image.url),
                         'has_saved': True})
        soup = BeautifulSoup(text, 'html.parser')
        title = get_title(soup)
        description = title
        # set description same as title
        # description = get_description(soup)
        # if not description:
        #     description = title
        cls = get_clses(soup)
        customize_color = get_color(soup)
        price = get_price(soup)
        print('price', price)
        bid_start_price = None
        if price:
            bid_start_price = get_bid_start_price(price);
        return {
            'status': 1,
            'data': {
                'title': title,
                'description': description,
                'b_code': b_code,
                'upc_ean_code': upc_ean_code,
                # 'upc_code': upc_code,
                # 'ean_code': ean_code,
                # 'fnksu_code': fnksu_code,
                # 'lpn_code': lpn_code,
                'pics': pics,
                'category': {'id': str(cls.id), 'name': cls.name} if cls else None,
                'customize_color': customize_color,
                'msrp_price': price,
                'bid_start_price': bid_start_price,
            },
        }
    # else:
    #     print('response.status_code', response.status_code)
    #     return {'status': 0, 'message': "Access to address " + 'https://amazon.ca/dp/' + code + "/" + " failed."}
    # except Exception as e:
    #     print(e)
    #     return {'status': 2, 'message': 'Url found but some error happended in processing the data.'}


