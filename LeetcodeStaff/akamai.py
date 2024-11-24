
def make_blocks(small, big, goal):
    if small < 0 or big < 0:
        return False

    if small*1 + big*5 == goal:
        return True

    return make_blocks(small-1, big, goal) or make_blocks(small, big-1, goal)


# print(make_blocks(3,1,8))
# print(make_blocks(3,1,9))
# print(make_blocks(3,2,10))
# print(make_blocks(2000,2000,2))



def make_blocks_iter(small, big, goal):
    if small < 0 or big < 0 or goal < 0:
        return False
    lst = [[ (j*5 + i*1 == goal) for j in range(big+1)] for i in range(small+1)]
    return any(lst)

    for i in range(small+1):
        for j in range(big+1):
            if i*1 + j*5 == goal:
                print(f'small: {i}, big: {j}, goal: {goal}')
                return True
    return False


print(make_blocks_iter(3,1,8))
print(make_blocks_iter(3,1,9))
print(make_blocks_iter(3,2,10))
print(make_blocks_iter(2000,2000,2))
print(make_blocks_iter(2000,2000,11017))



