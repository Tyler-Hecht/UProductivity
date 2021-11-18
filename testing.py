'''
This program tests a function that checks whether or not the requirements
for a major are fulfilled. The Actuarial Sciences (ACSC) major is used for
the test. Currently, the ACSC major is simplified to just the computational
cluster: https://catalog.udel.edu/preview_program.php?catoid=47&poid=34542
'''

#a dictionary giving the requirements for the ACSC computational cluster
#the key is the requirement to be fulfilled and the value is another dictionary
#the other dictionary gives what courses can fulfill the requirement and how many are needed to fulfill it
comp_cluster = {"CISC106": {"can_fulfill": ["CISC106"], "amount": 1},
                "CISC181": {"can_fulfill": ["CISC181"], "amount": 1},
                "MISY330": {"can_fulfill": ["MISY330"], "amount": 1}
                }

#a list of the courses that have been fulfilled
courses = ["CISC106"]

#main function
def check_requirements(courses: [str], reqs: {str: dict}) -> str:
    '''
    This function checks whether or not the requirements for a major are fulfilled
    
    Args:
        courses ([str]): A list of strings representing the courses on the planned schedule
        reqs {str: dict}: A dictionary containing requirements and the courses that can fulfill
            the requirement as well as how many of the courses must be taken
    Returns:
        str: An message indicating whether or the requirements are fulfilled by the planned courses
            and what requirements must still be fulfilled, if any
    '''
    #the missing courses will be listed here
    missing = []
    #a boolean which represents whether or not the requirements are fulfilled
    #starts off true as default but may become false
    fulfilled = True
    #iterates over the dictionary of requirements using both the key and value
    for key, value in reqs.items():
        #determines whether or not a requirement is fulfilled
        if set(value["can_fulfill"]).isdisjoint(courses):
            #if it isn't fulfilled, make fulfilled false (permanently) and add the requirement to the list
            fulfilled = False
            missing.append(key)
    #if all requirements are fulfilled
    if fulfilled:
        return "You aren't missing any courses"
    #if there are still requirements to fulfill
    else:
        #a string that will say which requirements are missing
        to_return = "You are missing the following requirements:"
        for req in missing:
            #adds the missing course to the string
            to_return += " " + req + ","
        #removes the extra comma and returns the string
        return to_return[:-1]
    
#test the code
print(check_requirements(courses, comp_cluster))