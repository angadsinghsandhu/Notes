# https://codeforces.com/problemset/problem/71/A

def abbvr(word):
    size = len(word)

    if size <= 10:
        return word
    else:
        return str(word[0] + str(size-2) + word[-1])

n = int(input())

for i in range(n):
    word = str(input())
    print(abbvr(word))