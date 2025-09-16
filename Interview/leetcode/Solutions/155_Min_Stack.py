# File: Leetcode/Solutions/155_Min_Stack.py

"""
Problem Number: 155
Problem Name: Min Stack
Difficulty: Medium
Tags: Stack, Design, Neetcode 150
Company (Frequency): Amazon, Bloomberg, Google, Facebook, Microsoft
Leetcode Link: https://leetcode.com/problems/min-stack/description/

DESCRIPTION

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the `MinStack` class:

- `MinStack()` initializes the stack object.
- `void push(int val)` pushes the element `val` onto the stack.
- `void pop()` removes the element on the top of the stack.
- `int top()` gets the top element of the stack.
- `int getMin()` retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

---

#### Example 1:
**Input:**
```plaintext
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]
```

**Output:**
```plaintext
[null,null,null,null,-3,null,0,-2]
```

**Explanation:**  
- MinStack minStack = new MinStack();
- minStack.push(-2);
- minStack.push(0);
- minStack.push(-3);
- minStack.getMin(); // return -3
- minStack.pop();
- minStack.top();    // return 0
- minStack.getMin(); // return -2

#### Constraints:
- `-2^31 <= val <= 2^31 - 1`
- Methods `pop`, `top`, and `getMin` operations will always be called on non-empty stacks.
- At most `3 * 10^4` calls will be made to `push`, `pop`, `top`, and `getMin`.
"""

class MinStack:
    """
    Thought Process:
    - The problem involves designing a stack that supports standard operations (push, pop, top) and also retrieves the minimum element in constant time.
    - A brute-force approach would involve scanning the stack to find the minimum, but this is inefficient.
    - An optimized approach uses an auxiliary stack to track the minimum element at each step.

    Input:
        None - The class is initialized without any input.

    Output:
        None - The class provides methods to interact with the stack.
    """

    def __init__(self):
        """
        Approach:
        - Initialize two stacks: one for storing the actual elements (`stack`) and another for tracking the minimum elements (`min_stack`).
        - Use `min_stack` to keep track of the minimum element at each step.

        T.C.: O(1) - Initialization is constant time.
        S.C.: O(1) - No additional space used during initialization.
        """
        self.stack = []  # Main stack to store elements
        self.min_stack = []  # Auxiliary stack to store minimum elements

    def push(self, val: int) -> None:
        """
        Approach:
        - Push the value onto the main stack.
        - Update the `min_stack` with the current minimum value (either the new value or the existing minimum).

        T.C.: O(1) - Appending to a list is constant time.
        S.C.: O(1) - No additional space used.
        """
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        """
        Approach:
        - Pop the top element from the main stack.
        - If the popped element is the current minimum, also pop it from the `min_stack`.

        T.C.: O(1) - Popping from a list is constant time.
        S.C.: O(1) - No additional space used.
        """
        if self.stack:
            popped = self.stack.pop()
            if popped == self.min_stack[-1]:
                self.min_stack.pop()

    def top(self) -> int:
        """
        Approach:
        - Return the top element of the main stack.

        T.C.: O(1) - Accessing the last element of a list is constant time.
        S.C.: O(1) - No additional space used.
        """
        if not self.stack:
            raise IndexError("top() called on empty stack")
        return self.stack[-1]

    def getMin(self) -> int:
        """
        Approach:
        - Return the top element of the `min_stack`, which is the current minimum.

        T.C.: O(1) - Accessing the last element of a list is constant time.
        S.C.: O(1) - No additional space used.
        """
        if not self.min_stack:
            raise IndexError("getMin() called on empty stack")
        return self.min_stack[-1]

# Run and print sample test cases
if __name__ == "__main__":
    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    print(min_stack.getMin())  # Output: -3
    min_stack.pop()
    print(min_stack.top())     # Output: 0
    print(min_stack.getMin())  # Output: -2
