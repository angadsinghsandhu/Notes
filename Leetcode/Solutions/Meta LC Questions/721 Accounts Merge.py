# ACCOUNTS MERGE

# Problem number: 721
# Difficulty: Medium
# Tags: Graph, Union-Find, DFS
# Link: https://leetcode.com/problems/accounts-merge/

from typing import List
from collections import defaultdict

class Solution:
    """
    This problem involves merging accounts based on common emails.
    If two accounts share the same email, they belong to the same person.
    
    We can solve this problem using Union-Find (Disjoint Set Union) to group emails 
    belonging to the same person. Once we group the emails, we can reconstruct the accounts.
    
    The solution has two main steps:
    1. Union the emails based on accounts.
    2. Gather the emails for each component and sort them.
    """

    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """
        Union-Find approach to merge accounts.
        
        T.C. : O(n * log n) where n is the total number of emails
        S.C. : O(n) where n is the total number of unique emails
        """
        # Helper function to find the root of an email
        def find(email: str) -> str:
            if parent[email] != email:
                parent[email] = find(parent[email])
            return parent[email]
        
        # Helper function to union two emails
        def union(email1: str, email2: str):
            root1 = find(email1)
            root2 = find(email2)
            if root1 != root2:
                parent[root2] = root1

        parent = {}
        email_to_name = {}

        # Step 1: Union all emails in the same account
        for account in accounts:
            name = account[0]
            first_email = account[1]
            for email in account[1:]:
                if email not in parent:
                    parent[email] = email  # Each email is initially its own parent
                email_to_name[email] = name
                union(first_email, email)
        
        # Step 2: Group emails by their root parent
        emails_by_parent = defaultdict(list)
        for email in parent:
            root_email = find(email)
            emails_by_parent[root_email].append(email)

        # Step 3: Reconstruct the merged account with name and sorted emails
        merged_accounts = []
        for root_email, emails in emails_by_parent.items():
            merged_accounts.append([email_to_name[root_email]] + sorted(emails))

        return merged_accounts

# Best Method: Union-Find is the most optimal approach here as it efficiently merges accounts and resolves shared emails.

# Sample Inputs for Testing
accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
solution = Solution()
output = solution.accountsMerge(accounts)

print(output)  # Expected output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"], ["Mary","mary@mail.com"], ["John","johnnybravo@mail.com"]]
