from selenium import webdriver
from bs4 import BeautifulSoup
import time

class Bot():
    def __init__(self):
        self.driver=webdriver.Chrome('C:\\Users\\justRELAX\\Downloads\\chromedriver_win32\\chromedriver.exe')
        self.ToFileTXT(self.get_proxy())

    def get_html(self):
        self.driver.get('https://hidemy.name/ru/proxy-list/?maxtime=2000&type=h&anon=34')
        time.sleep(6)
        requiredHtml = self.driver.page_source
        return requiredHtml
    
    def get_proxy(self):
        html=self.get_html()
        soup=BeautifulSoup(html,'lxml')
        proxys=[]
        proxyTables=soup.find(class_='table_block').find('table').findAll('tr')
        for i in proxyTables:
            ip=i.find('td')
            port=ip.next_sibling
            proxys.append(ip.text+':'+port.text)
        proxys.pop(0)
        return proxys
    
    def ToFileTXT(self,proxys):
        f=open('proxy_file.txt','w')
        for i in proxys:
            if(i!=proxys[-1]):
                f.write(i+'\n')
            else:
                f.write(i)
        f.close()
        self.driver.quit()



def main():
    b=Bot()


if __name__=='__main__':
    main()
