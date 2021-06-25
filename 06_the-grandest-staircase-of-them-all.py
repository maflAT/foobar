"""
The Grandest Staircase Of Them All
==================================

With the LAMBCHOP doomsday device finished, Commander Lambda is preparing to 
debut on the galactic stage -- but in order to make a grand entrance, Lambda 
needs a grand staircase! As the Commander's personal assistant, you've 
been tasked with figuring out how to build the best staircase EVER. 

Lambda has given you an overview of the types of bricks available, plus a 
budget. You can buy different amounts of the different types of bricks (for 
example, 3 little pink bricks, or 5 blue lace bricks). Commander Lambda wants 
to know how many different types of staircases can be built with each amount of 
bricks, so they can pick the one with the most options. 

Each type of staircase should consist of 2 or more steps.  No two steps are 
allowed to be at the same height - each step must be lower than the previous 
one. All steps must contain at least one brick. A step's height is 
classified as the total amount of bricks that make up that step.
For example, when N = 3, you have only 1 choice of how to build the staircase, 
with the first step having a height of 2 and the second step having a height of 
1: (# indicates a brick)

#
##
21

When N = 4, you still only have 1 staircase choice:

#
#
##
31
 
But when N = 5, there are two ways you can build a staircase from the given 
bricks. The two staircases can have heights (4, 1) or (3, 2), as shown below:

#
#
#
##
41

#
##
##
32

Write a function called solution(n) that takes a positive integer n and returns 
the number of different staircases that can be built from exactly n bricks. n 
will always be at least 3 (so you can have a staircase at all), but no more 
than 200, because Commander Lambda's not made of money!

Input:
Solution.solution(3)
Output:
    1

Input:
Solution.solution(200)
Output:
    487067745
"""

def solution(n):

    def stairs(bricks, max_height):
        # search cached result for combination of bricks and height constraint
        if bricks in cache and max_height in cache[bricks]: 
            return cache[bricks][max_height]

        if bricks <= 2: return 1    # only one column possible
        
        """multiple columns: 
        add all possible combinations ranging from maximum number of bricks in 
        single column, while staying below the previous column;
        down to minimum number of bricks in one column while still maintaining 
        minimum one step difference to the next column."""
        # determine how many bricks must go into the next columns to the right
        min_to_the_right = max(0, bricks - max_height)
        max_to_the_right = bricks - MIN_STAIR_HEIGHT[bricks]
        combinations = 0
        for i in range(min_to_the_right, max_to_the_right + 1):
            height_limit = min(bricks - i - 1, i)
            #sanity check: limit can't be negative of > number of bricks
            assert 0 <= height_limit <= i 
            combinations += stairs(i, height_limit)
        # cache result for combination of bricks and height constraint
        cache.setdefault(bricks, {})[max_height] = combinations
        return combinations


    def generate_stack_heights(bricks=250):
        """Generate lookup tables 
        'height_map': gives the minimum height (shallowest staircaise) possible 
        for the given number of bricks.
        reversed_height_map: gives the maximum number of bricks that can fit into
        the given height"""
        height_map = {}
        reversed_height_map = {}
        heigth = 0
        next_step_at = 1
        for n in range(bricks):
            if n >= next_step_at:
                reversed_height_map[heigth] = n - 1
                heigth += 1
                next_step_at += heigth
            height_map[n] = heigth
        return height_map, reversed_height_map
        

    MIN_STAIR_HEIGHT, MAX_BRICK_COUNT = generate_stack_heights(250)
    cache = {}
    return stairs(n, n - 1) # edge case all bricks in single column not allowed
