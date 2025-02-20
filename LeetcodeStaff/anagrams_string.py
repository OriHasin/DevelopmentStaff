"""
Problem Statement: String Anagrams (Hard)
Given a string s and a pattern p, find all starting indices of p's anagrams in s.

An anagram is a permutation of characters. In other words, find all substrings in s that are permutations of p.

Example:
Input: s = "cbaebabacd", p = "abc"
Output: [0, 6]
Explanation: The substrings starting at indices 0 ("cba") and 6 ("bac") are anagrams of "abc".
"""

from collections import Counter


def find_anagrams(s: str, p: str) -> list[int]:
    if len(p) > len(s):
        return []

    p_count = Counter(p)
    s_count = Counter(s[:len(p)])

    result = []
    left = 0

    if s_count == p_count:
        result.append(0)  # If first window is an anagram, store index 0

    for right in range(len(p), len(s)):
        s_count[s[right]] += 1  # Add new character to window
        s_count[s[left]] -= 1  # Remove leftmost character from window

        if s_count[s[left]] == 0:
            del s_count[s[left]]

        left += 1

        if s_count == p_count:
            result.append(left)

    return result


# Testing
print(find_anagrams("cbaebabacd", "abc"))  # Output: [0, 6]
print(find_anagrams("abab", "ab"))  # Output: [0, 1, 2]




