// Given two strings s and t. Find the minimum number 
// of operations that need to be performed on str1 to convert 
// it to str2. The possible operations are:

// 1. Insert
// 2. Remove
// 3. Replace

// This is the Dynamic Programming solution for the edit distance problem.

#include <bits/stdc++.h>
using namespace std;
int minDis(string s1, string s2, int n, int m, vector<vector<int>> &dp){

// If any string is empty,
// return the remaining characters of other string
		
if(n==0) return m;
		
if(m==0) return n;
		
		
// To check if the recursive tree
// for given n & m has already been executed
		
if(dp[n][m]!=-1) return dp[n][m];
		
		
// If characters are equal, execute
// recursive function for n-1, m-1
		
if(s1[n-1]==s2[m-1]){		
	if(dp[n-1][m-1]==-1){			
	return dp[n][m] = minDis(s1, s2, n-1, m-1, dp);		
	}	
	else
	return dp[n][m] = dp[n-1][m-1];
}

		
// If characters are nt equal, we need to
		
// find the minimum cost out of all 3 operations.
		
else{		
	int m1, m2, m3;	 // temp variables
	
	if(dp[n-1][m]!=-1){
	m1 = dp[n-1][m];	
	}		
	else{
	m1 = minDis(s1, s2, n-1, m, dp);	
	}		
			
	if(dp[n][m-1]!=-1){			
	m2 = dp[n][m-1];		
	}		
	else{
	m2 = minDis(s1, s2, n, m-1, dp);	
	}								
	
	if(dp[n-1][m-1]!=-1){
	m3 = dp[n-1][m-1];	
	}
	else{
	m3 = minDis(s1, s2, n-1, m-1, dp);	
	}	
	return dp[n][m] = 1+min(m1, min(m2, m3));	
}

}


// Driver program
int main() {
	
string str1 = "voldemort";
string str2 = "dumbledore";
	
int n= str1.length(), m = str2.length();
vector<vector<int>> dp(n+1, vector<int>(m+1, -1));
				
cout<<minDis(str1, str2, n, m, dp);
return 0;
	
//	 This code is a contribution of Bhavneet Singh

}
