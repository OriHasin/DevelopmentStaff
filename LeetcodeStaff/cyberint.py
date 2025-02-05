def add_prefix(func):
    def wrapper(*args, **kwargs):
        gen = func(args[0])
        for num in gen:
            yield "$"+num
    return wrapper



@add_prefix
def gen_num_coin(num):
    for i in range(num+1):
        yield str(i)+"$"


# Like performing the decorator itself
gen_num_coin = add_prefix(gen_num_coin)


gen = gen_num_coin(6)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))



def to_int(string):
    sum = 0
    pow = len(string)-1
    for idx in range(len(string)):
        sum += ((ord(string[idx]) - ord('0')) * (10 ** pow))
        pow -= 1
    return sum

print(to_int("303"))
