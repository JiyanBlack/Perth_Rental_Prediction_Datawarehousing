import urllib.request,urllib.parse
import pandas
import re
from bs4 import BeautifulSoup

req_headers = {'Host': 'www.realestate.com.au',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

domain = "http://www.realestate.com.au"

df = pandas.read_csv('./csvs/realestate_4000_details.csv')

count = 0

house_reg = re.compile(r'.*?<li>Property Type:<span>(.*?)</span></li>.*')

def get_html(cur_url):
    global req_headers,domain
    url = domain + cur_url
    print(url)
    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req) as res:
            return res.read()
    except Exception as e:
        print(e)
        return None

def save_one_column(parsed_result):
    global count,df
    for key in parsed_result.keys():
        df.loc[count-1, key] = parsed_result[key]
    df.loc[count-1, 'is_recorded'] = 1

def save_df():
    global df
    df.to_csv('./csvs/realestate_4000_details.csv',index=False)

def get_next_url():
    global df,count
    url = None
    try:
        if count < df.shape[0]:
            url = df.iloc[count]['url']
            count += 1
        return url
    except Exception as e:
        print(e)
        return None

def find_is_furnished(decoded_html):
    is_furnished = 0
    if find_key_words(decoded_html,'unfurnished'):
        is_furnished = 0
    else:
        is_furnished = find_key_words(decoded_html,'furnished')
    return is_furnished

def find_key_words(decoded_html, keywords):
    if type(keywords) == type(''):
        keywords = [keywords]
    for keyword in keywords:
        if decoded_html.find(keyword.lower()) >= 0:
            return 1
    return 0

def find_house_type(decoded_html):
    global house_reg
    match_result = re.search(house_reg,decoded_html)
    return match_result.group(1).strip()

def parse_html(html):
    with open('detail_test.html','wb') as f:
        f.write(html)
    decoded_html = html.decode('utf-8')
    lower_html = decoded_html.lower()
    house_type = find_house_type(decoded_html)
    is_air_conditioning = find_key_words(lower_html, ['air conditioning','air con'])
    is_sports = find_key_words(lower_html,['pool','gym'])
    is_floorboard = find_key_words(lower_html,'floorboard')
    is_outdoor = find_key_words(lower_html,['courtyard','outdoor entertaining area','balcony'])
    is_furnished = find_is_furnished(lower_html)
    is_secure = find_key_words(lower_html,['alarm','secure','intercom','fenced'])
    return {'property_type':house_type,'is_air_conditioning':is_air_conditioning, 'is_floorboard':is_floorboard,'is_furnished':is_furnished,'is_outdoor': is_outdoor,'is_sports': is_sports,'is_secure': is_secure}

def check_existing_csv():
    global df, count
    print(df.columns)
    if 'is_recorded' in df.columns and df.loc[0,'is_recorded'] == 1:
        print('Existing csv file found!')
        count = df.shape[0]-1
        while df.loc[count, 'is_recorded'] == 0:
            count -= 1
        print('Start from row',count)
    else:
        print('No existing csv found!')
        df['property_type'] = 'unknown'
        df['is_air_conditioning'] = 0
        df['is_floorboard'] = 0
        df['is_furnished'] = 0
        df['is_outdoor'] = 0
        df['is_secure'] = 0
        df['is_sports'] = 0
        df['is_recorded'] = 0

def main():
    global df,count
    check_existing_csv()
    while True:
        cur_url = get_next_url()
        if not cur_url:
            print('Reach the end.')
            save_df()
            break
        html = get_html(cur_url)
        if not html:
            continue
        parsed_result = parse_html(html)
        save_one_column(parsed_result)
        print(parsed_result)
        if count % 10 == 9:
            save_df()
            print('Saved at: ', count)

if __name__== "__main__":
    main()