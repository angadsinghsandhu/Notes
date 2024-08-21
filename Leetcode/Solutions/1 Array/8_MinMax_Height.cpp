#include <bits/stdc++.h>
using namespace std;

class Solution {
    public:
    int getMinDiff(int arr[], int n, int k) {
        sort(arr, arr + n); // sort the array to get the
                            // corner cases ans.
                            
        // between elements max and min value 
        // these 2 variables will hold the value 
        int minEle, maxEle;
        
        // current result when arr[0]
        // iss min and arr[n-1] is max
        int result = arr[n - 1] - arr[0]; 
 
        for (int i = 1; i < n; i++) {
            // cout << "Max Element : " << maxEle << endl;
            if (arr[i] >= k && arr[n - 1] >= k) {
                // if the middle elements max and min
                maxEle = max(arr[i - 1] + k, arr[n - 1] - k);
               
                // difference if less than result then update
                minEle = min(arr[0] + k, arr[i] - k);
                
                // result.
                result = min(result, maxEle - minEle);
            }
        }
        
        return result; // return result.
    }
}

void main(){

}
