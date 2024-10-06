def read_large_file(file_name):
    with open(file_name) as f:
        for line in f:
            yield line

def process_line(line):
    print(line.strip())

file_generator = read_large_file("txt_file")

# Process one line at a time
for line in file_generator:
    process_line(line)
