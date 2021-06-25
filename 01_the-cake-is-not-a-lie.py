""" 
the-cake-is-not-a-lie
Write a function called solution(s) that, given a non-empty string less than 
200 characters in length describing the sequence of M&Ms, returns the maximum 
number of equal parts that can be cut from the cake without leaving any 
leftovers.
"""

import re

def solution(sequence):
    pattern = re.compile(r"^([a-z]+?)+$")
    # [a-z]+? -> match shortest sequence of characters possible
    # (...)\1+? -> match the previous match as often as possible
    # no other characters before after or between matches allowed
    match = pattern.match(sequence)
    if match is None:
        return 1
    else:
        return len(sequence) // len(match.group(1))