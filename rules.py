import json

"""
This program tests a function that checks whether or not the requirements
for a major are fulfilled. The Computer Science (CS) major is used for
the test: https://catalog.udel.edu/preview_program.php?catoid=47&poid=34727
"""

# make sure to save ACSC.json to the same location as testing.py
with open('courses_list.json') as data_file:
    courses_list = json.load(data_file)


# main function
def check_cs_requirements(courses_taken: dict) -> dict:
    fulfilled = {}
    # university requirements
    fulfilled["ENGL 110"] = check_course(courses_taken, "ENGL 110")
    fulfilled["First year experience"] = check_FYS(courses_taken)
    fulfilled["Discover learning experience"] = check_DLE(courses_taken)
    fulfilled["Multicultural"] = check_multicultural(courses_taken)
    for group in ["A", "B", "C", "D"]:
        fulfilled["Group " + group] = check_group(courses_taken, group)
    fulfilled["Capstone"] = check_capstone(courses_taken)
    # major requirements
    for course_number in ["108", "181", "210", "220", "260", "275", "303", "320", "361", "372"]:
        course = "CISC " + course_number
        fulfilled[course] = check_course(courses_taken, course)
    fulfilled["MATH 205 or MATH 350"] = check_course(courses_taken, "MATH 205") or check_course(courses_taken, "MATH 350")
    for course_number in ["210", "241", "242"]:
        course = "MATH " + course_number
        fulfilled[course] = check_course(courses_taken, course)
    fulfilled["Capstone requirement"] = (check_course(courses_taken, "CISC 498") and check_course(courses_taken, "CISC 499")) or (check_course(courses_taken, "UNIV 401") and check_course(courses_taken, "UNIV 402"))
    return fulfilled
    
# helper functions
def check_course(courses_taken: dict, course: str) -> bool:
    return course in courses_taken

def check_FYS(courses_taken: dict) -> bool:
    fulfilled = False
    for course in courses_taken:
        if course in courses_list:
            if courses_list[course]["fys"]:
                fulfilled = True
    return fulfilled

def check_DLE(courses_taken: dict) -> bool:
    credits = 0
    for course in courses_taken:
        if course in courses_list:
            if courses_list[course]["dle"]:
                credits += courses_taken[course]
    return credits >= 3

def check_multicultural(courses_taken: dict) -> bool:
    credits = 0
    for course in courses_taken:
        if course in courses_list:
            if courses_list[course]["multicultural"]:
                credits += courses_taken[course]
    return credits >= 3

def check_group(courses_taken: dict, group: str) -> bool:
    credits = 0
    for course in courses_taken:
        if course in courses_list:
            if courses_list[course]["group"] == group:
                credits += courses_taken[course]
    return credits >= 3

def check_capstone(courses_taken: dict) -> bool:
    credits = 0
    for course in courses_taken:
        if course in courses_list:
            if courses_list[course]["capstone"]:
                credits += courses_taken[course]
    return credits >= 3

# example of courses taken
courses_taken = {"HIST 304": 4}

# testing
print(check_cs_requirements(courses_taken))