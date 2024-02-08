import requests
from bs4 import BeautifulSoup

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

def get_pics(soup):

    return None

def get_clses(soup):
    a_tags = soup.find_all('a', class_='a-link-normal a-color-tertiary')
    if a_tags:
        clses = []
        for a in a_tags:
            clses.append(a.text)
        return clses;
    return None
def get_size(soup):
    span_with_id = soup.find('span',id='native_dropdown_selected_size_name')
    if span_with_id:
        return  span_with_id.text
    return  None

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
        return span.text
    return None

def get_bid_start_price(price_str):
    try:
        price = float(price_str[1:])
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
            f = "{:.2f}".format(my_int)
            return float(f)
    except:
        return None


# Return status and data if have
# status 0: url not found
# status 1: success
# status 2: url found but something error happended in process the data
# data: only have data for status 1, a dict including title, description ...
# message: status 0 or 2, error message
def scrap(code):
    try:
        # response = requests.get('https://amazon.ca/dp/' + code + "/")
        print('0')

        f = open('test','r')
        print('1')
        response = {'status_code': 200, text: f.read()}

        if response.status_code == 200:
            soup = bs4(response.text, 'html.parse')
            print('here')

            title = get_title(soup)
            description = get_description(soup)
            if not description:
                description = title
            b_code = code
            upc_code = None
            ean_code = None
            fnksu_code = None
            lpn_code = None
            pics = get_pics(soup)
            cls =get_clses(soup)
            cutomize_size = get_size(soup)
            cutomize_color = get_color(soup)
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
                    'categories': cls,
                    'cutomize_size': cutomize_size,
                    'cutomize_color': cutomize_color,
                    'msrp_price': price,
                    'bid_start_price': bid_start_price,
                },
            }
        else:
            return {'status': 0, 'message': "Access to address " + 'https://amazon.ca/dp/' + code + "/" + " false."}
    except:
        return {'status': 2, 'message': 'Url found but some error happended in processing the data.'}