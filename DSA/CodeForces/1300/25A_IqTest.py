size = int(input())
nums = list(map(int, input().split()))

even_func = lambda x: 1 if x%2 == 0 else 0
even_lst = list(map(even_func, nums))

if even_lst.count(1) == 1:
    print(even_lst.index(1)+1)
else:
    print(even_lst.index(0)+1)