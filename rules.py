import json
from typing import Union

"""
This program tests a function that checks whether or not the requirements
for a major are fulfilled. The Computer Science (CS) major is used for
the test: https://catalog.udel.edu/preview_program.php?catoid=47&poid=34727
"""

# Load courses_list file for testing on computer
with open('courses_list.json') as data_file:
    courses_list = json.load(data_file)


# main functions
def check_cs_requirements(courses_taken: {str: dict}, functionality: str) -> Union[list, dict]:
    """
    This function checks whether or not the requirements for the Computer Science BS are fulfilled

    Args:
        courses_taken ({str: dict}): A dictionary with each course taken as keys and information about the
            course as values
    Returns:
        If functionality is "fulfilled":
            [[str]]: A list containing two lists: the first lists every fulfilled requirement and the
            second lists every unfulfilled requirement
        If functionality is "courses":
            {str: [str]}: A dictionary with each requirement as keys and a list of the courses that
            help fulfill the requirement as values
    """
    # dictionary that says whether or not a requirement has been fulfilled
    fulfilled_dict = {}
    # university requirements
    fulfilled_dict["ENGL 110"] = check_courses(courses_taken, ["ENGL 110"])[functionality]
    fulfilled_dict["First year experience"] = check_FYS(courses_taken)[functionality]
    fulfilled_dict["Discovery learning experience"] = check_DLE(courses_taken)[functionality]
    fulfilled_dict["Multicultural"] = check_multicultural(courses_taken)[functionality]
    fulfilled_dict["Creative Arts and Humanities Breadth"] = check_group(courses_taken, "A")[functionality]
    fulfilled_dict["History and Cultural Change Breadth"] = check_group(courses_taken, "B")[functionality]
    fulfilled_dict["Social and Behavioral Sciences Breadth"] = check_group(courses_taken, "C")[functionality]
    fulfilled_dict["Mathematics, Natural Sciences, and Technology Breadth"] = check_group(courses_taken, "D")[functionality]
    fulfilled_dict["Capstone"] = check_capstone(courses_taken)[functionality]
    # college requirements
    fulfilled_dict["College of Engineering requirements"] = check_college_reqs(courses_taken)[functionality]
    # general CISC courses
    for course_number in ["108", "181", "210", "220", "260", "275", "303", "320", "361", "372"]:
        course = "CISC " + course_number
        fulfilled_dict[course] = check_courses(courses_taken, [course])[functionality]
    # technical electives
    fulfilled_dict["Technical electives"] = check_technical_electives(courses_taken)[functionality]
    # stat sequence
    fulfilled_dict["MATH 205 or MATH 350"] = check_courses(courses_taken, ["MATH 205"])[functionality] or check_courses(courses_taken,
                                                                                                         ["MATH 350"])[functionality]
    # general MATH courses
    for course_number in ["210", "241", "242"]:
        course = "MATH " + course_number
        fulfilled_dict[course] = check_courses(courses_taken, [course])[functionality]
    # CS Capstone requirement
    capstone_sequence_1 = check_courses(courses_taken, ["CISC 498", "CISC 499"])[functionality]
    capstone_sequence_2 = check_courses(courses_taken, ["UNIV 401", "UNIV 402"])[functionality]
    fulfilled_dict["Capstone requirement"] = capstone_sequence_1 or capstone_sequence_2
    # science courses
    science_sequence_1 = check_courses(courses_taken, ["PHYS 207", "PHYS 227", "PHYS 208", "PHYS 228"])[functionality]
    science_sequence_2 = check_courses(courses_taken, ["CHEM 103", "CHEM 133", "CHEM 104", "CHEM 134"])[functionality]
    science_sequence_3 = check_courses(courses_taken, ["BISC 207", "BISC 208"])[functionality]
    science_sequence_4 = check_courses(courses_taken, ["GEOL 105", "GEOL 107", "GEOL 115"])[functionality]
    science_sequence_5 = check_courses(courses_taken, ["GEOL 107", "GEOL 110"])[functionality]
    fulfilled_dict[
        "Science courses"] = science_sequence_1 or science_sequence_2 or science_sequence_3 or science_sequence_4 or science_sequence_5
    # additional requirements
    fulfilled_dict["CISC 304 or MATH 349 or approved 300+ level math course"] = check_courses(courses_taken, [
        "CISC 304"])[functionality] or check_courses(courses_taken, ["MATH 349"])[functionality]
    fulfilled_dict["ENGL 312 or ENGL 410"] = check_courses(courses_taken, ["CISC 312"])[functionality] or check_courses(courses_taken,
                                                                                                         ["MATH 410"])[functionality]
    fulfilled_dict["CISC 355"] = check_courses(courses_taken, ["CISC 355"])[functionality]
    # electives
    fulfilled_dict["124 credits"] = check_electives(courses_taken)[functionality]
    # return the dictionary as a list of two lists
    fulfilled = []
    unfulfilled = []
    if functionality == "courses":
        return fulfilled_dict
    elif functionality == "fulfilled":
        for requirement in fulfilled_dict:
            if fulfilled_dict[requirement]:
                fulfilled.append(requirement)
            else:
                unfulfilled.append(requirement)
        return [fulfilled, unfulfilled]

# helper functions
def check_courses(courses_taken: {str: dict}, courses: [str]) -> dict:
    """
    This function checks whether or not every course in a list of courses has been taken

    Args:
        courses_taken ({str: dict}): A dictionary containing every offered course as keys and a
            dictionary with information about the course as values
        courses ([str]): The courses to be checked if all have been taken
    Returns:
        dict: A dictionary saying if and how the courses requirement was fulfilled
    """
    fulfilled_by = {"courses": []}
    fulfilled = True
    for course in courses:
        fulfilled = fulfilled and course in courses_taken
        if course in courses_taken:
            fulfilled_by["courses"].append(course)
    fulfilled_by["fulfilled"] = fulfilled
    return fulfilled_by


def check_FYS(courses_taken: {str: dict}) -> dict:
    """
    This function checks whether a course satisfying the First Year Seminar requirement has been taken

    Args:
        courses_taken ({str: dict}): A dictionary containing every offered course as keys and a
            dictionary with information about the course as values
    Returns:
        dict: A dictionary saying if and how the FYS requirement was fulfilled
    """
    fulfilled_by = {"courses": []}
    fulfilled = False
    for course in courses_taken:
        if courses_list[course]["fys"]:
            fulfilled = True
            fulfilled_by["courses"].append(course)
    fulfilled_by["fulfilled"] = fulfilled
    return fulfilled_by

def check_DLE(courses_taken: {str: dict}) -> dict:
    """
    This function checks whether the Discovery Learning Experience requirement has been fulfilled

    Args:
        courses_taken ({str: dict}): A dictionary containing every offered course as keys and a
            dictionary with information about the course as values
    Returns:
        dict: A dictionary saying if and how the DLE requirement was fulfilled
    """
    fulfilled_by = {"courses": []}
    credits = 0
    for course in courses_taken:
        if courses_list[course]["dle"]:
            credits += courses_taken[course]
            fulfilled_by["courses"].append(course)
    fulfilled_by["fulfilled"] = credits >= 3
    return fulfilled_by

def check_multicultural(courses_taken: {str: dict}) -> dict:
    """
    This function checks whether the multicultural requirement has been fulfilled

    Args:
        courses_taken ({str: dict}): A dictionary containing every offered course as keys and a
            dictionary with information about the course as values
    Returns:
        dict: A dictionary saying if and how the multicultural requirement was fulfilled
    """
    fulfilled_by = {"courses": []}
    credits = 0
    for course in courses_taken:
        if courses_list[course]["multicultural"]:
            fulfilled_by["courses"].append(course)
            credits += courses_taken[course]
    fulfilled_by["fulfilled"] = credits >= 3
    return fulfilled_by

def check_group(courses_taken: {str: dict}, group: str) -> dict:
    """
    This function checks whether a group breadth requirement has been fulfilled

    Args:
        courses_taken ({str: dict}): A dictionary containing every offered course as keys and a
            dictionary with information about the course as values
        group (str): The group (A, B, C, or D) to be checked
    Returns:
        dict: A dictionary saying if and how the breadth requirement was fulfilled
    """
    fulfilled_by = {"courses": []}
    credits = 0
    for course in courses_taken:
        if courses_list[course]["group"] == group and not courses_list[course]["coe"]:
            credits += courses_taken[course]
            fulfilled_by["courses"].append(course)
    fulfilled_by["fulfilled"] = credits >= 3
    return fulfilled_by

def check_capstone(courses_taken: {str: dict}) -> dict:
    """
    This function checks whether the capstone requirement has been fulfilled

    Args:
        courses_taken ({str: dict}): A dictionary containing every offered course as keys and a
            dictionary with information about the course as values
    Returns:
        dict: A dictionary saying if and how the capstone requirement was fulfilled
    """
    fulfilled_by = {"courses": []}
    credits = 0
    for course in courses_taken:
        if courses_list[course]["capstone"]:
            credits += courses_taken[course]
            fulfilled_by["courses"].append(course)
    fulfilled_by["fulfilled"] = credits >= 3
    return fulfilled_by

def check_technical_electives(courses_taken: {str: dict}) -> dict:
    """
    This function checks whether the technical electives requirement has been fulfilled

    Args:
        courses_taken ({str: dict}): A dictionary containing every offered course as keys and a
            dictionary with information about the course as values
    Returns:
        dict: A dictionary saying if and how the technical electives requirement was fulfilled
    """
    fulfilled_by = {"courses": []}
    vip_credits = 0
    credits = 0
    for course in courses_taken:
        if (not course[-2:] == 87) or vip_credits < 3:
            if (course[:4] == "CISC" and float(course[-3:]) >= 300) and (
            not float(course[-3:]) in [303, 320, 361, 372, 355, 356, 357, 465, 366, 466]):
                credits += courses_taken[course]
                fulfilled_by["courses"].append
                if course[-2:] == 87:
                    vip_credits += courses_taken[course]
    fulfilled_by["fulfilled"] = credits >= 6
    return fulfilled_by
            

def check_electives(courses_taken: {str: dict}) -> bool:
    """
    This function checks whether the electives requirement has been fulfilled

    Args:
        courses_taken ({str: dict}): A dictionary containing every offered course as keys and a
            dictionary with information about the course as values
    Returns:
        bool: Whether or not the electives requirement is fulfilled
    """
    fulfilled_by = {"courses": []}
    credits = 0
    for course in courses_taken:
        credits += courses_taken[course]
        if courses_taken[course] > 0:
            fulfilled_by["courses"].append(course)
    fulfilled_by["fulfilled"] = credits >= 124
    return fulfilled_by

def check_college_reqs(courses_taken: {str: dict}) -> dict:
    """
    This function checks whether the College of Engineering requirement has been fulfilled

    Args:
        courses_taken ({str: dict}): A dictionary containing every offered course as keys and a
            dictionary with information about the course as values
    Returns:
        dict: A dictionary saying if and how the college electives requirement was fulfilled
    """
    fulfilled_by = {"courses": []}
    credits = 0
    pcp_credits = 0
    upper_level_credits = 0
    for course in courses_taken:
        # PCP credits can't exceed 6
        if (not courses_list[course]["pcp"]) or pcp_credits <= 6:
            # must be from university breadth courses or COE breadth courses
            if courses_list[course]["group"] in ["A", "B", "C"] or (courses_list[course]["coe"] and courses_list[course]["group"] != "D"):
                credits += courses_taken[course]
                fulfilled_by["courses"].append(course)
                # keep track of how many PCP credits have been taken
                if courses_list[course]["pcp"]:
                    pcp_credits += courses_taken[course]
                # upper-level courses
                    if (courses_list[course]["group"] in ["A", "B", "C"] and float(course[-3:]) >= 300) or (
                    courses_list[course]["coe"] and courses_list[course]["group"] != "D" and float(course[-3:]) >= 300):
                        upper_level_credits += courses_taken[course]
    fulfilled_by["fulfilled"] = credits >= 9 and upper_level_credits >= 6
    return fulfilled_by

# example of courses taken
courses_taken = {"MATH 241": 4}

# testing
print(check_cs_requirements(courses_taken, "fulfilled"))
print(check_cs_requirements(courses_taken, "courses"))