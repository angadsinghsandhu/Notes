#include <iostream>
#include <bits/stdc++.h>

using namespace std;

void show2d(vector<vector<int>> arr){
    for(auto i:arr){
        for(auto j:i)
            cout << j << " ";
        cout << endl;
    }
    cout << endl;
    return;
}

void show(vector<int> arr){
    for(auto i:arr)
        cout << i << " ";
    cout << "\n";
    return;
}

void knapsack(vector<int> wt, vector<int> val, int W){
    
    vector<vector<int>> dp(val.size()+1, vector<int>(W+1));
    
    show2d(dp);
    
    for(int i=0; i<dp[0].size(); i++)
        // setting first row to 0
        dp[0][i] = 0;
        
    // show2d(dp);
    
    for(int i=0; i<dp.size(); i++)
        // setting first column to 1
        dp[i][0] = 1;
        
    show2d(dp);
    
    for(int i=1; i<(int) dp.size(); i++){
        for(int j=0; j<dp[0].size(); j++){
            if(j-val[i-1]>=0)
                dp[i][j] = dp[i-1][j] + dp[i-1][j-val[i-1]];
            else
                dp[i][j] = dp[i-1][j];
                
            show2d(dp);
        }
    }
    
    cout << dp[val.size()][W];
    
}

int knapsack_mem(vector<int> wt, vector<int> val, int W, vector<vector<int>> dp, int n){
    // Base case
    if (n==0 or W==0)
        return 0;
    
    // array check for repetition
    if(dp[n][W] != -1)
        return dp[n][W];
        
    if(W-wt[n-1]<0){
        dp[n][W] = knapsack_mem(wt, val, W, dp, n-1);
        return dp[n][W];
    } else {
        int weight = wt[n-1];
        int value = val[n-1];
        
        dp[n][W] = max(value + knapsack_mem(wt, val, W-weight, dp, n-1), knapsack_mem(wt, val, W, dp, n-1));
        return dp[n][W];
    }
}

int knapsack_rec(vector<int> wt, vector<int> val, int W){
    // base case
    if(wt.empty() or W==0)
        return 0;
        
    if(W-*wt.end()<0){
        int value = val.back();
        int weight = wt.back();
        val.pop_back();
        wt.pop_back();
        return knapsack_rec(wt, val, W);
    } else {
        // reducing the input to check if it is the best output
        int value = val.back();
        int weight = wt.back();
        val.pop_back();
        wt.pop_back();
        return max(value + knapsack_rec(wt, val, W-weight), knapsack_rec(wt, val, W));
    }
}

int main()
{
    vector<int> wt = {3, 4, 5, 6, 10};
    vector<int> val = {5, 2, 11, 6, 9};
    int W = 11;
    
    // int ans = knapsack_rec(wt, val, W);
    
    // vector<vector<int>> dp(val.size()+1, vector<int>(W+1, -1));
    // int ans = knapsack_mem(wt, val, W, dp, val.size());
    
    // cout << "answer : " << ans;
    
    knapsack(wt, val, W);

    return 0;
}
