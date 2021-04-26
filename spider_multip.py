import requests
import re
import os
import time
from get_image import get_image
from multiprocessing import Process,JoinableQueue,cpu_count

PROC_COUNT = 12

heads = {
    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}

def crawl_webpage_recursive(url):
    html = ""
    try:
        response = requests.get(url,headers=heads)
        html = response.text
        # print(html)
    except:
        print("爬取失败")

    offensive_flag = re.search(r"<p>This gallery has been flagged as <strong>Offensive For Everyone</strong>.",html)

    if offensive_flag != None:
        kv = {'nw':"always"}
        try:
            response = requests.get(url,headers=heads,params=kv)
            html = response.text
            # print(html)
        except:
            print("爬取失败")

    enb_index = re.search(r"<img alt=.*?>",html).start()
    url = re.findall("<a href=.*?>", html[:enb_index])[-1][9:-2]

    match_list = re.findall(r"<h1.*?/h1>",html)

    title_str=match_list[0][11:-5]

    title_str=re.sub(r'[/\\\"|<>?\*]','',title_str)

    print(title_str)
    # quit()

    if title_str != "":
        title_str = title_str+"//"

    return url,title_str


def producer(q, url):
    prev_url=""
    while prev_url != url:
        try:
            response = requests.get(url,headers=heads)
        except:
            print("爬取失败")

        match_list = re.findall(r"<img id=\"img\" src=.*?>",response.text)
        img_url = re.split(r" ", match_list[0])[2][5:-1]
        # print(img_url)

        q.put(img_url)

        match_list = re.findall(r"<a id=\"next\" onclick=\"return load_image.*?>",response.text)
        prev_url = url
        url = re.split(r"href=",match_list[0])[-1][1:-2]


    q.join()

def consumer(q,title):
    while True:
        img_url=q.get()
        get_image(img_url,title,verbose=True)
        q.task_done()#发送信号给生产者的q.join()说，已经处理完从队列中拿走的一个项目


if __name__ == '__main__':
    print('Enter e-hentai gallery urls.')
    print('Type \'end\' to finish entering.')
    line = input()
    urls = []
    while line != 'end':
        urls.append(line)
        line = input()
    

    start_time = time.time()
    i = 0
    for url in urls:
        i=i+1
        url,title_str=crawl_webpage_recursive(url)
        print("Crawling {0}".format(url))

        q = JoinableQueue()
        p1 = Process(target=producer,args=(q,url))

        consumer_list=[]
        for i in range(PROC_COUNT):
            c=Process(target=consumer,args=(q,title_str))
            c.daemon = True
            consumer_list.append(c)

        p1.start()
        for c in consumer_list:
            c.start()

        p1.join()

    end_time = time.time()
    print("用时",(end_time-start_time),"秒。")
    