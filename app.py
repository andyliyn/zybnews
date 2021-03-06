#coding=utf-8
import sys
import urllib2
import re
import os
from bs4 import BeautifulSoup

#init header  
header = {  
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',  
    'Accept-Encoding':'gzip, deflate',  
    'Accept-Language':'zh-CN,zh;q=0.9',  
    'Connection':'keep-alive',  
    'Host':'weixin.sogou.com',  
    'Upgrade-Insecure-Requests':'1',  
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',  
    } 

#get cookie  
def get_cookies():  
    driver = webdriver.Chrome()  
    driver.get("http://weixin.sogou.com/")  
  
    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()  
    time.sleep(10)  
  
    cookies = driver.get_cookies()  
    cookie = {}  
    for items in cookies:  
        cookie[items.get('name')] = items.get('value')  
    return cookie
 
def extract_url(info):     
     soup=BeautifulSoup(info,"html.parser")
     #print 'soup',soup
     re_url = soup.findAll('h3')
     return re_url
 
def extract_sub_web_title(sub_web):
     re_key = "<title>.+</title>"
     title = re.findall(re_key,sub_web)
     return title
 
def extract_sub_web_content(sub_web):
     re_key = "<div id=\"Cnt-Main-Article-QQ\".*</div>"
     content = re.findall(re_key,sub_web)
     return content
 
def filter_tags(htmlstr):
     re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) 
     re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
     re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
     re_p=re.compile('<P\s*?/?>')
     re_h=re.compile('</?\w+[^>]*>')
     re_comment=re.compile('<!--[^>]*-->')
     s=re_cdata.sub('',htmlstr)
     s=re_script.sub('',s)
     s=re_style.sub('',s)
     s=re_p.sub('\r\n',s)
     s=re_h.sub('',s) 
     s=re_comment.sub('',s)
     blank_line=re.compile('\n+')
     s=blank_line.sub('\n',s)
     return s

def explore_access(web_url):
    #web_url=urlStr.replace('pgNum',str(k))
    request = urllib2.Request(web_url) 
    request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')  
    opener = urllib2.build_opener()  
    html= opener.open(request).read()
    return html

#网页搜索
def extract_web_content(keyword):
    f = file('result.txt','w')
    urlStr='http://weixin.sogou.com/weixin?query=keyword&_sug_type_=&s_from=input&_sug_=n&type=2&page=pgNum&ie=utf8'
    #keyword='互联网营销'
    urlStr=urlStr.replace('keyword',keyword)
    for k in range(1,3):
        web_url=urlStr.replace('pgNum',str(k))    
        #get news
        #content = urllib2.urlopen(url).read()
        content = explore_access(web_url)
        #print content
        #get the url
        get_url = extract_url(content)
        num=len(get_url)
        for i in range(num):
            item=get_url[i].find('a')
            title=item.renderContents()
            title=title.decode('utf-8', 'ignore')
            link=item.get("href")
            print 'title====',title,'--- link is   ',link
            if title  and link:
                re_content = filter_tags(title+"\r"+link)
                f.write(re_content.encode("utf-8"))
                f.write("\r\n")

    #print 'get_url-----',get_url
    f.close()

#通过微信搜狗从指定公众号查询关键字内容
def extract_web_content_weixin_account(wxid,keyword,fileName):
    f = file(fileName,'w')
    urlStr='http://weixin.sogou.com/weixin?type=2&ie=utf8&query=keyword&tsn=1&ft=&et=&interation=&wxid=targetWXID&usip=101.80.92.79'
    urlStr=urlStr.replace('keyword',keyword)
    urlStr=urlStr.replace('targetWXID',wxid)
    print urlStr
    for k in range(1,2):    
        print k
        web_url=urlStr.replace('pgNum',str(k))
        print 'web_url======================'
        print  web_url
        #get news
        #content = urllib2.urlopen(url).read()
        content = explore_access(web_url)
        #print content
        #get the url
        get_url = extract_url(content)
        num=len(get_url)
        for i in range(num):
            item=get_url[i].find('a')
            title=item.renderContents()
            title=title.decode('utf-8', 'ignore')
            link=item.get("href")
            print 'title====',title,'--- link is   ',link
            if title  and link:
                re_content = filter_tags(title+"\r"+link)
                f.write(re_content.encode("utf-8"))
                f.write("\r\n")
    f.close()
    
extract_web_content_weixin_account('oIWsFt8_jYUmdw1PQgNVhH9vOEvI','health','health.txt')
    
