#include<iostream>
using namespace std;

#include <algorithm>

class Solution{
    public:
    // arr : given array
    // l : starting index of the array i.e 0
    // r : ending index of the array i.e size-1
    // k : find kth smallest element and return using this function
    
    int kthSmallest(int arr[], int l, int r, int k) {
        //code here
        // Sort the given array
        sort(arr, arr + r + 1);
     
        // Return k'th element in the sorted array
        return arr[k - 1];
    }
};


int main(){
    return 0;
}