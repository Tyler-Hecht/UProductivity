import requests
from bs4 import BeautifulSoup
import json

# Getting the html for the College Engineering Breadth courses and Professional and Career Preparation Courses
url = "https://catalog.udel.edu/preview_program.php?catoid=47&poid=34806#professional-listing"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

find_courses = soup.find("div", class_="custom_leftpad_20")
find_courses = find_courses.find_all("div", class_="custom_leftpad_20")

# Finding all COE breath courses and adding them to the list
coe_courses = []
coe = find_courses[0].find_all("li", class_="acalog-course")

for course in coe:
    course = course.text.split()
    course = course[0] + " " + course[1]
    coe_courses.append(course)

# Finding all PCP breadth courses and adding them to the list
pcp_courses = []
pcp = find_courses[1].find_all("li", class_="acalog-course")

for course in pcp:
    course = course.text.split()
    course = course[0] + " " + course[1]
    pcp_courses.append(course)

# Opens the courses.json file and adds a dictionary indicating whether the class is a coe or pcp class
with open('courses.json', 'r+') as file:
    data = json.load(file)

for course in data:
    if course in coe_courses:
        data[course]["coe"] = True
    else:
        data[course]["coe"] = False
    if course in pcp_courses:
        data[course]["pcp"] =  True
    else:
        data[course]["pcp"] = False

with open("courses.json", 'w') as file_object:
    file_object.write(json.dumps(data, indent=2))



