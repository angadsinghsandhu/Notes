# # Frequency Sort

# T.C. = O(nlogn)
from collections import Counter

def freqSort(txt):
    ct = Counter(txt)
    arr = list(ct.items())
    arr.sort(key=lambda x: [x[1], x[0]], reverse=True)
    arr = list(map(lambda x: x[0], arr))

    return arr

text = "Hello World welcome me to this plane were I now reside temporarily"
text = text.replace(" ", "")

print(freqSort(text))
