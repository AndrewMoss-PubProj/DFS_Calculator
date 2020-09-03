from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os
import re

def make_soup(thepage):
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata


def Order_Scrape():
    playerdatasaved = ""
    playerdata = ""
    selenium_Path = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\Andrew Moss\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = webdriver.Chrome(executable_path=selenium_Path, options=options)
    driver.get('https://rotogrinders.com/lineups/mlb?site=draftkings')
    Select(driver.find_element_by_xpath('/html/body/div[1]/div/section/div/section/div[1]/div[3]/div[1]/div[3]/div/select')).select_by_value("4:35pm: Classic: 6 Games")
    soup = make_soup(driver.page_source)
    for time in soup.findAll('li', id=re.compile("^schedule")):
        if time['style'] == "display: none;":
            continue
        for entry in time.findAll('div', {'class': 'blk game'}):
            temp = entry.findAll('div',class_='pitcher players')
            for item in temp:
                playerdata = playerdata + item.find('a',class_='player-popup').text + ",0\n"
            for record in entry.findAll('ul', {'class': 'players'}):
                counter = 0
                for data in record.findAll('li', {'class': 'player'}):
                        if data.find('a') is None:
                            counter = counter + 1
                            continue
                        playerdata = playerdata + data.find('a')['title'] + "," + str(counter % 9+1)+"\n" #+ data.find('span',class_='pown').text
                        counter = counter+1
    playerdatasaved = playerdatasaved + playerdata[0:] + "\n"
    header = "Name,Pos\n"
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\BattingOrders.csv"),"wb")
    file.write(bytes(header, encoding="utf-8", errors="ignore"))
    file.write(bytes(playerdatasaved, encoding="utf-8", errors="ignore"))
    file.close()
    driver.close()

Order_Scrape()