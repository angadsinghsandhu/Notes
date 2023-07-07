#include<iostream>
using namespace std;

// Pair struct is used to return
// two values from getMinMax()
struct Pair
{
    int min;
    int max;
};

int getMax(int a, int b){
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

int getMin(int a, int b){
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

struct Pair getMinMax_divide(int arr[], int low, int high){
    
}

struct Pair getMinMax_linear( int arr[], int len ){
    // Complexity : Time [O(n)]
    struct Pair minmax;

    int i=0;

    // return if only on element
    if (len == 1){
        minmax.max = arr[0];
        minmax.min = arr[0];
        return minmax;
    }

    // for morethan 2 elements
    minmax.max = getMax(arr[0], arr[1]);
    minmax.min = getMin(arr[0], arr[1]);

    for(i = 2; i<len; i++){
        minmax.max = getMax(minmax.max, arr[i]);
        minmax.min = getMin(minmax.min, arr[i]);
    }

    return minmax;
}

int main(){
    int arr[5] = { 3, 5, 4, 1, 2 };

    int len = sizeof(arr)/sizeof(arr[0]);
    int max, min;

    struct Pair minmax = getMinMax(arr, len);

    cout << "Maximum is : " << minmax.max << endl;
    cout << "Minimum is : " << minmax.min << endl;

    return 0;
}

