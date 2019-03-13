import re


def is_int(num):
    # We can use exceptions but they are expensive so we would prefere to use as a workflow. instead we can use regular expressions
    if re.match(r'^[-+]?(\d)+$', num):
        return True
    return False


#TODO: This may be further improved
def print_variables(varDict):
    print("(", end="")
    for idx, key in enumerate(varDict):
        if idx > 0:
            print(",", end="")
        print(str(key) + "=" + str(varDict[key]), end="")
    print(")")
