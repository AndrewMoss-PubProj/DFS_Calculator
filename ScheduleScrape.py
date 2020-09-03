from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import os



def make_soup(thepage):
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata


def Schedule_Scrape():
    playerdatasaved = ""
    selenium_Path = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\Andrew Moss\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = webdriver.Chrome(executable_path=selenium_Path, options=options)
    driver.get("https://www.espn.com/mlb/schedule")
    soup = make_soup(driver.page_source)
    for entry in soup.find('table', {'class': 'schedule has-team-logos align-left'}):
        for record in entry.findAll('tr'):
            playerdata = ''
            count = 0
            for data in record.findAll('td'):
                if count == 2:
                    break
                playerdata = playerdata +"," + data.text.split()[-1]
                count = count + 1

            playerdatasaved = playerdatasaved + playerdata[0:] + "\n"
    header = ",Team,Opponent"
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Schedule.csv"), "wb")
    file.write(bytes(header, encoding="ascii,", errors="ignore"))
    file.write(bytes(playerdatasaved, encoding="ascii,", errors="ignore"))
    file.close()


def Schedule_Clean():
    Schedule = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Schedule.csv")
    Schedule = Schedule.iloc[:, 1:]
    Rev_Schedule = pd.DataFrame({'Team':Schedule['Opponent'].tolist(), 'Opponent':Schedule['Team'].tolist()})
    Schedule = pd.concat([Schedule, Rev_Schedule], ignore_index=True)
    return Schedule



def Driver():
    Schedule_Scrape()
    Schedule = Schedule_Clean()
    return Schedule


