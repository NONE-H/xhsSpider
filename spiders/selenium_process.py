
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
# from webdriver_manager.chrome import ChromeDriverManager
import PySimpleGUI as sg
import time
import re
import random
import json
from utils import *

def urlProcess(word):
    file = open(f'./data/{word}_fiddler.txt','r',encoding='utf-8')
    if file==None:
        print(f'未找到./data/{word}_fiddler.txt')
        print('------------------------------------\n')
        print('请检查修改您的默认fiddler文件保存位置,file->save->selected all sessions->as text')
        print('将其默认保存路径手动改为该文件夹下/data,以便后续使用')
        print('\n------------------------------------\n')
        
        print(f'对于该文件: {word}_fiddler.txt')
        print(f'您可将它移动到/data文件夹下,执行如下命令以单独解析此文件')
        print(f'\n python main.py {word} -f \n')
        exit(0)
    file_data = file.read()
    
    base_url = "https://www.xiaohongshu.com/discovery/item/"
    
    pattern = re.compile(r'"se_pr":"([\d\w]*)"',re.U)
    ids = pattern.findall(file_data)
    
    url = []
    for id in ids:
        if len(id)==24:
            url.append(base_url+id)
    
    url = list(set(url))
    print(f'{word}文章的有效地址数量为: {len(url)}')
    return url
    

def startBrower():
    # opt = Options()
    # opt.add_argument('--no-sandbox')                # 解决DevToolsActivePort文件不存在的报错
    # opt.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
    # opt.add_argument('blink-settings=imagesEnabled=false')      # 不加载图片，提升运行速度
    # #opt.add_argument('--headless')                  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
    # opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    option = webdriver.ChromeOptions()
    # option.add_argument(r'--user-data-dir=C:\Users\11422\AppData\Local\Google\Chrome\User Data1')
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # driver = webdriver.Chrome(options=option,executable_path=r"./chromedriver.exe")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    return driver

def getXHScontent(word):
    URL = urlProcess(word)
    articles = []
    brower = startBrower()
    provincesAll = provinces()
    for id,url in enumerate(URL):
        if id%20==0:
            print('---------------------')
            print(f'已完成 {id}/{len(URL)}')
            print('---------------------')
        print(f'正在访问 {url}')
        # selenium 自动化爬虫方法
        brower.get(url)
        time.sleep(8)
        article = ""
        video = ""
        imgListUrl = []
        commentsListUrl = []
        contents_1 = brower.find_elements(by=By.TAG_NAME,value="p")
        contents_2 = brower.find_elements(by=By.CLASS_NAME,value="as-p")
        avatarImg = brower.find_element(by=By.XPATH,value="//div[@class='left-img']/img")
        author = brower.find_element(by=By.XPATH, value="//span[@class='name-detail']")
        imgList = brower.find_elements(by=By.XPATH,value="//ul[@class='slide']/li/span")
        writeTime = brower.find_element(by=By.XPATH, value="//div[@class='publish-date']/span")
        commentsList = brower.find_elements(by=By.XPATH, value="//div[@class='all-tip']/div[@class='content']/div[@class='comment']")
        for i in imgList:
            pat = re.compile('url\("(.*)"\)')
            imgListUrl.append(re.search(pat, i.get_attribute('style')).group(1))
        if len(imgList) == 0:
            video = brower.find_element(by=By.XPATH, value="//div[@class='videoframe']/video")
            videoSrc = video.get_attribute('src')
        for i in commentsList:
            commentAvatar = i.find_element(by=By.XPATH, value=".//div[@class='avatar-img cube-image normal-image']/img").get_attribute('src')
            commentUserName = i.find_element(by=By.XPATH, value=".//div[@class='user-info']//a").text
            commentTime = i.find_element(by=By.XPATH, value=".//div[@class='user-info']/span").text
            commentContent = i.find_element(by=By.XPATH, value="./p[@class='content']").text
            commentsListUrl.append({
                'commentAvatar':commentAvatar,
                'commentUserName':commentUserName,
                'commentTime':commentTime,
                'commentContent':commentContent
            })
        try:
            heartCount = brower.find_element(by=By.XPATH, value="//span[@class='like-sum']")
            heartCounts = heartCount.text
        except:
            heartCounts = random.randint(0,10000)

        careArticleLen = random.randint(9,10)

        type = word
        for content in contents_1:
            words = content.text
            if words.find("一起来分享给朋友们看看吧")==-1:
                article+=words
            else:
                break
        for content in contents_2:
            words = content.text
            article+=words
        print(f'文章字数: {len(article)}')
        if len(article)==0:
            continue

        articles.append({
            "url":url,
            "content":article,
            'avatarImg':avatarImg.get_attribute('src'),
            'authorName':author.text,
            'writeTime':writeTime.text,
            'heartCount':heartCounts,
            'careArticleLen':careArticleLen,
            'address':provincesAll[random.randint(0,len(provincesAll)-1)],
            'type':type,
            'imgList':"https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fi1.hdslb.com%2Fbfs%2Farchive%2F8faf492337fbdc3443236de7fe45ba12676a3ba4.png&refer=http%3A%2F%2Fi1.hdslb.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1658999944&t=2c0ccab841f5812bef3fb6b8ff831f7c" if len(imgListUrl) == 0 else ','.join(imgListUrl),
            'comments':json.dumps(commentsListUrl),
            'videoSrc':0 if video == "" else videoSrc
        })
        saveArticles(word, articles)
    print('---------------------')
    print(f'有效文章数量为{len(articles)}')
    print('---------------------')
    return articles

