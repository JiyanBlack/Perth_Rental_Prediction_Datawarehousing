import urllib.request,urllib.parse
import pandas
import re
from bs4 import BeautifulSoup
from os import listdir

origin_url = "http://www.ksouhouse.com/rp.php?q=Perth&sta=wa&id="
cur_id = 1
req_headers = {'Host': 'www.realestate.com.au',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}
files = []

def next_url():
    global cur_id, origin_url, files
    while str(cur_id)+'.html' in files:
        cur_id += 1
    if cur_id >260000:
        return None
    cur_url = origin_url + str(cur_id)
    return cur_url

def get_html(cur_url):
    global req_headers
    try:
        req = urllib.request.Request(cur_url, headers=req_headers)
        with urllib.request.urlopen(req) as res:
            return res.read()
    except Exception as e:
        print(e)
        return None

# def read_progress():
#     global cur_id
#     try:
#         with open('html/download_html_progress.dat', 'r') as f:
#             cur_id = int(f.read())
#     except Exception as e:
#         print('No progress found.')
def read_progress():
    global files
    files = listdir('./html/')

def save_html(cur_html):
    global cur_id
    try:
        soup = BeautifulSoup(cur_html, 'html5lib')
        extacted = soup.find(id = 'mainT').contents[0].contents[0].contents[1].contents[0]
        with open('html/'+str(cur_id)+'.html','wb') as f:
            f.write(str(extacted).encode('utf-8'))
        # f.write(cur_html)
    except Exception as e:
        print(e)

def save_progress():
    global cur_id
    cur_id += 1
#     with open('html/download_html_progress.dat', 'w') as f:
#         f.write(str(cur_id))

def main():
    read_progress()
    url = True
    while url:
        url = next_url()
        print('Begin: ', url)
        html = get_html(url)
        if not html:
            continue
        save_html(html)
        save_progress()
        print('Finish: ',url)

if __name__=="__main__":
    main()