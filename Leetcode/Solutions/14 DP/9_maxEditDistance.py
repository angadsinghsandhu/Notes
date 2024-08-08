# Edit Maximum Distance

# given two words w1 and w2, find the minimum number 
# of operations required to convert w1 to w2

# # character operations permitted
# - Insert
# - Delete
# - Replce

# # example 1 input
# house values
# horse ros

# # example 1 output
# 3
# order : replace 'h' with 'r', remove 'r', remove 'e'

# T.C. : O(n^2)
# S.C. : O(n^2)
def dynamic(w1, w2):
    r, c = len(w1), len(w2)
    
    dp = [ [0]*(c+1) for i in range(r+1) ]
    # print(dp)

    for i in range(r+1):
        for j in range(c+1):
            # for w1 being empty we insert all words of w2
            if i==0:
                dp[i][j] = j
            # for w2 being empty we delete all words of w1
            elif j==0:
                dp[i][j] = i
            # if both charates are smae then ignore
            elif w1[i-1] == w2[j-1]:
                dp[i][j] = dp[i-1][j-1]
                continue
            # performing insert, delete, relpace
            else:
                # dp[i][j-1] is insert
                # dp[i-1][j] is deletw
                # dp[i-1][j-1] is replace
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1]) 

    return dp[r][c]
            

w1, w2 = map(str, input("Enter Words : ").split())

print("Edit Distance is : {}".format(dynamic(w1, w2)))