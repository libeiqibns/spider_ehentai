import requests
import re
import os
from get_image import get_image
from progress_bar import progressbar

def crawl_webpage_recursive(url):
    heads = {
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    html = ""

    try:
        response = requests.get(url,headers=heads)
        html = response.text
    except:
        print("爬取失败")

    match_list = re.findall(r"<h1>.*?</h1>",html)
    title_str=match_list[0][4:-5]
    print(title_str)

    match_list = re.findall(r"<div><span>.*?</span></div>",html)
    page_string = match_list[0][11:-13]
    cur_page = int(page_string.split('<')[0])
    total_page = int(page_string.split('>')[-1])
    # print(cur_page,total_page)

    progressbar(0,total_page,"Crawling:",size=50)

    match_list = re.findall(r"<img id=\"img\" src=.*?>",html)
    img_url = re.split(r" ", match_list[0])[2][5:-1]
    # print(img_url)

    if title_str != "":
        title_str = title_str+"//"

    get_image(img_url,title_str)

    progressbar(cur_page,total_page,"Crawling:",size=50)

    match_list = re.findall(r"<a id=\"next\" onclick=\"return load_image.*?>",html)
    next_url = re.split(r"href=",match_list[0])[-1][1:-2]

    while next_url != url:
        url = next_url
        try:
            response = requests.get(url,headers=heads)
            html = response.text
        except:
            print("爬取失败")

        match_list = re.findall(r"<div><span>.*?</span></div>",html)
        page_string = match_list[0][11:-13]
        cur_page = int(page_string.split('<')[0])
        total_page = int(page_string.split('>')[-1])
        # print(cur_page,total_page)

        match_list = re.findall(r"<img id=\"img\" src=.*?>",html)
        img_url = re.split(r" ", match_list[0])[2][5:-1]
        # print(img_url)

        get_image(img_url,title_str)

        progressbar(cur_page,total_page,"Crawling:",size=50)

        match_list = re.findall(r"<a id=\"next\" onclick=\"return load_image.*?>",html)
        next_url = re.split(r"href=",match_list[0])[-1][1:-2]

    print('\n')

if __name__ == '__main__':
    print('Enter e-hentai image webpage urls.')
    print('Type \'end\' to finish entering.')
    line = input()
    urls = []
    while line != 'end':
        urls.append(line)
        line = input()
    
    for url in urls:
        crawl_webpage_recursive(url)
    