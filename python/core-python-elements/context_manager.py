""" A context manager is a Python construct that allows you to manage resources such as files, database connections,
or locks efficiently.  A class-based context manager needs to implement two methods: __enter__() and __exit__().
We can also use if for Locks by self.lock.acquire() and self.lock.release() in the corresponding methods.
the exception params in __exit__() is for handling exceptions that happens in with statement. """

class ContextResourceManager:

    def __init__(self, file_name, mode):
        self.file = open(file_name, mode)

    def __enter__(self):
        print("start running default __enter__() function...")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("close the resource, running __exit__() function...")
        self.file.close()

def custom_open(file_name, mode):
    return ContextResourceManager(file_name, mode)



with custom_open("txt_file", "rt") as f:
    data = f.read()
    print(f'I have read : \n{data}')
