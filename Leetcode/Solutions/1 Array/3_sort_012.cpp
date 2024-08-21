class Solution {
    public:
    void sort012(int a[], int n){

        int zeros = 0;
        int ones = 0;
        int twos = 0;
        
        for (int i = 0; i<n; i++) {
            if(a[i] == 0){
                zeros++;
            } else if (a[i] == 1){
                ones++;
            } else {
                twos++;
            }
        }
        
        int counter = 0;
        
        for(; zeros > 0; zeros--){
            a[counter++] = 0;
        }
        
        for(; ones > 0; ones--){
            a[counter++] = 1;
        }
        
        for(; twos > 0; twos--){
            a[counter++] = 2;
        }
        
        return; 

    }
};