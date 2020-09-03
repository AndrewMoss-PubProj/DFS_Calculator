from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

def make_soup(thepage):
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata


def Fangraphs_BatterScrape():
    playerdatasaved = ""
    playerdata = ""
    selenium_Path = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\Andrew Moss\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = webdriver.Chrome(executable_path=selenium_Path, options=options)
    driver.get('https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=bat&type=sabersim&team=0&lg=all&players=0')
    driver.find_element_by_xpath('//*[@id="DFSBoard1_dg1_ctl00_ctl02_ctl00_PageSizeComboBox_Input"]').click()
    time.sleep(.5)
    driver.find_element_by_xpath('//*[@id="DFSBoard1_dg1_ctl00_ctl02_ctl00_PageSizeComboBox_DropDown"]/div/ul/li[7]').click()
    soup = make_soup(driver.page_source)
    for record in soup.findAll('table', {'class': 'rgMasterTable'}):
        for entry in record.findAll('tr'):
            playerdata = ""
            for data in entry.findAll('td'):
                playerdata = playerdata + ", " + data.text
            playerdatasaved = playerdatasaved + playerdata[2:] + "\n"
    header = "Name,Team,Game,Pos,PA,H,1B,2B,3B,HR,R,RBI,SB,CS,BB,SO,Yahoo,Fanduel,DraftKings"
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\FangraphsProjections\\FangraphsBatters.csv"),"wb")
    file.write(bytes(header, encoding="utf-8", errors="ignore"))
    file.write(bytes(playerdatasaved, encoding="utf-8", errors="ignore"))
    file.close()
    driver.close()

def Fangraphs_PitcherScrape():
    playerdatasaved = ""
    playerdata = ""
    selenium_Path = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\Andrew Moss\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = webdriver.Chrome(executable_path=selenium_Path, options=options)
    driver.get('https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=pit&type=sabersim&team=0&lg=all&players=0')
    driver.find_element_by_xpath('//*[@id="DFSBoard1_dg1_ctl00_ctl02_ctl00_PageSizeComboBox_Input"]').click()
    time.sleep(.5)
    driver.find_element_by_xpath('//*[@id="DFSBoard1_dg1_ctl00_ctl02_ctl00_PageSizeComboBox_DropDown"]/div/ul/li[7]').click()
    soup = make_soup(driver.page_source)
    for record in soup.findAll('table', {'class': 'rgMasterTable'}):
        for entry in record.findAll('tr'):
            playerdata = ""
            for data in entry.findAll('td'):
                playerdata = playerdata + ", " + data.text
            playerdatasaved = playerdatasaved + playerdata[2:] + "\n"
    header = "Name,Team,Game,W,IP,TBF,Ha,1B,2B,3B,HR,BBa,K,Yahoo,Fanduel,DraftKings"
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\FangraphsProjections\\FangraphsPitchers.csv"),"wb")
    file.write(bytes(header, encoding="utf-8", errors="ignore"))
    file.write(bytes(playerdatasaved, encoding="utf-8", errors="ignore"))
    file.close()
    driver.close()


Fangraphs_BatterScrape()
Fangraphs_PitcherScrape()