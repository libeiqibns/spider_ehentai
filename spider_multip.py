import requests
import re
import os
from get_image import get_image
from progress_bar import progressbar
from multiprocessing import Process,JoinableQueue,cpu_count

PROC_COUNT = cpu_count()

heads = {
    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}

def crawl_webpage_recursive(url):
    html = ""
    try:
        response = requests.get(url,headers=heads)
        html = response.text
    except:
        print("爬取失败")

    enb_index = re.search(r"<img alt=.*?>",html).start()
    url = re.findall("<a href=.*?>", html[:enb_index])[-1][9:-2]

    return url


def producer(q, url):
    html=""
    try:
        response = requests.get(url,headers=heads)
        html = response.text
    except:
        print("爬取失败")

    match_list = re.findall(r"<h1>.*?</h1>",html)

    title_str=match_list[0][4:-5]
    print(title_str)

    match_list = re.findall(r"<img id=\"img\" src=.*?>",html)
    img_url = re.split(r" ", match_list[0])[2][5:-1]
    # print(img_url)

    if title_str != "":
        title_str = title_str+"//"

    match_list = re.findall(r"<a id=\"next\" onclick=\"return load_image.*?>",html)
    next_url = re.split(r"href=",match_list[0])[-1][1:-2]
    q.put((img_url,title_str))
    while next_url != url:
        url = next_url
        try:
            response = requests.get(url,headers=heads)
            html = response.text
        except:
            print("爬取失败")

        match_list = re.findall(r"<img id=\"img\" src=.*?>",html)
        img_url = re.split(r" ", match_list[0])[2][5:-1]
        # print(img_url)

        q.put((img_url,title_str))

        match_list = re.findall(r"<a id=\"next\" onclick=\"return load_image.*?>",html)
        next_url = re.split(r"href=",match_list[0])[-1][1:-2]

    q.join()

def consumer(q):
    while True:
        img_url,title_str=q.get()
        get_image(img_url,title_str,verbose=True)
        q.task_done()#发送信号给生产者的q.join()说，已经处理完从队列中拿走的一个项目


if __name__ == '__main__':
    print('Enter e-hentai gallery urls.')
    print('Type \'end\' to finish entering.')
    line = input()
    urls = []
    while line != 'end':
        urls.append(line)
        line = input()
    
    i = 0
    for url in urls:
        i=i+1
        url=crawl_webpage_recursive(url)
        print("Crawling {0}".format(url))

        q = JoinableQueue()
        p1 = Process(target=producer,args=(q,url))

        consumer_list=[]
        for i in range(PROC_COUNT):
            c=Process(target=consumer,args=(q,))
            c.daemon = True
            consumer_list.append(c)

        p1.start()
        for c in consumer_list:
            c.start()

        p1.join()
    