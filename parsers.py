import re

html_tags_re = re.compile('<.*?>')
not_alpha_re = re.compile('[^a-zA-Z]')

def cleanhtml(raw_html):
    result = re.sub(html_tags_re, ' ', raw_html)
    result = re.sub(not_alpha_re, ' ', result)
    return result

def merge_map(kmap, kitems):
    for item in kitems:
        s = item.capitalize()
        if s in kmap:
            kmap[s] += 1
        else:
            kmap[s] = 1

def collect(keys_map, desc):
    items = cleanhtml(desc).split()
    merge_map(keys_map, items)
    result = dict(sorted(keys_map.items(), key=lambda item: item[1], reverse=True))
    return result

if __name__ == '__main__':
    keys_map = {}
    with open('test1.data') as f:
        keys_map = collect(keys_map, f.read())
    with open('test2.data') as f:
        keys_map = collect(keys_map, f.read())
    print(keys_map)
