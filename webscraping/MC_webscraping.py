import requests
from bs4 import BeautifulSoup
import json

# Getting the html for the Multicultural approved courses
url = "https://catalog.udel.edu/preview_program.php?catoid=40&poid=29592"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

find_courses = soup.find_all("li", class_="acalog-course")

# Finding all the courses on the Multicultural page and adding them to the list
mc_courses = []

for course in find_courses:
    course = course.text.split()
    course = course[0] + " " + course[1]
    mc_courses.append(course)

# Opens the courses.json file and adds a dictionary indicating whether the class is a multicultural class
with open('courses.json', 'r+') as file:
    data = json.load(file)
for prefix in data:
    courses = data[prefix]
    for course in courses:
        course_code = prefix + " " + course["num"]
        if course_code in mc_courses:
            course["multicultural"] = True
        else:
            course["multicultural"] = False

with open("courses.json", 'w') as file_object:
    file_object.write(json.dumps(data, indent=2))
