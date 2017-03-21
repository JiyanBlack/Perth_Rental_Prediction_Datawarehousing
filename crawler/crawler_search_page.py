import urllib.request,urllib.parse
import pandas
import re
from bs4 import BeautifulSoup
import hashlib

req_headers = {'Host': 'www.realestate.com.au',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

df = pandas.DataFrame(columns = ['url','rental','bedroom','bathroom','carpool','address'])

url_pool = "http://www.realestate.com.au/rent/in-perth+-+greater+region%2c+wa/list-1"

generate_url_re = re.compile(r'.*?/list-(\d+)$')

def generate_url(cur_url):
    global generate_url_re
    cur_url.strip()
    print('Finish: ',cur_url)
    match_result = re.match(generate_url_re,cur_url)
    page_number = match_result.groups()[0]
    # print(-len(page_number))
    url_no_page = cur_url[0:-len(page_number)]
    next_page_number = str(int(page_number) + 1)
    next_url = url_no_page + next_page_number
    print('Begin: ', next_url)
    return next_url

# def test_invalid_page(cur_html):
#     if cur_html.decode('utf8').find("We couldn't find anything matching your search criteria:")>0:
#         return True
#     return False

def get_html(cur_url):
    global req_headers
    req = urllib.request.Request(cur_url, headers=req_headers)
    with urllib.request.urlopen(req) as res:
        return res.read()

def find_all_dd(one_house):
    dds = one_house.find_all('dd')
    result = ['0','0','0']
    for i in range(len(dds)):
        result[i] = dds[i].string
    return result

def parse_one_house(one_house):
    detail_url = one_house.find('a')['href']
    try:
        price = one_house.find('p',class_ = 'priceText').string
    except AttributeError as e:
        price = None
    [bedroom, bathroom, carpool] = find_all_dd(one_house)
    # bedroom = one_house.find('dt',class_='rui-icon-bed').string
    # bathroom = one_house.find('dt',class_='rui-icon-bath').string
    # carpool = one_house.find('dt',class_='rui-icon-car').string
    try:
        address = one_house.find('h2', class_='rui-truncate').string
    except AttributeError as e:
        address = None
    return {'url':detail_url, 'rental':price, 'bedroom':bedroom, 'bathroom':bathroom, 'carpool':carpool, 'address':address}

def parse_html(cur_html):
    with open('test.html','wb') as f:
        f.write(cur_html)
    soup = BeautifulSoup(cur_html,'lxml')
    all_article = soup.find_all('article',class_ = 'resultBody')
    # print(len(one_article))
    house_details = []
    for one_house in all_article:
        parse_one_house(one_house)
        one_house_detail = parse_one_house(one_house)
        house_details.append(one_house_detail)
    if not house_details:
        return False
    return house_details

def save_to_csv(cur_pased):
    global df
    for one_row in cur_pased:
        df.loc[-1] = one_row
        df.index += 1
    df.to_csv('raw_house_info.csv', index=False)

def main():
    global url_pool
    cur_url = url_pool
    is_next_page = True
    while is_next_page:
        cur_html = get_html(cur_url)
        # print(cur_html)
        cur_parsed = parse_html(cur_html)
        if not cur_parsed:
            print('Reach the end.')
            break
        save_to_csv(cur_parsed)
        cur_url = generate_url(cur_url)

if __name__ == "__main__":
    main()