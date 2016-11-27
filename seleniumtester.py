import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, query, courseName):
    driver.get("https://csulb.okta.com/")
    try:
        user = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "input27")))
        pw = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "input34")))
        user.send_keys("") # YOUR USERNAME HERE
        pw.send_keys("")   # YOUR PASSWORD HERE
        button = driver.find_element_by_xpath('//input[@type="submit" and @value="Sign In"]')
        button.click()
        time.sleep(5)
        window_before = driver.window_handles[0]
        bb = driver.find_element_by_xpath('//img[@src="https://csulb.okta.com/bc/image/fileStoreRecord?id=fs0r9zeso8JAELNNYTUJ"]')
        bb.click()
        time.sleep(10)
        window_after = driver.window_handles[1]
        driver.switch_to_window(window_after)
        course = driver.wait.until(EC.presence_of_element_located((
            By.LINK_TEXT, courseName)))
        course.click()
        grades = driver.wait.until(EC.presence_of_element_located((
            By.LINK_TEXT, "Grades")))
        grades.click()
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        myPoints= []
        totalPoints = []
        for tag in soup.find_all('td'):
            x = tag.text
            if not x.endswith('%'):
                data = x.split("/")
                try:
                    if not float(data[0]) == 0.0:
                        myPoints.append(float(data[0]))
                        totalPoints.append(float(data[1]))
                except Exception:
                    print(end='')
        sumMine = sum(myPoints)
        sumTotal = sum(totalPoints)
        grade = (sumMine/sumTotal)*100
        msg = "Course name: " + courseName + "\nGrade: " + str(round(grade,2))+"%"
        print(msg)
    except TimeoutException:
        print("Box or Button not found in the site")

if __name__ == "__main__":
    message = []
    driver = init_driver()
    x = (lookup(driver, "Selenium","REC 141 Sec 04 10919 Intro to Leisure Services"))
    message.append(x)
    driver = init_driver()
    message.append(lookup(driver, "Selenium", "BIOL 200 Sec 01A 1147 General Biology"))
    driver = init_driver()
    message.append(lookup(driver, "Selenium", "CECS 229 Sec 03 10376 Discrete Struct Comp Applic II"))
    driver = init_driver()
    message.append(lookup(driver, "Selenium", "CECS 341 Sec 05 11273 Computer Architect Organizatin"))
    driver = init_driver()
    message.append(lookup(driver, "Selenium", "CECS 343 Sec 01 4057 Intro to Software Engineering"))
