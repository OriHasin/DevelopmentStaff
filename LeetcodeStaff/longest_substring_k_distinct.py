"""Problem Statement:
Given a string s and an integer k, find the length of the longest substring that contains at most k distinct characters."""




def longest_k_distinct(s: str, k: int) -> int:
    if k == 0:
        return 0

    char_count = {}  # Dictionary to count occurrences of characters
    left = 0
    max_len = 0

    for right in range(len(s)):
        char_count[s[right]] = char_count.get(s[right], 0) + 1  # Always adding new char (expanding), then check if substring is valid or not (shrink)

        # Shrink the window until we have at most k distinct characters
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]  # Remove character from dictionary
            left += 1  # Move left pointer forward

        max_len = max(max_len, right - left + 1)  # Update max length

    return max_len



print(longest_k_distinct("araaci", 2))  # Output: 4
print(longest_k_distinct("araace", 1))  # Output: 2
print(longest_k_distinct("cbbebi", 3))  # Output: 5



