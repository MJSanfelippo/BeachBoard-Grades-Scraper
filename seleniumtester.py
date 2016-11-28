import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def init_driver():
    driver = webdriver.PhantomJS()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, username, password, listOfCourses):
    driver.get("https://bbcsulb.desire2learn.com/")
    try:
        user = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "Username")))
        pw = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "Password")))
        user.send_keys(username) # YOUR USERNAME HERE
        pw.send_keys(password)   # YOUR PASSWORD HERE
        button = driver.find_element_by_xpath('//input[@type="submit" and @value="Login"]')
        button.click()
        coursesGradesURLS = []
        for i in range(len(listOfCourses)):
            course = driver.wait.until(EC.presence_of_element_located((
                By.LINK_TEXT, listOfCourses[i])))
            x = course.get_attribute("href")
            x = x[(len(x)) - 6:]
            coursesGradesURLS.append("https://bbcsulb.desire2learn.com/d2l/lms/grades/my_grades/main.d2l?ou="+x)
        for i in range(len(coursesGradesURLS)):
            driver.get(coursesGradesURLS[i])
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            myPoints = []
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
            grade = (sumMine / sumTotal) * 100
            msg = "Course name: " + courses[i] + "\nGrade: " + str(round(grade, 2)) + "%"
            print(msg)
        driver.quit()
    except TimeoutException:
        print("Box or Button not found in the site")

if __name__ == "__main__":
    driver = init_driver()
    courses = ["REC 141 Sec 04 10919 Intro to Leisure Services",
               "BIOL 200 Sec 01A 1147 General Biology",
               "CECS 229 Sec 03 10376 Discrete Struct Comp Applic II",
               "CECS 341 Sec 05 11273 Computer Architect Organizatin",
               "CECS 343 Sec 01 4057 Intro to Software Engineering"]
    courses.sort()
    # lookup(driver, [USERNAME HERE], [PASSWORD HERE], courses)
    lookup(driver, "", "", courses)