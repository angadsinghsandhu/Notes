# # Checking for a palindrome efficiently

# T.C. : O(n)
def isPalindrome(s):
    return s == s[::-1]

string = "madam"
print(isPalindrome(string))