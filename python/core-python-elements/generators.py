""" A generator is a special type of iterator that generates values on the fly using the yield statement, instead of
loading everything into memory at once.
Every time yield is encountered, the function returns a value but remembers where it left off for the next call.
This allows handling large sequences efficiently, since only one value is produced at a time.

When we use yield keyword inside a function, this function automatically return a generator, not a specific return type.
Inorder to access specific elements, we have to use next(generator_object) function."""


def generate_even_numbers(limit = 100):
    num = 0
    while num <= limit:
        yield num
        num += 2


even_generators = generate_even_numbers()

# This is automatically doing next() on the generator until StopIteration is raised.
for even in even_generators:
    print(even)