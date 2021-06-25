"""
| 7
| 4 8
| 2 5 9
| 1 3 6 10
Each cell can be represented as points (x, y), with x being the distance from 
the vertical wall, and y being the height from the ground. For example, the 
bunny worker at (1, 1) has ID 1, the bunny worker at (3, 2) has ID 9, and the 
bunny worker at (2,3) has ID 8. This pattern of numbering continues 
indefinitely (Commander Lambda has been adding a LOT of workers). 

Write a function solution(x, y) which returns the worker ID of the bunny at 
location (x, y). Each value of x and y will be at least 1 and no greater than 
100,000. Since the worker ID can be very large, return your solution as a 
string representation of the number.

1.) ID can be split up into a base value per 'level' + an offset:
    'base': 7       'offset': 0         a) 'base' is a function of (x + y):
            4 7               0 1           (1+4), (2+3), (3+2), (1+4) 
            2 4 7             0 1 2         all result in 'base' = 7
            1 2 4 7           0 1 2 3   b) 'offset' is simply (x - 1)

2.) Find function for 'base':
    a) delta between two 'base' values seems to increase linearly
       -> looks like second order polynomial function.
    b) solving for y = ax^2 + bx + c either by hand or using:
       https://www.wolframalpha.com/input/?i=interpolating+polynomial+%7B%7B2%2C1%7D%2C%7B3%2C2%7D%2C%7B4%2C4%7D%2C%7B5%2C7%7D%7D
       gives us: 'x^2/2 - 3x/2 + 2'
    c) don't forget that the 'x' in this equation actually represents our input 
       parameters '(x + y)' and 'y' = 'base'

3.) recombining 'base' + 'offset' gives us the result:
    ID = (x + y)**2 / 2 - (x + y) * 3 / 2 + x + 1
    =============================================
"""

def solution(x, y):
    id_ = ((x + y)**2 / 2) - ((x + y) * 3 / 2) + x + 1
    return '{0:.0f}'.format(id_)