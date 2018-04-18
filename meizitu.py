#coding='UTF-8'
import requests
import lxml.etree
import random
import chardet
import os
import time
from lxml import etree
import logging
logging.basicConfig(level=logging.DEBUG,filename="./logs/meizitu_log",filemode='w',
                   format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname) - %(message)s')
logging.info('this is a loggging info message') 
logging.debug('this is a loggging debug message') 
logging.warning('this is loggging a warning message') 
logging.error('this is an loggging error message') 
logging.critical('this is a loggging critical message') 
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
def get_all_pages():
    for offset in range(1,17):
        str_url="http://www.meizitu.com/a/sexy_"+str(offset)+".html"
        yield(str_url)
def get_each_url(str_url):
    response=requests.get(str_url,headers={'User-Agent':random.choice(USER_AGENTS)})
    response.encoding='gbk'
    html=response.text
    selector=etree.HTML(html)
    urls=selector.xpath('//li[@class="wp-item"]/div/h3/a/@href')
    for each_url in urls:
        res=requests.get(each_url,headers={'User-Agent':random.choice(USER_AGENTS)})
        res.encoding='gbk'
        each_html=res.text
        each_selector=etree.HTML(each_html)
        each_title=each_selector.xpath('//div[@class="metaRight"]/h2/a/text()')[0]
        each_img_url=each_selector.xpath('//div[@id="picture"]/p/img/@src')
        each_img_name=each_selector.xpath('//div[@id="picture"]/p/img/@alt')
        if os.path.exists('/root/python/meizitu_img/'+each_title):
            print(each_title+"目录存在,开始下载")
            os.chdir('/root/python/meizitu_img/'+each_title)
            for i in range(0,len(each_img_url)):
                if os.path.exists(each_img_name[i]):
                    print(each_img_name[i]+"下载已完成")
                else:
                    each_img=requests.get(each_img_url[i],headers={'User-Agent':random.choice(USER_AGENTS)})
                    time.sleep(2)
                    with open(str(each_img_name[i]),'wb') as fp:
                        fp.write(each_img.content)
                        fp.close()
                        print(each_img_name[i]+"下载完成")
        else:
            print(each_title+"目录不存在，创建目录并下载")
            os.mkdir('/root/python/meizitu_img/'+each_title)
            os.chdir('/root/python/meizitu_img/'+each_title)
            for i in range(0,len(each_img_url)):
                if os.path.exists(each_img_name[i]):
                    print(each_img_name[i]+"下载已完成")
                else:
                    each_img=requests.get(each_img_url[i],headers={'User-Agent':random.choice(USER_AGENTS)})
                    time.sleep(2)
                    with open(str(each_img_name[i]),'wb') as fp:
                        fp.write(each_img.content)
                        fp.close()
                        print(each_img_name[i]+"下载完成")
if __name__ == "__main__":
    str_urls=get_all_pages()
    for str_url in str_urls:
        get_each_url(str_url)
