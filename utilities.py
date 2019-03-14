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



