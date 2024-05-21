#include <bits/stdc++.h>
using namespace std;

class Solution{
    void swap(int arr[], int left, int right) {
        int temp = arr[left];
        arr[left] = arr[right];
        arr[right] = temp;
    }
    
    int getPos(int arr[], int len, int start){
        for(int i=start; i<len; i++){
            if(arr[i]>=0){
                return i;
            }
        }
    }
    
    public:
    int* NegSort(int a[], int n){
        int l= 0;
        l = getPos(a, n, l);
        
        for (int i=l+1; i<n && l<n; i++){
            if (a[i] < 0){
                swap(a, l, i);
                l++;
            }
        }
        
        return a;
    }
};

struct Pair{
    int min;
    int max;
};

int main() {
    
    int len = 5;
    int a[5] = {1, -2, 3, -4, -5};
    int* b;
    
    Solution ob;
    b = ob.NegSort(a, len);
	//code
	
	for(int i=0; i<len; i++){
	    cout << b[i] << " " << endl;
	}
	return 0;
}