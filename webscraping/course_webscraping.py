import requests
from bs4 import BeautifulSoup
import json

"""
This program attempts to gather data about every course that the University of Delaware offers using BeautifulSoup
to webscrape the courses page on the UD catalog. URL = "https://catalog.udel.edu/content.php?catoid=47&navoid=8868".
Data collected will be loaded onto the courses.json file.
"""
json_file = 'courses.json'

courses = {"": {
    "credits": [
      0
    ],
    "title": "",
    "group": None,
    "dle": False,
    "fys": False,
    "multicultural": False,
    "capstone": False,
    "coe": False,
    "pcp": False
  },}

# Since there are 46 pages of courses, the program has to iterate through each page by manipulating the format of the
# URL.
first_half_of_url = "https://catalog.udel.edu/content.php?catoid=47&catoid=47&navoid=8868&filter%5Bitem_type%" \
                    "5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D="
second_half_of_url = "#acalog_template_course_filter"


for i in range(1, 47):
    url = first_half_of_url + str(i) + second_half_of_url
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    # Iterates through each course on the courses page to find the course prefix (code), course number, course title
    # and number of credits
    find_courses = soup.find_all("td", class_="width")

    for find_course in find_courses:
        a = find_course.find("a")
        course_elements = a.text.split()
        course_prefix = course_elements[0]
        course_num = course_elements[1]
        course_code = course_prefix + " " + course_num
        title = course_elements[3:]
        course_title = ""
        for word in title:
            course_title = course_title + " " + word
        course_title = course_title[1:]

        # Fixes the error with apostrophe
        if "’" in course_title:
            apostrophe_position = None
            position = 0
            for char in course_title:
                if char == "’":
                    apostrophe_position = position
                position += 1
            course_title = course_title[0:apostrophe_position] + "'" + course_title[apostrophe_position + 1:]

        # Finds the link to the course page to find the number of credits
        link = find_course.find('a', href=True).get('href')
        new_url = "https://catalog.udel.edu/" + link
        new_page = requests.get(new_url)
        new_soup = BeautifulSoup(new_page.content, "html.parser")

        # Finds the number of credits on the course page
        find_credits = new_soup.find_all("p")
        refined = find_credits[1].text.split()

        found = False
        credits_position = None
        for position, word in enumerate(refined):
            if not found:
                if word == 'Credit(s):':
                    credits_position = position
                    found = True
        num_credits = []
        try:
            if refined[credits_position + 1][1] == "-":
                min = int(refined[credits_position + 1][0])
                max = int(refined[credits_position + 1][2])
                num_credits = list(range(min, max + 1))
            else:
                num_credits.append(int(refined[credits_position + 1][0]))
        except:
            num_credits.append(int(refined[credits_position + 1][0]))

        # Adds the course information to the courses dictionary
        courses[course_code] = {"credits": num_credits, "title": course_title}

# Storing the courses dictionary on the json file
with open(json_file, 'w') as file_object:
    file_object.write(json.dumps(courses, indent=2))
