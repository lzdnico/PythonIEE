import re
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
import os
import traceback
import win32com
documentlist = []
path = 'E:/IEEE' + '.txt'
def getDocument(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        js = "var q=document.body.scrollTop=10000"
        driver.execute_script(js)
        driver.execute_script(js)
        driver.execute_script(js)
        driver.execute_script(js)
        driver.execute_script(js)
        driver.execute_script(js)
        time.sleep(5)
        elem = driver.find_elements_by_xpath("//a[@ng-if='::(!(record.ephemera))']")
        for i in elem:
            documentlist.append(i.get_attribute("href"))
            print(documentlist[-1])
        time.sleep(3)
        driver.close()
    except:
        print("Open Web Error")


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getUrlText():
    for j in range(len(documentlist)):
        url = documentlist[j]
        list = []
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find_all('script',type="text/javascript")
        title = soup.find('title')
        with open(path, 'a', encoding='utf-8') as f:
             f.write("href:="+documentlist[j]+'\n'+"tittle: "+'\n'+title.text + '\n')
        for i in a:
            try:
                plt = re.findall(r'\"abstract\".*","', i.string)
                str = ''.join(plt)
                abstract = str.split('":"')[1]
                abstract = abstract[0:-18]
                print("\r当前进度: {:.2f}%".format((j+1) * 100 / len(documentlist)), end="")
                if plt != []:
                    list.append(abstract)
                with open(path, 'a', encoding='utf-8') as f:
                    f.write("abstract:"+ '\n')
                    for i in range(len(list)):
                        begin = 0
                        end = 100
                        len1 = len(list[i])+100
                        while end <len1:
                            f.write(list[i][begin:end] + '\n')
                            begin=end
                            end = end +100
                    f.write('\n'+'\n')
            except:
                continue


def main():
    search = input("plz enter what u want search:\n")
    url = "http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=" + search + "&sortType=desc_p_Publication_Year&rowsPerPage=50"
    print(url)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(search + '\n'+ '\n')
    getDocument(url)
    getUrlText()

main()