# -*- coding: utf-8 -*-
import urllib3
import traceback
import json
import certifi
import random
import requests
import time
import re
import os
# import MongoDB
from PIL import Image
from urllib3.contrib.socks import SOCKSProxyManager


#just a test
url = "https://game.nihaoma.top/t1/?template=blue&token=b595fa57&CateID=10#/"


http = urllib3.PoolManager(
    cert_reqs = 'CERT_REQUIRED',
    ca_certs = certifi.where()
)
######## 访问某些网站使用本地ssr代理
proxy = urllib3.ProxyManager('http://127.0.0.1:1087',
                             'https://127.0.0.1:1087')

sockproxy = SOCKSProxyManager('socks5://localhost:1086')



'''
通过ssr代理访问 端口1080 
无Referer
'''
# def visitByProxy(url):
#     try:
#         web = proxy.request('GET', url,
#                                  headers={
#                                      'User-Agent':
#                                          'ozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'
#                                      , 'accept-language': "zh-CN,zh;q=0.9,zh-TW;q=0.8"
#                                      # "Host": "www.google.com",
#                                      #  'Referer':" https://www.google.com/"
#                                  })
#     #except BaseException:
#     except Exception:
#
#         print(Exception)
#         print("error")
#         return "error"
#     else:
#         print(web.status)
#         return web

def visitByProxy(url):
    # web = proxy.request('GET', url,
    #                         headers={
    #                             'User-Agent':
    #                                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    #                             , 'accept-language': "zh-CN,zh;q=0.9,zh-TW;q=0.8"
    #                             #"Host": "www.google.com"
    #                             #'Referer': " https://www.google.com/"
    #                         })
    # return web
    i = 0
    while i < 3:
        try:
            web = proxy.request('GET', url,
                               headers={
                                   'User-Agent':
                                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36 LBBROWSER'
                                   , 'accept-language': "zh-CN,zh;q=0.9,zh-TW;q=0.8"
                               },
                               timeout = 20
                               )
            print(web.status)
            return web
        except requests.exceptions.RequestException as e:
            print(e)
            print("retry "+i)
            i = i +1
    return "error"



'''
直接通过本地IP访问 获取html 
无Referer
'''
# def visitByLocalNet(url):
#     try:
#         web = http.request('GET', url,
#                            headers={
#                                'User-Agent':
#                                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36 LBBROWSER'
#                                , 'accept-language': "zh-CN,zh;q=0.9,zh-TW;q=0.8"
#                            },
#                            )
#         print(web.status)
#     except BaseException:
#         print("error"+url)
#         return "error"
#     else:
#         return web


def visitByLocalNet(url):
    i = 0
    while i < 3:
        try:
            web = http.request('GET', url,
                               headers={
                                   'User-Agent':
                                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36 LBBROWSER'
                                   , 'accept-language': "zh-CN,zh;q=0.9,zh-TW;q=0.8"
                               },
                               timeout = 20
                               )
            print(web.status)
            return web
        except requests.exceptions.RequestException as e:
            print(e)
            print("retry "+i)
            i = i +1
    return "error"


'''
通过ssr代理访问 端口1080 
带Referer
'''
def visitByProxyRef(url , Referer):
    try:
        web = proxy.request('GET', url,
                            headers={
                                'User-Agent':
                                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36 LBBROWSER'
                                 ,'Referer': Referer
                                , 'accept-language': "zh-CN"
                            })
    except BaseException:
        print()
        print("error")
        return "error"
    else:
        print(web.status)
        return web


'''
直接本地IP进行访问
添加Referer
'''
def visitByLocalNetRef(url,Referer):
    try:
        web = http.request('GET', url,
                           headers={
                               'User-Agent':
                                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36 LBBROWSER'
                               , 'Referer': Referer
                               , 'accept-language': "zh-CN,zh;q=0.9,zh-TW;q=0.8"
                           },
                           )
        print(web.status)
    except BaseException:
        print("error" + url)
        return "error"
    else:
        return web

###爬去图片 然后根据图片的尺寸或者大小进行筛选
#######################################################################################################################
###通过获取的html文件来读取其中的图片的url
def getImageUrl(web):
    print("getImageList")
    #设置正则匹配项
    req = r'src="(.+?\.jpg)"'
    imgreq = re.compile(req)
    imglist = re.findall(imgreq, web.data.decode('utf-8'))
    return imglist


###通过图片的URL来进行下载
def downloadImage(imglist,name):
    fileIndex = 0
    print("Download")
    for i in imglist:
        print(imglist)
        f = open('d:/picture/'+name+str(fileIndex)+'.jpg','wb')
        img = visitByProxy(i)
        f.write(img.data)
        fileIndex = fileIndex+1
        ###需要的图片在第一张
        break

###通过图片的像素进行筛选
def clearUselessImageByPix(path):
    for i in os.walk(path):
        for file in i[2]:
            img = Image.open(path+file)
            img.close()
            if img.size >= (574,384):
                print(file+"ok")
            else:
                os.remove(path+file)
                print(file+"delete")

###通过图片的尺寸进行筛选
def clearUselessImageBySize(path,pictureSize):
    for i in os.walk(path):
        for file in i[2]:
            fsize = os.path.getsize(path+file)
            fsize = fsize / float(1024)  ##KB
            if fsize < pictureSize:
                os.remove(path+file)
                print(file+"delete")
            else:
                print(file+"ok")

###获取文件尺寸
def getFileSize(path):
    fsize = os.path.getsize(path)
    fsize = fsize/float(1024) ##KB
    return round(fsize,1)#返回一位小数
########################################################################################################################


'''
<span data-v-2f74c3b4="" title="Revenge" class="player-code roboto mrr5">Revenge</span> ##Revenge
<span data-v-2f74c3b4="" title="Hero Gaming" class="player-code roboto mrl5">Hero Gaming</span>

'''

'''

<i data-v-2f74c3b4="" class="roboto-bold">2.07</i>

<i data-v-2f74c3b4="" class="roboto-bold">1.82</i>
'''
##

def getBuffTextData(web):
    reqTitle = r'title="(.)"'

#

'''
从html页面中获取到当前页面的出售物品信息
其中包括物品的
名称
价格
数量
将其存储到数据库中
'''
def getC5TextData(web,index):
    '''
    匹配所有的 sell item
    这些正则表达式需要根据实际的返回html文件进行调整
    '''
    req = r'<li class="selling">(.+?)</li>'
    nameR = r'<span class=" .+? ">(.+?)</span>'
    priceR = r'<span class="price">￥ (.+?)</span>'
    numberR = r'<span class="num">(.+?)</span>'
    soleR = r'^([0-9]+?)[^0-9]+'
    soleRC = re.compile(soleR)
    matchlist = re.findall(req, web.data.decode("UTF-8"), re.S)
    print(matchlist)
    #每个Item提取对应的 物品名称 价格 数量
    for i in matchlist:
        name = re.findall(nameR, i, re.S)[0]
        price = re.findall(priceR, i, re.S)[0]
        #numberO 中带有中文描述符 不是纯数字
        numberO = re.findall(numberR, i, re.S)[0]
        number = re.findall(soleR,numberO)[0]
        #print(name)
        MongoDB.insert("c5",name,price,number,index)
        #MongoDB.SaveName(name)
        #数据处理之后将其存入数据库中


'''
Html页面获取Nice
'''
def getNiceTextData(web,index):
    req = r'<div class="sneakerItem"(.+?)</div></div></div>'
    name = r'<div class="bottom">(.+?)$'
    number = r'<div class="count">(.+?)[^0-9]+</div></div>'
    price = r'<div class="num">(.+?)</div></div>'
    id = r'gid="(.+?)"'
    matchlist = re.findall(req, web.data.decode("UTF-8"), re.S)
    for i in matchlist:
        nameR = re.findall(name,i,re.S)[0]
        priceR = re.findall(price, i, re.S)[0]
        numberR = re.findall(number, i, re.S)[0]
        idR = re.findall(id,i,re.S)[0]
        MongoDB.insert("nice",nameR,priceR,numberR,index)
