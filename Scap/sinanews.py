from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
import pymysql
def spyder_sinanewstop4():
    # 爬取Top4新闻标题以及来源网址
    cursor.execute('drop table if exists sinanewstop')
    cursor.execute('create table if not exists sinanewstop(newsId int(20) primary key  AUTO_INCREMENT, newsTitle varchar(500),newsSource varchar(500), newsNumber varchar(50), dateTime varchar(50), articleSource varchar(50)) character set utf8mb4')
    mysqlcon.commit()
    for newsTop4 in soup.select('.news-1'):
        for newsTop4_1 in newsTop4.select('li a'):
            # 新闻标题
            title = newsTop4_1.text
            # 新闻来源网址
            sourceUrl = newsTop4_1['href']
            newsAirticle = requests.get(newsTop4_1['href'])
            newsAirticle.encoding = 'utf-8'
            soup1 = BeautifulSoup(newsAirticle.text, 'html.parser')
            preid = soup1.find(attrs={'name': 'comment'})['content']
            # 新闻ID
            newsNumber = preid[3:]
            # 发稿日期
            date = soup1.select('.date-source span')
            if date.__len__() > 0:
                date = date[0].text.strip()
                dtime = datetime.strptime(date, '%Y年%m月%d日 %H:%M')
                articlesource = soup1.select('.source')[0].text
            else:
                dtime = '不详'
                articlesource = '不详'
            cursor.execute('insert into sinanewstop(newsTitle,newsSource,newsNumber,dateTime,articleSource)VALUES(%s,%s,%s,%s,%s)', [title, sourceUrl, str(newsNumber), str(dtime), str(articlesource)])
            mysqlcon.commit()
            # 获取top4新闻评论
            # cursor.execute('drop table if exists sinanewstopcoms')
            cursor.execute('create table if not exists sinanewstopcoms(id int(20) primary key AUTO_INCREMENT,newsTitle varchar(255),name varchar(255),comments varchar(1000),dateTime varchar(50),areaFrom varchar(50)) character set utf8mb4')
            url1 = 'http://comment.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid={}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=10&t_size=3&h_size=3&thread=1'
            url = url1.format(preid[3:])
            res1 = requests.get(url)
            # BeautifulSoup()
            res1.encoding = 'utf-8'
            # print(str(res1.text))
            newres1 = res1.text
            print(newres1)
            jsonres1 = json.loads(newres1)
            print(type(jsonres1))
            if jsonres1['result']['cmntlist']:
                for i in range(len(jsonres1['result']['cmntlist'])):
                        nick = jsonres1['result']['cmntlist'][i]['nick']
                        content = jsonres1['result']['cmntlist'][i]['content']
                        time = jsonres1['result']['cmntlist'][i]['time']
                        area = jsonres1['result']['cmntlist'][i]['area']
                        cursor.execute('insert into sinanewstopcoms(newsTitle, name, comments, dateTime, areaFrom)VALUES(%s,%s,%s,%s,%s)',[title, nick, str(content), time, area])
                        mysqlcon.commit()

def spyder_sinanewstop5_15():
    # 获取Top5-14的新闻信息
    for newsTop5_14 in soup.select('.news-2'):
        for newsTop5_14_1 in newsTop5_14.select('li a'):
            # 新闻标题
            title = newsTop5_14_1.text
            # 新闻来源网址
            sourceUrl = newsTop5_14_1['href']
            newsAirticle = requests.get(newsTop5_14_1['href'])
            newsAirticle.encoding = 'utf-8'
            soup1 = BeautifulSoup(newsAirticle.text, 'html.parser')
            preid = soup1.find(attrs={'name': 'comment'})['content']
            # 新闻ID
            newsNumber = preid[3:]
            # 发稿日期
            date = soup1.select('.date-source span')
            if date.__len__() > 0:
                date = date[0].text.strip()
                dtime = datetime.strptime(date, '%Y年%m月%d日 %H:%M')
                articlesource = soup1.select('.source')[0].text
            else:
                dtime = '不详'
                articlesource = '不详'
            cursor.execute('insert into sinanewstop(newsTitle,newsSource,newsNumber,dateTime,articleSource)VALUES(%s,%s,%s,%s,%s)', [title, sourceUrl, str(newsNumber), str(dtime), str(articlesource)])
            mysqlcon.commit()
            # 获取top获取新闻评论
            # cursor.execute('drop table if exists sinanewstopcoms')
            # cursor.execute('create table if not exists sinanewstopcoms(id int(20) primary key AUTO_INCREMENT,newsTitle varchar(255),name varchar(255),comments varchar(1000),dateTime varchar(50),areaFrom varchar(50)) character set utf8mb4')
            url1 = 'http://comment.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid={}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=10&t_size=3&h_size=3&thread=1'
            url = url1.format(preid[3:])
            print('跳转的地址是：' + url)
            res1 = requests.get(url)
            # BeautifulSoup()
            res1.encoding = 'utf-8'
            # print(str(res1.text))
            newres1 = res1.text
            print(newres1)
            jsonres1 = json.loads(newres1)
            print(type(jsonres1))
            if jsonres1['result']['cmntlist']:
                for i in range(len(jsonres1['result']['cmntlist'])):
                    nick = jsonres1['result']['cmntlist'][i]['nick']
                    content = jsonres1['result']['cmntlist'][i]['content']
                    time = jsonres1['result']['cmntlist'][i]['time']
                    area = jsonres1['result']['cmntlist'][i]['area']
                    cursor.execute('insert into sinanewstopcoms(newsTitle, name, comments, dateTime, areaFrom)VALUES(%s,%s,%s,%s,%s)',[title, nick, str(content), time, area])
                    mysqlcon.commit()
            else:
                cursor.execute(
                    'insert into sinanewstopcoms(newsTitle, name, comments, dateTime, areaFrom)VALUES(%s,%s,%s,%s,%s)',
                    [title, '', '', '', ''])
                mysqlcon.commit()
# 抓取数据存放到文件中
# 抓取top4新闻信息
def top4news_file():
    with open('F:\sinatop4.txt', 'w', encoding='utf-8') as f:
        for news0 in soup.select('.news-1'):
            print("开始抓取数据...")
            print("热门事件Top4")
            for news1 in news0.select('li a'):
                print('新闻标题：'+news1.text)
                print('来源网址：'+news1['href'])
                title = news1.text
                sourceUrl = news1['href']
                newsAirticle = requests.get(news1['href'])
                newsAirticle.encoding = 'utf-8'
                soup1 = BeautifulSoup(newsAirticle.text, 'html.parser')
                preid = soup1.find(attrs={'name': 'comment'})['content']
                newsNumber = preid[3:]
                # 发稿日期
                date = soup1.select('.date-source span')
                if date.__len__() > 0:
                    date = date[0].text.strip()
                    dt = datetime.strptime(date, '%Y年%m月%d日 %H:%M')
                    print(dt)
                    ds = soup1.select('.source')[0]
                    print('消息来源：  ' + ds.text)
                else:
                    print('没有日期署名')
                f.write('新闻标题：{}， 新闻来源网址：{}， 新闻编号：{}，日期：{}，新闻出处：{}\n'.format(title, sourceUrl, newsNumber, dt, ds))
                # 取出评论
                url1 = 'http://comment.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid={}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=10&t_size=3&h_size=3&thread=1'
                url = url1.format(preid[3:])
                print('跳转的地址是：' + url)
                res1 = requests.get(url)
                # BeautifulSoup()
                res1.encoding = 'utf-8'
                # print(str(res1.text))
                newres1 = res1.text
                print(newres1)
                jsonres1 = json.loads(newres1)
                print(type(jsonres1))
                if jsonres1['result']['cmntlist']:
                    for i in range(len(jsonres1['result']['cmntlist'])):
                        with open('F:\sinatop4coms.txt', 'a', encoding='utf-8') as f1:
                            print('网友：' + jsonres1['result']['cmntlist'][i]['nick'])
                            print('评论：' + jsonres1['result']['cmntlist'][i]['content'])
                            print('评论时间：' + jsonres1['result']['cmntlist'][i]['time'])
                            print('地区：' + jsonres1['result']['cmntlist'][i]['area'])
                            nick = jsonres1['result']['cmntlist'][i]['nick']
                            f1.write('网友名字：{}\n'.format(nick))
                            content = jsonres1['result']['cmntlist'][i]['content']
                            f1.write('评论内容：{}\n'.format(content))
                            time = jsonres1['result']['cmntlist'][i]['time']
                            f1.write('评论时间：{}\n'.format(time))
                            area = jsonres1['result']['cmntlist'][i]['area']
                            f1.write('地区：{}\n'.format(area))
                else:
                    print('还没有人评论')
# 抓取top5-15到文件当中
def top5_15_file():
    with open('F:\sinatop5-15.txt', 'w', encoding='utf-8') as f:
        for news0 in soup.select('.news-2'):
            for news1 in news0.select('li a'):
                print('')
                if news1.find_parent().attrs:
                    print('这个是广告')
                else:
                    print('新闻标题：'+news1.text)
                    print('来源网址：'+news1['href'])
                    title = news1.text
                    sourceUrl = news1['href']
                    resAirticle = requests.get(news1['href'])
                    resAirticle.encoding = 'utf-8'
                    soup1 = BeautifulSoup(resAirticle.text, 'html.parser')
                    preid = soup1.find(attrs={'name': 'comment'})['content']
                    newsNumber = preid[3:]
                    print('新闻id是：' + preid[3:])
                    # title = soup1.find_all(attrs={"name": "comment"})
                    # print("meta包含的内容是："+title.text)
                    # 新闻文章正文
                    print("正文：")
                    print(''.join([article.text.strip() for article in soup1.select('#article p')[:-1]]))
                    # 发稿日期
                    date = soup1.select('.date-source span')
                    if date.__len__() > 0:
                        date = date[0].text.strip()
                        dt = datetime.strptime(date, '%Y年%m月%d日 %H:%M')
                        print(dt)
                        ds = soup1.select('.source')[0]
                        print('消息来源：  '+ds.text)
                    else:
                        print('没有日期署名')
                    # 取出责任编辑(作者)
                    author = soup1.select('.show_author')[0].text.lstrip('责任编辑：')
                    print('作者:'+author)
                    f.write('新闻标题：{}， 新闻来源网址：{}， 新闻编号：{}，日期：{}，新闻出处：{}\n'.format(title, sourceUrl, newsNumber, dt, ds))
                    # 获取评论
                    # print('爬取的评论代码：'+comments[0].text)
                    url1 = 'http://comment.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid={}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=10&t_size=3&h_size=3&thread=1'
                    url = url1.format(preid[3:])
                    print('跳转的地址是：'+url)
                    res1 = requests.get(url)
                    # BeautifulSoup()
                    res1.encoding = 'utf-8'
                    # print(str(res1.text))
                    newres1 = res1.text
                    print(newres1)
                    jsonres1 = json.loads(newres1)
                    print(type(jsonres1))
                    if jsonres1['result']['cmntlist']:
                        for i in range(len(jsonres1['result']['cmntlist'])):
                            with open('F:\sinatop5_15coms.txt', 'a', encoding='utf-8') as f1:
                                print('网友：' + jsonres1['result']['cmntlist'][i]['nick'])
                                print('评论：' + jsonres1['result']['cmntlist'][i]['content'])
                                print('评论时间：' + jsonres1['result']['cmntlist'][i]['time'])
                                print('地区：' + jsonres1['result']['cmntlist'][i]['area'])
                                nick = jsonres1['result']['cmntlist'][i]['nick']
                                f1.write('网友名字：{}\n'.format(nick))
                                content = jsonres1['result']['cmntlist'][i]['content']
                                f1.write('评论内容：{}\n'.format(content))
                                time = jsonres1['result']['cmntlist'][i]['time']
                                f1.write('评论时间：{}\n'.format(time))
                                area = jsonres1['result']['cmntlist'][i]['area']
                                f1.write('地区：{}\n'.format(area))
                    else:
                        print('还没有人评论')

if __name__ =='__main__':
    print('开始爬虫')
    mysqlcon = pymysql.Connect("localhost", "bzq", "123456", "sina")
    cursor = mysqlcon.cursor()
    res = requests.get('https://news.sina.com.cn/china/')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    i = 0
    spyder_sinanewstop4()
    spyder_sinanewstop5_15()
    top4news_file()
    top5_15_file()
    print('爬虫结束')






