#coding='UTF-8'
import lxml
from lxml import etree
import requests
import os
import pymongo
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
def get_douban_urls(str_url):
    str_response=requests.get(str_url,headers=headers)
    str_html=str_response.text
    str_selectors=etree.HTML(str_html)
    douban_url=str_selectors.xpath('//td[@valign="top"]/div/a/@href')
    return douban_url
def movie_spider(each_url):
    response=requests.get(each_url)
    html=response.text
    selector=lxml.etree.HTML(html)
    mingzi=selector.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
    daoyan=selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0]
    riqi=selector.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/@content')[0]
    pingfeng=selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
    leixing_orgin=selector.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')
    leixing=''.join(leixing_orgin)
    database_info(str(mingzi),str(daoyan),str(riqi),leixing,str(pingfeng))
def database_info(mingzi,daoyan,riqi,leixing,pingfeng):
    con=pymongo.MongoClient("localhost",27017)
    douban_db=con.douban
    douban_table=douban_db.movie
    movie_info={}
    movie_info["电影名字"]=mingzi
    movie_info["导演"]=daoyan
    movie_info["上映日期"]=riqi
    movie_info["类型"]=leixing
    movie_info["评分"]=pingfeng
    douban_table.insert(movie_info)
if __name__ == "__main__":
    str_url="https://movie.douban.com/chart"
    douban_url=get_douban_urls(str_url)
    for each_url in douban_url:
        movie_spider(each_url)
