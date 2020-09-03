import selenium_Nav
import Utils
from bs4 import BeautifulSoup
import os


def make_soup(thepage):
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata


def batterScrape(selection):
    if selection == 1:
        selenium_Nav.navFDBatters()
    if selection == 2:
        selenium_Nav.navDKBatters()
    if selection == 3:
        selenium_Nav.navYaHBatters()
    playerdatasaved = ""
    for number in range(1):
        soup = make_soup(selenium_Nav.driver.page_source)
        for entry in soup.findAll('tbody', {'class': 'stat-table__body'}):
            for record in entry.findAll('tr'):
                playerdata = ''
                for data in record.findAll('a', class_= ['full']):
                    name = Utils.parseName(data.text)
                    playerdata = name.strip()
                for data in record.findAll('td', class_= ['fp active','cost','pa','bb','1b','2b','3b','hr','r','rbi','sb']):
                    stat = Utils.parseDigit(data.text)
                    playerdata = playerdata + ',' + stat
                playerdatasaved = playerdatasaved + "\n" + playerdata[0:]
    header = "Name,FP,Price,PA,BB,1B,2B,3B,HR,R,RBI,SB"
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\NFProjections\\batters.csv"), "wb")
    file.write(bytes(header, encoding="ascii,", errors="ignore"))
    file.write(bytes(playerdatasaved, encoding="ascii,", errors="ignore"))
    file.close()


def pitcherScrape(selection):
    if selection == 1:
        selenium_Nav.navFDPitchers()
    if selection == 2:
        selenium_Nav.navDKPitchers()
    if selection == 3:
        selenium_Nav.navYaHPitchers()
    playerdatasaved = ""
    for number in range(1):
        soup = make_soup(selenium_Nav.driver.page_source)
        for entry in soup.findAll('tbody', {'class': 'stat-table__body'}):
            for record in entry.findAll('tr'):
                playerdata = ''
                for data in record.findAll('a', class_=['full']):
                    name = Utils.parseName(data.text)
                    playerdata = name.strip()
                for data in record.findAll('td', class_=['fp active', 'cost', 'wl', 'ip', 'h', 'er', 'k', 'bb']):
                    stat = Utils.parseDigit(data.text)
                    if stat.count(".") == 2:
                        stat = stat[0:4]
                    playerdata = playerdata + ',' + stat

                playerdatasaved = playerdatasaved +"\n" + playerdata[0:]
    header = "Name,FP,Price,W,IP,Ha,ER,K,BBa"
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\NFProjections\\pitchers.csv"), "wb")
    file.write(bytes(header, encoding="ascii,", errors="ignore"))
    file.write(bytes(playerdatasaved, encoding="ascii,", errors="ignore"))
    file.close()
    selenium_Nav.driver.close()

def NBAScrape(selection):
    if selection == 1:
        selenium_Nav.navFDNBA()
    if selection == 2:
        selenium_Nav.navDKNBA()
    if selection == 3:
        selenium_Nav.navYaHNBA()
    playerdatasaved = ""
    for number in range(1):
        soup = make_soup(selenium_Nav.driver.page_source)
        for entry in soup.findAll('tbody', {'class': 'stat-table__body'}):
            for record in entry.findAll('tr'):
                playerdata = ''
                for data in record.findAll('a', class_=['full']):
                    name = Utils.parseName(data.text)
                    playerdata = name.strip()
                for data in record.findAll('td', class_=['fp active', 'cost','min','pts', 'reb', 'ast', 'stl', 'blk', 'to']):
                    stat = Utils.parseDigit(data.text)
                    playerdata = playerdata + ',' + stat
                playerdatasaved = playerdatasaved + "\n" + playerdata[0:]
    header = "Name,FP,Price,Mins,Pts,Rebs,Ast,Stl,Blk,TO"
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\NBA.csv"), "wb")
    file.write(bytes(header, encoding="ascii,", errors="ignore"))
    file.write(bytes(playerdatasaved, encoding="ascii,", errors="ignore"))
    file.close()

def MLBscrape(siteSelection):
    batterScrape(siteSelection)
    pitcherScrape(siteSelection)

def NBAscrape(siteSelection):
    NBAScrape(siteSelection)

def scrapeDriver(sport):
    siteSelection = int(input("Which site would you like to scrape? Press: \n 1-Fanduel \n 2-DraftKings \n 3-Yahoo Daily Fantasy (Scrape Only)"))
    if sport == 1:
        MLBscrape(siteSelection)
    if sport == 2:
        NBAScrape(siteSelection)
    return siteSelection


