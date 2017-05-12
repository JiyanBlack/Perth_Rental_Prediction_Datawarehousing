import re

with open('./useragentswitcher.xml','r') as f:
    text = f.read()
    match_result = re.match(r'useragent\=\"(.+?)\" appcodename', text)
    print(match_result)