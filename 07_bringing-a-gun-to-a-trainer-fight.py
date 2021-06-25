"""
Bringing a Gun to a Trainer Fight
=================================

Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny 
trainers! Fortunately, you grabbed a beam weapon from an abandoned storeroom 
while you were running through the station, so you have a chance to fight your 
way out. But the beam weapon is potentially dangerous to you as well as to the 
bunny trainers: its beams reflect off walls, meaning you'll have to be very 
careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming 
too weak to cause damage. You also know that if a beam hits a corner, it will 
bounce back in exactly the same direction. And of course, if the beam hits 
either you or the bunny trainer, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, trainer_position, 
distance) that gives an array of 2 integers of the width and height of the 
room, an array of 2 integers of your x and y coordinates in the room, an array 
of 2 integers of the trainer's x and y coordinates in the room, and returns 
an integer of the number of distinct directions that you can fire to hit the 
elite trainer, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 
1250]. You and the elite trainer are both positioned on the integer lattice at 
different distinct positions (x, y) inside the room such that [0 < x < 
x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can 
travel before becoming harmless will be given as an integer 1 < distance 
<= 10000.

For example, if you and the elite trainer were positioned in a room with 
dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum 
shot distance of 4, you could shoot in seven different directions to hit the 
elite trainer (given as vector bearings from your location): [1, 0], [1, 2], 
[1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot 
at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot 
at bearing [-3, -2] bounces off the left wall and then the bottom wall before 
hitting the elite trainer with a total shot distance of sqrt(13), and the shot 
at bearing [1, 2] bounces off just the top wall before hitting the elite 
trainer with a total shot distance of sqrt(5).

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases -- 
Input:
solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9
"""

def solution(dimensions, player_position, target_position, beam_range):
    WIDTH = dimensions[0]
    HEIGHT = dimensions[1]
    RANGE2 = beam_range ** 2

    # center coordinates on player:
    TARGET_X = target_position[0] - player_position[0]
    TARGET_Y = target_position[1] - player_position[1]
    PLAYER_MIRROR_X = WIDTH - 2 * player_position[0]
    TARGET_MIRROR_X = WIDTH - 2 * target_position[0]
    PLAYER_MIRROR_Y = HEIGHT - 2 * player_position[1]
    TARGET_MIRROR_Y = HEIGHT - 2 * target_position[1]

    # Tier 0: current room
    players = set()
    targets = set()
    if TARGET_X ** 2 + TARGET_Y ** 2 <= RANGE2:
        targets.add(normalize(TARGET_X, TARGET_Y))

    # Tier 1 to max beam range
    max_tier = int(ceil(float(beam_range) / min(WIDTH, HEIGHT)) + 1)
    for tier in range(1, max_tier):
        for tile in tiles_in_tier(tier):
            # calculate x coordinates relative to player
            player_x = tile[0] * WIDTH
            target_x = player_x + TARGET_X
            if tile[0] % 2 != 0:
                # if tile x coordinate is odd, positions are mirrored
                player_x += PLAYER_MIRROR_X
                target_x += TARGET_MIRROR_X
            # calculate y coordinates
            player_y = tile[1] * HEIGHT
            target_y = player_y + TARGET_Y
            if tile[1] % 2 != 0:
                # if tile y coordinate is odd, positions are mirrored
                player_y += PLAYER_MIRROR_Y
                target_y += TARGET_MIRROR_Y
            # check max range
            player_distance = player_x ** 2 + player_y ** 2
            target_distance = target_x ** 2 + target_y ** 2
            # if both player and target are out or range abort early
            if player_distance > RANGE2 and target_distance > RANGE2: continue
            # otherwise calculate normalized vectors for player and target
            player_vector = normalize(player_x, player_y)
            target_vector = normalize(target_x, target_y)
            # entity closest to the origin will be handled first
            if target_distance < player_distance:
                if target_vector not in players:
                    targets.add(target_vector)
                if player_vector not in targets and player_distance <= RANGE2:
                    players.add(player_vector)
            else:
                if player_vector not in targets:
                    players.add(player_vector)
                if target_vector not in players and target_distance <= RANGE2:
                    targets.add(target_vector)
    
    # diagnostic output:
    # print(f'{players = }')
    # print(f'{targets = }')
    return len(targets)


def tiles_in_tier(tier):
    if not isinstance(tier, int): raise TypeError("tier must be a positive integer")
    if tier < 0: raise ValueError("tier must be a positive integer")
    if tier == 0: return [(int(0), int(0))]
    # generate tiles is first 8th of circle (0 < phi < 45)
    tiles = [(tier, i) for i in range(1, tier)]
    # add tiles between 45 and 90
    tiles += [(y, x) for x, y in tiles]
    # add tile at 45
    tiles += [(tier, tier)]
    # add second quarter
    tiles += [(-x, y) for x, y in tiles]
    # add 3rd and 4th quarter
    tiles += [(x, -y) for x, y in tiles]
    # add tiles on axis
    tiles += [(tier, 0), (0, tier), (-tier, 0), (0, -tier)]
    return tiles


def normalize(x, y):
    """Find the greatest common factor between x and y and apply it to both.
    The sign of both numbers will be preserved."""
    if x == 0 and y == 0:
        raise ValueError("Can't normalize vector of length 0")
    # catch edge cases where x or y == 0
    if x == 0: return int(x), int(-1 if y < 0 else 1)
    if y == 0: return int(-1 if x < 0 else 1), int(y)
    # find prime factors of x and y
    fx, fy = factorize(abs(x)), factorize(abs(y))
    # use the shorter of the 2 lists to search common factors in both lists
    shorter, longer = sorted([fx, fy], key=len)
    gcf = 1             # greatest common factor
    for factor in shorter:
        if factor in longer:
            gcf *= factor
            longer.remove(factor)
    return int(x / gcf), int(y / gcf)
    

def factorize(n):
    """split n into prime factors using the generated 'PRIMES' lookup table"""
    if not isinstance(n, int): raise TypeError("n must be a positive integer")
    if n < 1: raise ValueError("n must be a positive integer")
    factors = []
    while n > 1:
        factors.append(PRIMES[n])
        n //= PRIMES[n]
    return factors


def prime_lut(n):
    """build lookup table for the smallest prime factor of each number up to n"""
    if not isinstance(n, int): raise TypeError("n must be a positive integer")
    if n < 1: raise ValueError("n must be a positive integer")
    lut = list(range(n + 1))
    for i in range(2, int(sqrt(n)) + 1):
        # if i is not a prime number, we can skip it
        if lut[i] != i: continue
        for j in range(2 * i, len(lut), i):
            # if no factors are registerd for j, register i as smallest factor
            if lut[j] == j: lut[j] = i
    return lut


from math import ceil, sqrt
PRIMES = prime_lut(10000 + 1250)

if __name__ == '__main__':
    # test: (should be 9)
    print(solution([300,275], [150,150], [185,100], 500))
