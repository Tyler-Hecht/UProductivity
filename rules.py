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
    # dictionary that says whether or not a requirement has been fulfilled
    fulfilled = {}
    # university requirements
    fulfilled["ENGL 110"] = check_courses(courses_taken, ["ENGL 110"])
    fulfilled["First year experience"] = check_FYS(courses_taken)
    fulfilled["Discover learning experience"] = check_DLE(courses_taken)
    fulfilled["Multicultural"] = check_multicultural(courses_taken)
    for group in ["A", "B", "C", "D"]:
        fulfilled["Group " + group] = check_group(courses_taken, group)
    fulfilled["Capstone"] = check_capstone(courses_taken)
    # general CISC courses
    for course_number in ["108", "181", "210", "220", "260", "275", "303", "320", "361", "372"]:
        course = "CISC " + course_number
        fulfilled[course] = check_courses(courses_taken, [course])
    # stat sequence
    fulfilled["MATH 205 or MATH 350"] = check_courses(courses_taken, ["MATH 205"]) or check_courses(courses_taken, ["MATH 350"])
    # general MATH courses
    for course_number in ["210", "241", "242"]:
        course = "MATH " + course_number
        fulfilled[course] = check_courses(courses_taken, [course])
    # CS Capstone requirement
    capstone_sequence_1 = check_courses(courses_taken, ["CISC 498", "CISC 499"])
    capstone_sequence_2 = check_courses(courses_taken, ["UNIV 401", "UNIV 402"])
    fulfilled["Capstone requirement"] = capstone_sequence_1 or capstone_sequence_2
    # science courses
    science_sequence_1 = check_courses(courses_taken, ["PHYS 207", "PHYS 227", "PHYS 208", "PHYS 228"])
    science_sequence_2 = check_courses(courses_taken, ["CHEM 103", "CHEM 133", "CHEM 104", "CHEM 134"])
    science_sequence_3 = check_courses(courses_taken, ["BISC 207", "BISC 208"])
    science_sequence_4 = check_courses(courses_taken, ["GEOL 105", "GEOL 107", "GEOL 115"])
    science_sequence_5 = check_courses(courses_taken, ["GEOL 107", "GEOL 110"])
    fulfilled["Science courses"] = science_sequence_1 or science_sequence_2 or science_sequence_3 or science_sequence_4 or science_sequence_5 
    # return the dictionary
    return fulfilled
    
# helper functions
def check_courses(courses_taken: dict, courses: [str]) -> bool:
    fulfilled = True
    for course in courses:
        fulfilled = fulfilled and course in courses_taken
    return fulfilled

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
courses_taken = {"CISC 108": 4}

# testing
print(check_cs_requirements(courses_taken))