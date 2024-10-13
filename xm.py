def strip(str, delimiter = " "):

    numbers_of_delimiters = str.count(delimiter)
    string_len = len(str)

    valid_chars = [None] * (string_len - numbers_of_delimiters)

    valid_chars_index = 0
    for char in str:
        if char != delimiter:
            valid_chars[valid_chars_index] = char
            valid_chars_index += 1

    return "".join(valid_chars)



if __name__ == '__main__':

    print(strip("a      c     de"))
    print(strip("a      c     de", "?"))
    print(strip("acde"))