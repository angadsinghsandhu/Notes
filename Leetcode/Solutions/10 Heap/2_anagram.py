# # checking if 2 words are anagrams of each other

from collections import Counter

# T.C. = O(nlogn)
# S.C. = O(n)
def isAnagram1(s1, s2):
    return sorted(s1) == sorted(s2)

# T.C. = O(n)
# S.C. = O(n)
def isAnagram2(s1, s2):
    return Counter(s1) == Counter(s2)
    

s1 = "SILENT"
s2 = "LISTEN"

print(isAnagram1(s1, s2))
print(isAnagram2(s1, s2))

