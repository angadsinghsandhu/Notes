#include <bits/stdc++.h>
using namespace std;

class Solution{
    public:     
    // nums[] represents lengths of different words in input sequence.
    // For example, nums[] = {3, 2, 2, 5} is for a sentence like
    // "aaa bb cc ddddd". n is size of nums[] and k is line width
    // (maximum no. of characters that can fit in a line)
    int solveWordWrap (vector<int>nums, int k)
    {
        int n = nums.size();
        // For simplicity, 1 extra space is used in all below arrays
     
        // extras[i][j] will have number of extra spaces if words from i
        // to j are put in a single line
        int extras[n+1][n+1];
        
        // filling 'extras with zeros'
        for(int i=0; i<n+1; i++)
            for(int j=0; j<n+1; j++)
                extras[i][j] = 0;
     
        // lc[i][j] will have cost of a line which has words from
        // i to j
        int lc[n+1][n+1];
        
        // filling 'lc with zeros'
        for(int i=0; i<n+1; i++)
            for(int j=0; j<n+1; j++)
                lc[i][j] = 0;
     
        // c[i] will have total cost of optimal arrangement of words
        // from 1 to i
        int c[n+1];
     
        int i, j;
     
        // calculate extra spaces in a single line. The value extra[i][j]
        // indicates extra spaces if words from word number i to j are
        // placed in a single line
        for (i = 1; i <= n; i++)
        {
            extras[i][i] = k - nums[i-1];
            for (j = i+1; j <= n; j++)
                extras[i][j] = extras[i][j-1] - nums[j-1] - 1;
        }
        
        // cout << "printing 'extras' : " << endl;
        // for(int i=0; i<n+1; i++){
        //     for(int j=0; j<n+1; j++)
        //         cout << extras[i][j] << " ";
        //     cout << endl;
        // }
        // cout << endl;
     
        // Calculate line cost corresponding to the above calculated extra
        // spaces. The value lc[i][j] indicates cost of putting words from
        // word number i to j in a single line
        for (i = 1; i <= n; i++)
        {
            for (j = i; j <= n; j++)
            {
                if (extras[i][j] < 0)
                    lc[i][j] = INF;
                else if (j == n && extras[i][j] >= 0)
                    lc[i][j] = 0;
                else
                    lc[i][j] = extras[i][j]*extras[i][j];
            }
        }
        
        // cout << "printing 'loss matrix' : " << endl;
        // for(int i=0; i<n+1; i++){
        //     for(int j=0; j<n+1; j++)
        //         cout << lc[i][j] << " ";
        //     cout << endl;
        // }
        // cout << endl;
     
        // Calculate minimum cost and find minimum cost arrangement.
        // The value c[j] indicates optimized cost to arrange words
        // from word number 1 to j.
        c[0] = 0;
        for (j = 1; j <= n; j++)
        {
            c[j] = INF;
            for (i = 1; i <= j; i++)
            { 
                if (c[i-1] != INF && lc[i][j] != INF && (c[i-1] + lc[i][j] < c[j]))
                {
                    c[j] = c[i-1] + lc[i][j];
                }
            }
        }
        
        // cout << "printing 'loss array' : ";
        // for(int i=0; i<n+1; i++){
        //     cout << c[i] << " ";
        // }
        // cout << endl;
     
        return c[n];
    }
}