from urllib import *
from urllib import request
from sys import *
import os
from time import *
from threading import *
from lxml import etree

def get_page(url):
    response=request.urlopen(url)
    html=response.read()
    return html

def get_content(html):
    root=etree.HTML(html)
    cont_list=[]
    p_list=root.xpath('//*[@class="chapter_content"]')
    for item in p_list:
        contents=item.xpath('p')
        strings=''
        for con in contents:
            text=con.text
            print(text)
            cont_list.append(text)
    return cont_list


def write(filename,cont):   #创建文件写入
    f=open(filename,'a',encoding="utf-8")
    for item in cont:
        if(item!=None):
            f.write(item+'\r\n')
    f.close()


def download():
    for i in range(1000):
        print(i)
        cur_url=domain+'/%d.html'%(i+1)
        print('cur_url_%d:'%(i+1)+cur_url)
        html=get_page(cur_url)
        cont=get_content(html)
        #print(cont)
        filename=site+'%d.txt'%(i+1)
        write(filename,cont)



domain='http://www.shicimingju.com/book/xiyouji'
site='f://xiyouji/'
if(os.path.exists('f://xiyouji')==False):
    os.mkdir('f://xiyouji')
threads=[]
threads.append(Thread(target=download,args=()))
for t in threads:
    t.start()
    t.join

