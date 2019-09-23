from urllib import request
from bs4 import BeautifulSoup
import re
import  requests
import  json
urlList=[['http://shankapi.ifeng.com/spring/finance/index/newInfoIndex/75219/getNewInfoIndexList', '即时'],
         ['http://shankapi.ifeng.com/spring/finance/index/infoData/20038/getInfoDataList' ,'宏观']
    ,['http://shankapi.ifeng.com/spring/finance/index/infoData/20032/getInfoDataList ','股票']
,['http://shankapi.ifeng.com/spring/finance/index/infoData/1-62-83-/getInfoDataList', '公司']
,['http://shankapi.ifeng.com/spring/finance/index/infoData/75003/getInfoDataList' ,'商业']
,['http://shankapi.ifeng.com/spring/finance/index/infoData/75004/getInfoDataList ','ipo']
,['http://shankapi.ifeng.com/spring/finance/index/infoData/75005/getInfoDataList ','国际']
,['http://shankapi.ifeng.com/spring/finance/index/infoData/20039/getInfoDataList ','women']
,['http://shankapi.ifeng.com/spring/finance/index/infoData/60128/getInfoDataList ','港股']]
class ThemeSpider(object):
    def __init__(self, theme_url,judge_url):
        self.theme_url = theme_url
        self.judge_url = judge_url
        self.urlList=urlList

    def getLinkList(self):
        response = request.urlopen(self.theme_url)
        response=requests.get(self.theme_url)
        linkSet = set()
        linkList = []
        if response.status_code!= 200:
            print("fail to get to first page")
            return linkList
        html_cont = response.text
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')

        h1 = soup.find('h1')
        content=str(html_cont)
        test=re.findall('(var allData = )(\{.+?\};)',content)[0][1]
        tt=re.findall('\{.+?\}',test)
        for item in tt:
            if 'finance.ifeng.com/c/' in item:
                try:
                    contentDict=eval(item.replace('null','None'))
                    linkList.append({'title': contentDict['title'], 'href': contentDict['url']})
                except:
                    print(item)
            else:
                print(item)


        # if hasattr(h1,'a') and h1.a is not None and h1.a['href'] != "#":
        #     linkList.append({'title':h1.a.text.strip(),'href':h1.a['href'].strip()})
        #     linkSet.add(h1.a['href'])
        #
        # #aLinks = soup.find_all('a', href=re.compile(r"http://finance.ifeng.com/a/\d+"))
        # aLinks = soup.find_all('a', href=re.compile(self.judge_url))
        # for link in aLinks:
        #     if link['href'] not in linkSet and link['href'] != "#":
        #         l = len(link.text.strip())
        #         if link.get('title',None) != None and link['title'] != '评论':
        #             if len(link['title'].strip()) > 0:
        #                 linkList.append({'title':link['title'].strip(), 'href':link['href'].strip()})
        #         elif link.get('class',None) != None:
        #             #排除掉网站上评论部分按钮的链接
        #             if link['class'][0] != 'pinl' and l > 0:
        #                 linkList.append({'title':link.text.strip(),'href':link['href'].strip() })
        #                 # linkSet.add(link['href'])
        #         elif l > 0:
        #             linkList.append({'title': link.text.strip(), 'href': link['href'].strip()})
        #             # linkSet.add(link['href'])
        #         linkSet.add(link['href'])

        return linkList

    def getLinkListJson(self):
        linkList=[]
        for url in urlList:
            tt=requests.get(url[0]).text
            content=json.loads(re.findall('{.+}',tt)[0])
            for item in content['data']:
                linkList.append({'title':item['title'],'href':item['url'],'type':url[1]})
        return linkList

