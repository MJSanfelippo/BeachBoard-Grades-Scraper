import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

#initiate the driver with either Chrome or PhantomJS
def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, username, password, listOfCourses):
    driver.get("https://bbcsulb.desire2learn.com/") #Send it to beachboard
    try:
        user = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "Username"))) # finds the username box
        pw = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "Password"))) # finds the password box
        user.send_keys(username) # types the username into the box
        pw.send_keys(password)   # types the password into the box
        pw.send_keys(Keys.RETURN) # presses enter while in the password box - this logs in for you
        coursesGradesURLS = [] # list to hold the grades urls for the courses
        for i in range(len(listOfCourses)):
            course = driver.wait.until(EC.presence_of_element_located((
                By.LINK_TEXT, listOfCourses[i]))) # finds the link of the course
            courseID = course.get_attribute("href") # finds the href attribute (the place that it goes when clicked)
            courseID = courseID[(len(courseID)) - 6:] # this strips the href into just the last 6 elements in it which is the course's ID
            coursesGradesURLS.append("https://bbcsulb.desire2learn.com/d2l/lms/grades/my_grades/main.d2l?ou="+courseID) # this url is the same for all course grade pages except for the id
        for i in range(len(coursesGradesURLS)):
            driver.get(coursesGradesURLS[i]) # sends the driver to the grades page
            html = driver.page_source # get the html of the page
            soup = BeautifulSoup(html, 'html.parser') # initiate soup
            myPoints = []
            totalPoints = []
            for tdTag in soup.find_all('td'): # finds all td tags
                textOfTd = tdTag.text #gets the text of the td tag
                if not textOfTd.endswith('%'):  # continue if the text doesnt end with a %
                    data = textOfTd.split("/") # split it by the division sign, effectively getting yourPoints/totalPoints
                    try:
                        if not float(data[0]) == 0.0: # this assumes that if you got a 0 on an assignment, it's because the prof just hasn't entered the grade - so this
                                                      # script won't work if you legitimately did get a 0 on an assignment
                            myPoints.append(float(data[0])) # gets your points
                            totalPoints.append(float(data[1])) # gets that assignment's total points
                    except Exception: # This essentially is a failsafe
                        print(end='')
            sumMine = sum(myPoints) # gets the sum of all of your points
            sumTotal = sum(totalPoints) # gets the sum of all of the total points available
            grade = (sumMine / sumTotal) * 100 # determines your grade
            msg = "Course name: " + courses[i] + "\nGrade: " + str(round(grade, 2)) + "%" # prints your grade rounded to 2 decimal places
            print(msg)
        driver.quit()
    except TimeoutException:
        print("Element not found in the site in time")

if __name__ == "__main__":
    driver = init_driver()
    # list of courses
    courses = ["REC 141 Sec 04 10919 Intro to Leisure Services",
               "BIOL 200 Sec 01A 1147 General Biology",
               "BIOL 200 Sec 11 1154 General Biology",
               "CECS 229 Sec 03 10376 Discrete Struct Comp Applic II",
               "CECS 341 Sec 05 11273 Computer Architect Organizatin",
               "CECS 343 Sec 01 4057 Intro to Software Engineering"]
    # lookup(driver, [USERNAME HERE], [PASSWORD HERE], courses)
    lookup(driver, "", "", courses)