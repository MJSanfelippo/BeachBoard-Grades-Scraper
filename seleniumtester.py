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
            print("ye")
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
            if (sumTotal==0):
                print("No grades posted for " + courses[i])
            else:
                grade = (sumMine / sumTotal) * 100 # determines your grade
                msg = "Course name: " + courses[i] + "\nGrade: " + str(round(grade, 2)) + "%" # prints your grade rounded to 2 decimal places
                print(msg)
        driver.quit()
    except TimeoutException:
        print("Element not found in the site in time")

if __name__ == "__main__":
    driver = init_driver()
    # list of courses
    courses = ["CECS 326 Sec 01 1204 Operating Systems",
               "CECS 323 Sec 09 8254 Database Fundamentals",
               "CECS 328 Sec 01 1206 Data Structures and Algorithms",
               "ENGR 350 Sec 03 8416 Computers- Ethics & Society",
               "REC 340 Sec 02 5610 Leisure Contemporary Society"]
    # lookup(driver, [USERNAME HERE], [PASSWORD HERE], courses)
    lookup(driver, "", "", courses)