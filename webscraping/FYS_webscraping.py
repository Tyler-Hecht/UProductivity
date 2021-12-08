import requests
from bs4 import BeautifulSoup
import json

# Getting the html for the First Year Seminar approved courses
url = "https://catalog.udel.edu/preview_program.php?catoid=40&poid=29594"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

find_courses = soup.find_all("li", class_="acalog-course")

# Finding all the courses on the FYS page and adding them to the list
fys_courses = []

for course in find_courses:
    course = course.text.split()
    course = course[0] + " " + course[1]
    fys_courses.append(course)

# Opens the courses.json file and adds a dictionary indicating whether the class is a fys class
with open('courses.json', 'r+') as file:
    data = json.load(file)
for prefix in data:
    courses = data[prefix]
    for course in courses:
        course_code = prefix + " " + course["num"]
        if course_code in fys_courses:
            course["fys"] = True
        else:
            course["fys"] = False

with open("courses.json", 'w') as file_object:
    file_object.write(json.dumps(data, indent=2))
