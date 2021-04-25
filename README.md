# spider_ehentai
用于爬取E绅士涩图的爬虫。

## 如何运行
单进程版：
```
python spider.py
```
多进程版（推荐）：
```
python spider_multip.py
```
程序开始后，输入多行e-hentai gallery url，输入"end"以结束输入。
例：
```
https://e-hentai.org/g/1896036/46f71bd9f9/
https://e-hentai.org/g/1892960/d3dcdd7e3e/
https://e-hentai.org/g/1895727/e31f33654a/
end
```
程序将依序爬取多个gallery。在当前文件夹中每个gallery创建一个文件夹。

## 我不想手动输入url，怎么办？
可以把url存入一个```.txt```文件，让程序从文件读取。然而程序没有直接支持读取文件（因为我懒没写），因此我们需要迂回解决。

### 在当前文件夹创建```url_list.txt```：
```
https://e-hentai.org/g/1896036/46f71bd9f9/
https://e-hentai.org/g/1892960/d3dcdd7e3e/
https://e-hentai.org/g/1895727/e31f33654a/
end
```
### 使用管道将```url_list.txt```重定向至标准输入流：
Windows:
```
type url_list.txt | python spider.py
```
Linux:
```
python spider.py < url_list.txt
```
Mac:

没用过，不知道，自己查
