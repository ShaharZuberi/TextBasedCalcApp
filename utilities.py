import re


def is_int(num):
    """
    Checks if a num is a number using regex
    Info 1: We could possibly use exceptions instead of regex but they are more expensive to use in a workflow
    Info 2: This could be extended to support floats
    """
    p = r'^[-+]?(\d)+$' # possible positivity sign followed by digits
    if re.match(p, num):
        return True
    return False


def vars_to_string(varDict):
    if not varDict:
        print("No variables found.")
        return

    res = "("
    for idx, (key, value) in enumerate(varDict.items()):
        if idx > 0:
            res += ","
        res += str(key) + "=" + str(value)
    res += ")"
    return res
