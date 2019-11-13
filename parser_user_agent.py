import requests
from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    return response.text

def get_user_agents(html):
    soup=BeautifulSoup(html,'lxml')
    user_agents=[]
    user_agents_Tables=soup.findAll(class_='row_name')
    for i in user_agents_Tables:
        if(i.find('a').text!='Symfony2 BrowserKit'):
            user_agents.append(i.find('a').text)
    return user_agents

def ToFileTXT(user_agents):
    f=open('user_agent.txt','w')
    for i in user_agents:
            if(i!=user_agents[-1]):
                f.write(i+'\n')
            else:
                f.write(i)
    f.close()

def main():
    user_agents=[]
    user_agents=get_user_agents(get_html('https://myip.ms/browse/comp_browseragents/1/sort/4#comp_browseragents_tbl_top'))
    ToFileTXT(user_agents)
    for i in user_agents:
        print(i)
if __name__=='__main__':
    main()
