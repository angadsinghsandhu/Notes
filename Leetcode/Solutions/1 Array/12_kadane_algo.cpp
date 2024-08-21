#include <bits/stdc++.h>
using namespace std;

// same as Q7
// Kadane's Algorithm : Given an array arr of N integers. Find the contiguous sub-array with maximum sum.

class Solution{    
    public:
    public:
    // arr: input array
    // n: size of array
    //Function to find the sum of contiguous subarray with maximum sum.
    int maxSubarraySum(int arr[], int n){
        
        // Your code here
        int max = arr[0];
        int max_curr = 0;
        
        for(int i=0; i<n; i++){
            max_curr = std::max(arr[i], arr[i] + max_curr);
            
            
            if(max_curr > max){
                max = max_curr;
            }
        
            if(max_curr < 0){
                max_curr = 0;
            }
        }
        
        return max;
        
    }
};