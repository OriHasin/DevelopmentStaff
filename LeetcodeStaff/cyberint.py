
def prefix_coin(func):
    print("runs before calling the function")
    def wrapper(num, *args, **kwargs):
        gen = func(num)
        for element in gen:
            yield "$" + element
    return wrapper




def gen_num_coin(num):
    print(1)
    for i in range(num+1):
        print(2)
        yield str(i)+"$"
        print(3)

gen_num_coin = prefix_coin(gen_num_coin)


gen = gen_num_coin(6)

print(next(gen))
print(next(gen))
print(next(gen))



def to_string(string):
    print(ord(string[0]))
    (ord(string[char]) -ord(0))

to_string("023")
