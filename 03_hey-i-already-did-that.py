from itertools import count

def solution(n, b):
    k = len(n)
    numbers = {}
    for i in count():
        # remember n and its position in the sequence
        numbers[n] = i

        # calculate x and y as strings containing the sorted digits of n
        y = ''.join(sorted(n))
        x = y[::-1]

        # convert x and y to int and calculate z as x - y
        z = from_base_x(x, b) - from_base_x(y, b)

        # convert z back to string in base b, padding to length k with zeros
        n = in_base_x(z, b).rjust(k, '0')

        # search for previous occurance of n
        # if found, return difference between index of n and length of list
        # else repeat from above
        if n in numbers: return len(numbers) - numbers[n]
    

def from_base_x(num_string, base):
    """get integer value of number, that is represented as str in base x"""
    if not 2 <= base <= 10: 
        raise ValueError("Base must be between 2 and 10!")
    num_int = 0
    for position, digit in enumerate(reversed(num_string), 0):
        if int(digit) >= base: 
            raise ValueError('All digits must be smaller than base!')
        num_int += int(digit) * base ** position
    return num_int

def in_base_x(num, base):
    """convert integer number to string of number in base x"""
    if not 2 <= base <= 10: 
        raise ValueError("Base must be between 2 and 10!")
    num_string = ''
    while num > 0:
        num_string = str(num % base) + num_string
        num //= base
    return num_string
