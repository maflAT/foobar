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
from math import sqrt
from pprint import pprint

def solution(dimensions, player_position, target_position, beam_range):
    WIDTH = dimensions[0]
    HEIGHT = dimensions[1]
    RANGE2 = beam_range ** 2
    # TILES_X = range(-ceil(beam_range / WIDTH), ceil(beam_range / WIDTH))
    # TILES_Y = range(-ceil(beam_range / HEIGHT), ceil(beam_range / HEIGHT))

    # center coordinates on player:
    WESTWALL = -player_position[0]
    EASTWALL = dimensions[0] - player_position[0]
    NORTHWALL = -player_position[1]
    SOUTHWALL = dimensions[1] - player_position[1]
    TARGET_X = target_position[0] - player_position[0]
    TARGET_Y = target_position[1] - player_position[1]
    PLAYER_MIRROR_X = WIDTH - 2 * player_position[0]
    TARGET_MIRROR_X = WIDTH - 2 * target_position[0]
    PLAYER_MIRROR_Y = HEIGHT - 2 * player_position[1]
    TARGET_MIRROR_Y = HEIGHT - 2 * target_position[1]

    # Tier 0: current room
    players = []
    targets = []
    if TARGET_X ** 2 + TARGET_Y ** 2 <= RANGE2:
        targets.append((TARGET_X, TARGET_Y))

    # Tier 1: first mirrored layer around room
    for tier in range(1, 3):
        for tile in tiles_in_tier(tier):
            if tile[0] % 2 == 0:
                player_x = tile[0] * WIDTH
                target_x = tile[0] * WIDTH + TARGET_X
            else:
                player_x = tile[0] * WIDTH + PLAYER_MIRROR_X
                target_x = tile[0] * WIDTH + TARGET_MIRROR_X + TARGET_X
            if tile[1] % 2 == 0:
                player_y = tile[1] * HEIGHT
                target_y = tile[1] * HEIGHT + TARGET_Y
            else:
                player_y = tile[1] * HEIGHT + PLAYER_MIRROR_Y
                target_y = tile[1] * HEIGHT + TARGET_MIRROR_Y + TARGET_Y
            if player_x ** 2 + player_y ** 2 <= RANGE2:
                players.append((player_x, player_y))
            targets.append((target_x, target_y))

    pprint(players)
    pprint(targets)


def factorize(n: int):
    if not isinstance(n, int): raise TypeError("n must be a positive integer")
    if n < 1: raise ValueError("n must be a positive integer")
    factors = []
    while n > 1:
        for prime in PRIMES:
            if n % prime == 0:
                factors.append(prime)
                n //= prime
                break
    return factors

def tiles_in_tier(tier: int):
    if not isinstance(tier, int): raise TypeError("tier must be a positive integer")
    if tier < 0: raise ValueError("tier must be a positive integer")
    if tier == 0: return [(int(0), int(0))]
    # generate tiles is first 8th of circle (0° < phi < 45°)
    tiles = [(tier, i) for i in range(1, tier)]
    # add tiles between 45° and 90°
    tiles += [(y, x) for x, y in tiles]
    # add tile at 45°
    tiles += [(tier, tier)]
    # add second quarter
    tiles += [(-x, y) for x, y in tiles]
    # add 3rd and 4th quarter
    tiles += [(x, -y) for x, y in tiles]
    # add tiles on axis
    tiles += [(tier, 0), (0, tier), (-tier, 0), (0, -tier)]
    return tiles

def prime_lut(n: int):
    """build lookup table for the smallest prime factor of each number up to n"""
    if not isinstance(n, int): raise TypeError("n must be a positive integer")
    if n < 1: raise ValueError("n must be a positive integer")
    lut = list(range(n + 1))
    for i in range(2, int(sqrt(n)) + 1):
        if lut[i] != i: continue    # i is not prime so we can skip it
        for j in range(2 * i, len(lut), i):
            if lut[j] == j: lut[j] = i # register i as smallest prime factor of j
    return lut

PRIMES = prime_lut(10000 + 1250)

solution([3,2], [1,1], [2,1], 4)

    # room = {
    #     'width': dimensions[0],
    #     'height': dimensions[1],
    #     'player': Player(player_position[0], player_position[1]),
    #     'target': Target(target_position[0], target_position[1]),

    # }
# Project rooms (trainer and player locations) in each direction 

# Mirror x-coordinates for each iteration in x-direction

# Mirror y-coordinates for each iteration in y-direction

# Stop if distance to trainer exceeds maximum beam distance

# check against known target vectors

# check against known trainer vectors

# add normalized target vector to results

# add normalized player vector to results

# class Room(object):
#     def __init__(self, dimensions, player_pos, target_pos) -> None:
#         self.width = dimensions[0]
#         self.heigth = dimensions[1]
#         self.player = player_pos
#         self.target = target_pos

#     def project(direction):

