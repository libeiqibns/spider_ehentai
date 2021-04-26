import requests
import re
from get_image import get_image

def get_page_image(url,title,verbose=False):
    html=""
    heads = {
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    try:
        response = requests.get(url,headers=heads)
        html = response.text
    except:
        print("爬取失败")

    match_list = re.findall(r"<img id=\"img\" src=.*?>",html)
    
    img_url = re.split(r" ", match_list[0])[2][5:-1]

    get_image(img_url,title,verbose)

if __name__ == '__main__':
    get_page_image("https://e-hentai.org/s/627fb1001f/1810644-1", 'test//')