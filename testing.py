import json

"""
This program tests a function that checks whether or not the requirements
for a major are fulfilled. The Actuarial Sciences (ACSC) major is used for
the test. Currently, the ACSC major is simplified to just the computational
cluster: https://catalog.udel.edu/preview_program.php?catoid=47&poid=34542
"""

"""
Imports a dictionary giving the requirements for the ACSC major: "acceptable courses"
shows what courses will count towards the requirement as well as how many credits each
is worth; "credits" shows how many credits are needed from the acceptable courses;
"special case?" shows if the credit requirement falls under a special case (such as
requirement sequences)

Notes:
-The dictionary being used doesn't have all the courses that will fulfill university/college
requirements but rather gives a few generic names such as A1, A2, etc for the purposes of
testing.
-Due to ambiguity on the catalog, the dictionary is formatted such that the first year experience
requires 0 credits to be met (and so is always fulfilled) and the secondary writing requirement,
for which any allowed course may be taken to fulfill (regardless of credits), requires 1 credit
to fulfill.
"""
# make sure to save ACSC.json to the same location as testing.py
with open('ACSC.json') as data_file:
    acsc_reqs = json.load(data_file)


# main function
def check_requirements(courses: list, reqs: dict) -> str:
    """
    This function checks whether or not the requirements for a major are fulfilled

    Args:
        courses ([str]): A list of strings representing the courses on the planned schedule
        reqs {str: dict}: A dictionary containing requirements and the courses that can fulfill
            the requirement (as well as their details)
    Returns:
        str: An message indicating whether or the requirements are fulfilled by the planned courses
            and what requirements must still be fulfilled, if any
    """
    # the missing courses will be listed here
    missing = []
    # a boolean which represents whether or not the requirements are fulfilled
    fulfilled = True

    # iterates over the dictionary of requirements using both the key and value
    for key, value in reqs.items():
        # determines whether or not a requirement is fulfilled
        if not req_fulfilled(value, courses):
            # if set(acceptable_courses).isdisjoint(courses):
            # if it isn't fulfilled, make fulfilled false (permanently) and add the requirement to the list
            fulfilled = False
            missing.append(key)

    # if all requirements are fulfilled
    if fulfilled:
        return "You aren't missing any courses"
    # if there are still requirements to fulfill
    else:
        # a string that will say which requirements are missing
        to_return = "You are missing the following requirements:"
        for req in missing:
            # adds the missing course to the string
            to_return += " " + req + ";"
        # removes the extra semicolon and returns the string
        return to_return[:-1]


def req_fulfilled(how_to_fulfill: dict, courses_taken: list) -> bool:
    """
    This function takes a list of courses that can fulfill the requirement and courses that have been taken
    and determines whether or not the requirement is fulfulled

    Args:
        how_to_fulfill (dict): What is needed to fulfull this degree requirement
        courses_taken (list): The courses that have been taken so far
    Returns:
        bool: Whether or not the requirement has been fulfilled
    """
    # if it's not a special case
    if not how_to_fulfill["special case?"]:
        credits = 0
        # adds up the credits from courses taken
        for key, value in how_to_fulfill["acceptable courses"].items():
            if key in courses_taken:
                credits += value
        # returns whether or not enough credits have been taken
        return credits >= how_to_fulfill["credits"]
    # if it's a sequence
    elif how_to_fulfill["special case?"] == "sequence":
        # considers each sequence
        for sequence in how_to_fulfill["acceptable courses"]:
            completed = True
            # checks if every course in the sequence is fulfilled
            for course in sequence:
                if course not in courses_taken:
                    completed = False
            # if the sequence is completed
            if completed:
                return True
        # if no sequence is completed
        return False


# test the code
print(check_requirements(["CISC106", "ACCT207", "MATH350", "MATH450", "A1", "A4", "B2", "B3"], acsc_reqs))
