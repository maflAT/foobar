"""
Running with Bunnies
====================

You and the bunny workers need to get out of this collapsing death 
trap of a space station -- and fast! Unfortunately, some of the 
bunnies have been weakened by their long work shifts and can't 
run very fast. Their friends are trying to help them, but this 
escape would go a lot faster if you also pitched in. The defensive 
bulkhead doors have begun to close, and if you don't make it 
through in time, you'll be trapped! You need to grab as many 
bunnies as you can and get through the bulkheads before they close. 

The time it takes to move from your starting point to all of the 
bunnies and to the bulkhead will be given to you in a square matrix 
of integers. Each row will tell you the time it takes to get to the 
start, first bunny, second bunny, ..., last bunny, and the bulkhead 
in that order. The order of the rows follows the same pattern 
(start, each bunny, bulkhead). The bunnies can jump into your arms, 
so picking them up is instantaneous, and arriving at the bulkhead at 
the same time as it seals still allows for a successful, if 
dramatic, escape. (Don't worry, any bunnies you don't pick 
up will be able to escape with you since they no longer have to 
carry the ones you did pick up.) You can revisit different spots if 
you wish, and moving to the bulkhead doesn't mean you have to 
immediately leave -- you can move to and from the bulkhead to pick 
up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths 
interact with the space station's security checkpoints and add 
time back to the clock. Adding time to the clock will delay the 
closing of the bulkhead doors, and if the time goes back up to 0 or 
a positive number after the doors have already closed, it triggers 
the bulkhead to reopen. Therefore, it might be possible to walk in a 
circle and keep gaining time: that is, each time a path is 
traversed, the same amount of time is used or added.

Write a function of the form solution(times, time_limit) to 
calculate the most bunnies you can pick up and which bunnies they 
are, while still escaping through the bulkhead before the doors 
close for good. If there are multiple sets of bunnies of the same 
size, return the set of bunnies with the lowest worker IDs (as 
indexes) in sorted order. The bunnies are represented as a sorted 
list by worker ID, with the first bunny being 0. There are at most 5 
bunnies, and time_limit is a non-negative integer that is at most
999.
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the 
starting point, bunny 0, bunny 1, bunny 2, and the bulkhead door 
exit respectively. You could take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the 
best combination for this space station hallway, so the solution is 
[1, 2].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown 
here.

-- Python cases -- 
Input:
solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, 
-1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output:
    [1, 2]

Input:
solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 
1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
Output:
    [0, 1]
"""

# def test():
#     test_cases = [
#         ([[0, 2, 2, 2, -1], 
#           [9, 0, 2, 2, -1], 
#           [9, 3, 0, 2, -1], 
#           [9, 3, 2, 0, -1], 
#           [9, 3, 2, 2, 0]], 1),
#         ([[0, 1, 1, 1, 1], 
#           [1, 0, 1, 1, 1], 
#           [1, 1, 0, 1, 1], 
#           [1, 1, 1, 0, 1], 
#           [1, 1, 1, 1, 0]], 3)]
#     print(solution(*(test_cases)[0]))
#     print(solution(*(test_cases)[1]))

def solution(times, time_limit):
    global TIMES, ROUTES, SIZE, BUNNIES
    SIZE = len(times)
    TIMES, ROUTES = find_shortcuts(times)
    BUNNIES = list(range(1, SIZE - 1))
    if find_loops(TIMES): return [b - 1 for b in BUNNIES]
    if TIMES[0][SIZE - 1] > time_limit: return []
    bunnies = traverse(cur_pos=0, target=0, time_left=time_limit, bunnies=[])
    if bunnies == False: return []
    return [b - 1 for b in bunnies]

def traverse(cur_pos, target, time_left, bunnies):
    """
    recursive function for traversing through nodes, 
    keeping track of collected bunnies and remaining time
    """
    # if if time to bulkhead > time left: return false
    if TIMES[cur_pos][SIZE - 1] > time_left: return False
    # if all bunnies collected and time to bulkhead <= time left: done (return bunnies)
    if cur_pos in BUNNIES and cur_pos not in bunnies:
        bunnies.append(cur_pos)
        bunnies.sort()
    # if current position is a shortcut node immediately traverse to next node
    if cur_pos != target:
        next_pos = ROUTES[cur_pos][target]
        return traverse(cur_pos=next_pos,
                        target=target,
                        time_left=time_left - TIMES[cur_pos][next_pos], 
                        bunnies=bunnies[:])
    if bunnies == BUNNIES: return bunnies
    # traverse to next bunny with lowest id
    missing_bunnies = [b for b in BUNNIES if b not in bunnies]
    results = []
    for bunny in missing_bunnies:
        next_pos = ROUTES[cur_pos][bunny]
        returned = traverse(cur_pos=next_pos,
                            target=bunny,
                            time_left=time_left - TIMES[cur_pos][next_pos], 
                            bunnies=bunnies[:])
        # if traversal to current bunny failed, continue with next
        if returned == False: continue
        # if all bunnies collected => done
        if returned == BUNNIES: return bunnies
        # else remember returned bunny list
        results.append(returned)
    # if at least one bunny list returned successfully:
    # return longest bunny list with lowest ids
    if len(results) > 0: 
        max_len = max(len(r) for r in results)
        results = (r for r in results if len(r) == max_len)
        return sorted(results)[0]
    # if all bunnies returned false: return current bunny list
    return bunnies

def find_shortcuts(time_table):
    """check if there are shorter paths between 2 nodes going through other nodes"""
    from itertools import product
    # table containing shortest times between nodes
    times = [[col for col in row] for row in time_table]
    # table containing each path with the shortest time
    routes = [[dest for dest in range(SIZE)] for _ in range(SIZE)]

    for sc in range(SIZE):
        for x, y in product(range(SIZE), repeat=2):
            if sc == x or sc == y: continue 
            if times[x][y] > times[x][sc] + times[sc][y]:
                times[x][y] = times[x][sc] + times[sc][y]
                routes[x][y] = routes[x][sc]
    return times, routes

def find_loops(time_table):
    """check if there are any positive feedback loops, allowing for infinite time"""
    for y in range(len(time_table)):
        for x in range(y + 1):
            if time_table[x][y] + time_table[y][x] < 0: return True

# test()