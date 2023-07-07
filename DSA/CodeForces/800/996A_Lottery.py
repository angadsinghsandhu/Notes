# helper functions
def get_next_big(money, demo):
    return [v for i,v in enumerate(demo) if v <= money][-1]

# denomination
demo = [1, 5, 10, 20, 100]
min_notes = 0
money = int(input())

while money > 0:
    # get largest denomination that is 
    # smaller or equal to available money
    curr_demo = get_next_big(money, demo)
    q, r = divmod(money, curr_demo)
    min_notes += q
    money = r

print(min_notes)