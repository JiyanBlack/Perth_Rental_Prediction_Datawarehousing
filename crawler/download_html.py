import urllib.request,urllib.parse
import pandas
import re
from bs4 import BeautifulSoup
from os import listdir
import pickle
import gzip
from io import StringIO
from multiprocessing import Pool

origin_url = "http://www.ksouhouse.com/p.php?q=Perth&sta=wa&id="
cur_id = 1
req_headers = {
'Host': 'www.ksouhouse.com',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}
files = []
pending_ids = []

def next_url():
    global cur_id, origin_url, files
    if cur_id >260000:
        return None
    cur_url = origin_url + str(cur_id)
    return cur_url

def get_url(id):
    cur_url = origin_url + str(id)
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
    global files,cur_id, pending_ids
    files = listdir('./html/')
    file_ids = [int(i.split('.')[0]) for i in files]
    file_ids.sort()
    pending_ids = [i for i in range(1,890000)]
    for i in file_ids:
        pending_ids.remove(i)
    try:
        cur_id = file_ids[-1]
    except Exception as e:
        cur_id = 1
    return cur_id

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
        # save_invalid()
def save_id_html(cur_html,id):
    global pending_ids
    try:
        soup = BeautifulSoup(cur_html, 'html5lib')
        extacted = soup.find(id = 'mainT').contents[0].contents[0].contents[1].contents[0]
        with open('html/'+str(id)+'.html','wb') as f:
            f.write(str(extacted).encode('utf-8'))
            pending_ids.remove(id)
    except Exception as e:
        print(e)

def save_progress():
    global cur_id
    cur_id += 1
#     with open('html/download_html_progress.dat', 'w') as f:
#         f.write(str(cur_id))

def download_one_html(id):
    url = get_url(id)
    print('Begin: ', url)
    html = get_html(url)
    if not html:
        print("Invalid: ", url)
    save_id_html(html,id)
    print('Finish: ',url)

def main():
    global cur_id,pending_ids
    while True:
        cur_id = read_progress()
        p = Pool(16)
        for i in pending_ids:
            p.apply_async(download_one_html, args=(i,))
        if len(pending_ids)==0:
            break
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')
    # url = True
    # while url:
    #     url = next_url()
    #     print('Begin: ', url)
    #     html = get_html(url)
    #     if not html:
    #         continue
    #     save_html(html)
    #     print('Finish: ',url)

if __name__=="__main__":
    main()