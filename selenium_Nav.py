from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


selenium_Path = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\Andrew Moss\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
driver = webdriver.Chrome(executable_path=selenium_Path, options=options)


def navFDBatters():
    driver.get("https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections/batters/#")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/span")))
    element.click()
    driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[1]").click()
def navFDPitchers():
    driver.get("https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections/pitchers/")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/span")))
    element.click()
    driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[1]").click()
def navDKBatters():
    driver.get("https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections/batters/#")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/span")))
    element.click()
    driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[2]").click()
def navDKPitchers():
    driver.get("https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections/pitchers/")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/span")))
    element.click()
    driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[2]").click()
def navYaHBatters():
    driver.get("https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections/batters/#")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/span")))
    element.click()
    driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[3]").click()
def navYaHPitchers():
    driver.get("https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections/pitchers/")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/span")))
    element.click()
    driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[3]").click()
def navFDNBA():
    driver.get("https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/span")))
    element.click()
    driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[1]").click()
def navDKNBA():
    driver.get("https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/span")))
    element.click()
    driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[2]").click()
def navYaHNBA():
    driver.get("https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/span")))
    element.click()
    driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[3]").click()

