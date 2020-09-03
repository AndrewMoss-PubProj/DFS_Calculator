from selenium import webdriver
import shutil
import os

def MLBDownload ():
    selenium_Path = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\Andrew Moss\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = webdriver.Chrome(executable_path=selenium_Path, options=options)
    driver.get("https://www.draftkings.com/lineup/upload")
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div[1]/a").click()
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div[1]/ul/li[2]/a").click()
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/ul/li[2]/a").click()
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/a").click()
    os.chdir('C:\\Users\\Andrew Moss\\Downloads')
    os.rename('C:\\Users\\Andrew Moss\\Downloads\\DKSalaries.csv',
              'C:\\Users\\Andrew Moss\\Downloads\\DKSalariesMLB.csv')
    shutil.move('C:\\Users\\Andrew Moss\\Downloads\\DKSalariesMLB.csv',
                'C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\DKSalariesMLB.csv')
    driver.close()

def NBADownload ():
    selenium_Path = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\Andrew Moss\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = webdriver.Chrome(executable_path=selenium_Path, options=options)
    driver.get("https://www.draftkings.com/lineup/upload")
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div[1]/a").click()
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div[1]/ul/li[4]/a").click()
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/ul/li[1]/a").click()
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/a").click()
    os.chdir('C:\\Users\\Andrew Moss\\Downloads')
    os.rename('C:\\Users\\Andrew Moss\\Downloads\\DKSalaries.csv',
              'C:\\Users\\Andrew Moss\\Downloads\\DKSalariesNBA.csv')
    shutil.move('C:\\Users\\Andrew Moss\\Downloads\\DKSalariesNBA.csv',
                'C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\DKSalariesNBA.csv')
    driver.close()


MLBDownload()