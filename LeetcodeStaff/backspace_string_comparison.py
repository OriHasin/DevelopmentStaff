"""
Problem Statement
Given two strings s and t, where '#' represents a backspace character, determine if they are equal after processing all backspaces.


Example:
Input: s = "ab#c", t = "ad#c"
Output: True
Explanation: Both become "ac" after processing backspaces.
"""


def str_backslash_comparison(s: str, t: str) -> bool:
    i, j = len(s) - 1, len(t) - 1
    backspace_s = backspace_t = 0  # Track backspaces

    while i >= 0 or j >= 0:

        while i >= 0:
            if s[i] == '#':
                backspace_s += 1
                i -= 1
            elif backspace_s > 0:
                backspace_s -= 1
                i -= 1
            else:
                break  # Valid character found


        while j >= 0:
            if t[j] == '#':
                backspace_t += 1
                j -= 1
            elif backspace_t > 0:
                backspace_t -= 1
                j -= 1
            else:
                break

        # Compare characters
        if i >= 0 and j >= 0 and s[i] != t[j]:
            return False

        # If one string is exhausted while the other is not
        if (i >= 0) != (j >= 0):
            return False

        i -= 1
        j -= 1

    return True


print(str_backslash_comparison("ab#c", "ad#c"))
print(str_backslash_comparison("a##c", "#a#c"))
print(str_backslash_comparison("a###c", "c"))
print(str_backslash_comparison("ab###c", "c"))
print(str_backslash_comparison("a#c", "b"))

