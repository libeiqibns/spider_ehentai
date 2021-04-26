import requests
import re
import os
import time
from get_page_image import get_page_image
from multiprocessing import Process,JoinableQueue,cpu_count

heads = {
    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}

def prepare(url):
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

    match_list = re.findall(r"Showing [0-9]+ - [0-9]+ of [0-9]+ images",html)
    image_count = int(match_list[0].split(' ')[-2])
    page_count = image_count // 40 + 1

    match_list = re.findall(r"<a href=\"https://e-hentai.org/s/[0-9a-z]+/[0-9]+-[0-9]+\">",html)

    for i in range(1,page_count):
        kv = {'p':i}
        try:
            response = requests.get(url,headers=heads,params=kv)
            html = response.text
            # print(html)
        except:
            print("爬取失败")
        match_list.extend(re.findall(r"<a href=\"https://e-hentai.org/s/[0-9a-z]+/[0-9]+-[0-9]+\">",html))

    urls = [url[9:-2] for url in match_list]

    # quit()

    match_list = re.findall(r"<h1.*?/h1>",html)

    title_str=match_list[0][11:-5]

    title_str=re.sub(r'[/\\\"|<>?\*]','',title_str)

    print(title_str)
    # quit()

    if title_str != "":
        title_str = title_str+"//"

    return urls,title_str

def producer(q,urls):
    for url in urls:
        q.put(url)
    q.join()


def consumer(q,title):
    while True:
        url=q.get()
        get_page_image(url,title,verbose=True)
        # print(title,url)
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
    for url in urls:
        q = JoinableQueue()
        
        print("Crawling {0}".format(url))
        urls,title=prepare(url)
        p1 = Process(target=producer,args=(q,urls))

        consumer_list=[]
        for i in range(len(urls)):
            c=Process(target=consumer,args=(q,title))
            c.daemon = True
            consumer_list.append(c)

        p1.start()
        for c in consumer_list:
            c.start()

        p1.join()

    end_time = time.time()
    print("用时",(end_time-start_time),"秒。")
    