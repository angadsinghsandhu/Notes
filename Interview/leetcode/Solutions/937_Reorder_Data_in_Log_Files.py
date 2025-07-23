# TODO

# File: Leetcode/Solutions/937_Reorder_Data_in_Log_Files.py

"""
Problem Number: 937
Problem Name: Reorder Data in Log Files
Difficulty: Medium
Tags: Array, String, Sorting
Company (Frequency): Google (30), Amazon (25), Facebook (20), Apple (15), Microsoft (10)
Leetcode Link: https://leetcode.com/problems/reorder-data-in-log-files/description/

DESCRIPTION

You are given an array of logs. Each log is a space-delimited string of words, where the first word is an identifier. There are two types of logs:

1. **Letter-logs:** All words (except the identifier) consist of lowercase English letters.
2. **Digit-logs:** All words (except the identifier) consist of digits.

Reorder the logs so that:

1. **All the letter-logs come before any digit-log.**
2. **The letter-logs are sorted lexicographically by their contents.** If their contents are identical, then sort them lexicographically by their identifiers.
3. **The digit-logs maintain their relative ordering.**

Return the final order of the logs.

---

#### Example 1:
**Input:**
```plaintext
logs = ["dig1 8 1 5 1","let1 art can","dig2 3 6","let2 own kit dig","let3 art zero"]
```

**Output:**
```plaintext
["let1 art can","let3 art zero","let2 own kit dig","dig1 8 1 5 1","dig2 3 6"]
```

**Explanation:**  
The letter-log contents are all different, so their ordering is "art can", "art zero", "own kit dig". The digit-logs remain in the same order.

#### Example 2:
**Input:**
```plaintext
logs = ["a1 9 2 3 1","g1 act car","zo4 4 7","ab1 off key dog","a8 act zoo"]
```

**Output:**
```plaintext
["g1 act car","a8 act zoo","ab1 off key dog","a1 9 2 3 1","zo4 4 7"]
```

**Explanation:**  
The letter-log contents are "act car", "act zoo", "off key dog". They are sorted lexicographically by content, and their relative ordering is preserved. The digit-logs remain in the same order.

#### Constraints:
- `1 <= logs.length <= 100`
- `3 <= logs[i].length <= 100`
- All the tokens of `logs[i]` are separated by a single space.
- `logs[i]` is guaranteed to have an identifier and at least one word after the identifier.
- The identifier consists of at most 10 alphanumeric characters.
- The words after the identifier consist of at most 10 lowercase English letters or digits.

"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem requires reordering an array of log strings based on specific rules.
    - Logs are categorized into two types:
        1. **Letter-logs:** Contain letters after the identifier.
        2. **Digit-logs:** Contain digits after the identifier.
    - The rules for ordering are:
        1. All letter-logs come before any digit-log.
        2. Letter-logs are sorted lexicographically by their content. If contents are identical, then sort by their identifiers.
        3. Digit-logs retain their original order.
    - To achieve this, we can use Python's built-in `sorted` function with a custom sorting key.
    - The key function will prioritize letter-logs over digit-logs and sort them accordingly.

    Input:
        logs: List[str] - An array of log strings.

    Output:
        List[str] - The reordered array of log strings following the specified rules.
    """

    def reorderLogFiles(self, logs: List[str]) -> List[str]:
        """
        Approach:
        - Define a key function that distinguishes between letter-logs and digit-logs.
        - For letter-logs, the key is a tuple: (0, content, identifier).
            - The leading 0 ensures that letter-logs come before digit-logs.
            - Sorting by content and then by identifier ensures proper ordering.
        - For digit-logs, the key is a tuple: (1,). 
            - The leading 1 ensures that digit-logs come after letter-logs.
            - Since there are no further elements in the tuple, digit-logs maintain their original order.
        - Use the `sorted` function with this key to reorder the logs accordingly.

        T.C.: O(N log N), where N is the number of logs, due to sorting.
        S.C.: O(N), space used by the sorted function.

        Parameters:
            logs (List[str]): The list of log strings to be reordered.

        Returns:
            List[str]: The reordered list of log strings.
        """
        def get_log_key(log: str):
            # Split log into identifier and the rest
            identifier, content = log.split(' ', 1)
            # Check if it's a letter-log or digit-log
            if content[0].isalpha():
                # Return a tuple that ensures letter-logs come first, then sorted by content and identifier
                return (0, content, identifier)
            else:
                # Digit-logs come after letter-logs; the tuple ensures they maintain original order
                return (1,)

        # Sort logs using the key function
        return sorted(logs, key=get_log_key)

    def reorderLogFiles_alternative(self, logs: List[str]) -> List[str]:
        """
        Alternative Approach:
        - Split the logs into two separate lists: letter_logs and digit_logs.
        - Sort the letter_logs based on the content and then by identifier.
        - Concatenate the sorted letter_logs with the original order of digit_logs.

        T.C.: O(N log N), where N is the number of logs, due to sorting.
        S.C.: O(N), space used by the additional lists.

        Parameters:
            logs (List[str]): The list of log strings to be reordered.

        Returns:
            List[str]: The reordered list of log strings.
        """
        letter_logs = []
        digit_logs = []

        for log in logs:
            identifier, content = log.split(' ', 1)
            if content[0].isalpha():
                letter_logs.append((content, identifier))
            else:
                digit_logs.append(log)

        # Sort letter_logs lexicographically by content, then by identifier
        letter_logs.sort()

        # Reconstruct the sorted letter logs
        sorted_letter_logs = [f"{identifier} {content}" for content, identifier in letter_logs]

        # Concatenate sorted letter logs with digit logs
        return sorted_letter_logs + digit_logs

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    logs1 = ["dig1 8 1 5 1","let1 art can","dig2 3 6","let2 own kit dig","let3 art zero"]
    print("Test Case 1:")
    print(f"Input Logs: {logs1}")
    print(f"Output (Sorted Logs): {solution.reorderLogFiles(logs1)}")
    print()

    # Test case 2
    logs2 = ["a1 9 2 3 1","g1 act car","zo4 4 7","ab1 off key dog","a8 act zoo"]
    print("Test Case 2:")
    print(f"Input Logs: {logs2}")
    print(f"Output (Sorted Logs): {solution.reorderLogFiles(logs2)}")
    print()

    # Test case 3
    logs3 = ["let1 art can","let2 art can","dig1 3 6","let3 art zero"]
    print("Test Case 3:")
    print(f"Input Logs: {logs3}")
    print(f"Output (Sorted Logs): {solution.reorderLogFiles(logs3)}")
    print()

    # Test case 4
    logs4 = ["dig1 8 1 5 1","dig2 3 6","dig3 4 5","dig4 7 8"]
    print("Test Case 4:")
    print(f"Input Logs: {logs4}")
    print(f"Output (Sorted Logs): {solution.reorderLogFiles(logs4)}")
    print()

    # Test case 5
    logs5 = ["let1 abc def","let2 abc def","let3 abc xyz","dig1 1 2","dig2 3 4"]
    print("Test Case 5:")
    print(f"Input Logs: {logs5}")
    print(f"Output (Sorted Logs): {solution.reorderLogFiles(logs5)}")
    print()