"""
Contain code to alter students code so it jplag don't crash.
"""

def parse(code):
    """
    Call functions to alter the code so jplag can check it.
    """
    code = _remove_trailing_space(code)
    code = _add_ending_newline(code)
    return code



def _remove_trailing_space(code):
    """
    Jplag crash if a file ends with trailing spaces on an empty line.
    We fix it by removing all spaces at the end of code.
    """
    return code.rstrip()



def _add_ending_newline(code):
    """
    Jplag need the code to have an empty newline at the end.
    It can handle multiple newlines so we always add one
    """
    return code + "\n"
