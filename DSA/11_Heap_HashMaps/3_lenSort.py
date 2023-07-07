# # Sorting by length (in Descending orer)

# T.C. = O(nlogn)
def strSort(txt):
    arr = txt.split()
    arr.sort(key=len, reverse=True)

    for i in arr : print(i, end=" ")
    print()


txt = "Hello World welcome me to this plane were I now reside temporarily"
strSort(txt)

