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
def check_cs_requirements() -> str:
    pass
    
# helper functions
def check_ENGL110(courses_taken: dict) -> bool:
    return "ENGL 110" in courses_taken

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

# example of courses taken
courses_taken = {"HIST 304": 4}

# testing
print(check_group(courses_taken, "B"))