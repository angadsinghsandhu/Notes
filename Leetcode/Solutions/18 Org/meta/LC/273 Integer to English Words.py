# INTEGER TO ENGLISH WORDS

# Problem number: 273
# Difficulty: Hard
# Tags: String, Math, Recursion
# Link: https://leetcode.com/problems/integer-to-english-words/

class Solution:
    """
    The problem requires converting a non-negative integer to its English word representation.
    We need to break the number into groups of thousands and convert each group to words.

    To solve this, we will:
    1. Define the English word mapping for single digits, tens, and teens.
    2. Handle the number in groups of thousands (e.g., 1234567 -> "One Million Two Hundred Thirty Four Thousand...").
    3. Recursively build the word representation for each group.

    We'll use recursion to handle each chunk of thousands, building the English representation.
    """

    LESS_THAN_20 = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
                    "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    THOUSANDS = ["", "Thousand", "Million", "Billion"]

    def numberToWords(self, num: int) -> str:
        """
        Main method to convert number to words.

        T.C. : O(n) where n is the number of digits in the input
        S.C. : O(1) except for recursion depth which depends on the number of chunks of thousands
        """
        if num == 0:
            return "Zero"

        res = ''
        i = 0

        # Process the number in chunks of thousands
        while num > 0:
            if num % 1000 != 0:
                res = self.helper(num % 1000) + self.THOUSANDS[i] + ' ' + res
            num //= 1000
            i += 1

        return res.strip()

    def helper(self, num: int) -> str:
        """
        Helper function to process numbers below 1000.
        """
        if num == 0:
            return ''
        elif num < 20:
            return self.LESS_THAN_20[num] + ' '
        elif num < 100:
            return self.TENS[num // 10] + ' ' + self.helper(num % 10)
        else:
            return self.LESS_THAN_20[num // 100] + ' Hundred ' + self.helper(num % 100)
