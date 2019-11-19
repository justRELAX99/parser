from selenium import webdriver
import time
from bs4 import BeautifulSoup

def get_html(driver):
        driver.get('https://hidemy.name/ru/proxy-list/?maxtime=2000&type=h&anon=34')
        time.sleep(6)
        requiredHtml =driver.page_source
        return requiredHtml
    
def get_proxy(html):
        soup=BeautifulSoup(html,'lxml')
        proxys=[]
        proxyTables=soup.find(class_='table_block').find('table').findAll('tr')
        for i in proxyTables:
            ip=i.find('td')
            port=ip.next_sibling
            proxys.append(ip.text+':'+port.text)
        proxys.pop(0)
        return proxys
    
def ToFileTXT(proxys):
        f=open('proxy_file.txt','w')
        for i in proxys:
            if(i!=proxys[-1]):
                f.write(i+'\n')
            else:
                f.write(i)
        f.close()

def main():
        driver=webdriver.Chrome('C:\\Users\\justRELAX\\Downloads\\chromedriver_win32\\chromedriver.exe')
        html=get_html(driver)
        proxys=get_proxy(html)
        ToFileTXT(proxys)
        driver.quit()

if __name__=='__main__':
    main()
