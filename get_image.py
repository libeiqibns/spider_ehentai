import requests
import os

def get_image(url,title):
    filename = url.split('/')[-1]
    path = title+filename
    try:
        if not os.path.exists(title):
            os.mkdir(title)
        if not os.path.exists(path):
            r = requests.get(url)
            with open (path, 'wb') as f:
                f.write(r.content)
                f.close()
                # print("文件保存成功",path)
        else:
            pass
            # print("文件已存在",path)
    except:
        print("爬取失败")

if __name__ == '__main__':
    print("Enter image url:")
    url = input()
    get_image(url,"")
