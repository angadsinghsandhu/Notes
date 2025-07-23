# Guide to Essential Data Structures in Python for Competitive Programming

Below is an extended guide that includes explanations of when to use each structure, key patterns that indicate their use, and the types of LeetCode problems where they are often employed.

## 1. Arrays (Lists in Python)

- **Description:**  
  Arrays, known as lists in Python, are ordered collections of elements that are mutable and can contain heterogeneous items. They are dynamic in size, allowing for the addition and removal of elements. Arrays store elements in contiguous memory locations, enabling efficient access and manipulation. Python lists provide O(1) time complexity for accessing elements by index but have O(n) complexity for insertion and deletion operations, especially in the middle of the list.

- **When to Use:**  
  Use arrays (lists) when:
  - You need to maintain an ordered collection of elements.
  - Random access to elements by index is required.
  - The size of the collection can change dynamically.
  - You need to perform operations like slicing, concatenation, or iteration efficiently.

- **Key Patterns:**
  - **Sliding Window:** Maintaining a subset of elements within a moving window.
  - **Prefix Sums:** Precomputing cumulative sums for range queries.
  - **Dynamic Programming:** Storing intermediate results in a linear fashion.
  - **Two-Pointer Techniques:** Using indices to traverse the array from both ends.
  - **Subarrays and Subsequences:** Identifying or manipulating contiguous or non-contiguous segments.

- **LeetCode Problem Types:**
  - **Sliding Window Maximum (Problem #239)**
  - **Two Sum (Problem #1)**
  - **Best Time to Buy and Sell Stock (Problem #121)**
  - **Maximum Subarray (Problem #53)**
  - **Product of Array Except Self (Problem #238)**
  - **Rotate Array (Problem #189)**

- **Python Implementation:**

  ```python
  # Example 1: Basic Array Operations
  arr = [1, 2, 3]
  arr.append(4)        # Append
  arr.pop()            # Pop
  print(arr[1])        # Access element at index 1
  arr.insert(1, 5)     # Insert 5 at index 1
  arr.remove(2)        # Remove first occurrence of element 2
  print(arr.index(3))  # Find index of element 3
  new_arr = arr.copy() # Copy array
  arr.reverse()        # Reverse array
  print(arr)
  # Output:
  # 2
  # 1
  # [5, 1, 3]
  
  # Example 2: Slicing and Concatenation
  list1 = [1, 2, 3]
  list2 = [4, 5, 6]
  combined = list1 + list2  # Concatenate lists
  print(combined)
  # Output: [1, 2, 3, 4, 5, 6]
  
  sliced = combined[2:5]     # Slice from index 2 to 4
  print(sliced)
  # Output: [3, 4, 5]
  
  # Example 3: Iteration
  for element in combined:
      print(element, end=" ")
  # Output: 1 2 3 4 5 6
  
  # Example 4: List Comprehensions
  squares = [x**2 for x in range(5)]
  print(squares)
  # Output: [0, 1, 4, 9, 16]
  
  # Example 5: Nested Lists
  matrix = [
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9]
  ]
  print(matrix[1][2])  # Access element in second row, third column
  # Output: 6
  ```

- **Time Complexity:**
  
  - **Access:** O(1)
  - **Append:** O(1) amortized
  - **Pop:** O(1) from the end, O(n) from the middle
  - **Insert:** O(n)
  - **Remove:** O(n)
  - **Copy:** O(n)
  - **Reverse:** O(n)
  - **Slicing:** O(k) where k is the size of the slice

- **Space Complexity:**  
  O(n), where n is the number of elements in the array.

- **Additional Notes:**
  
  - **Dynamic Sizing:** Unlike static arrays in languages like C or Java, Python lists can grow and shrink dynamically, providing greater flexibility.
  
  - **Heterogeneous Elements:** Python lists can store elements of different data types, including other lists, which allows for the creation of complex data structures like matrices.
  
  - **Memory Overhead:** Python lists have additional memory overhead compared to lower-level array implementations due to their dynamic nature and ability to store heterogeneous data.

- **Best Practices:**
  
  - **Use List Comprehensions:** They provide a concise and efficient way to create lists.
  
  - **Avoid Frequent Insertions/Deletions in the Middle:** Since these operations are O(n), they can lead to performance bottlenecks in large lists.
  
  - **Use Slicing Carefully:** Slicing creates a new list, which can consume additional memory if overused on large lists.
  
  - **Leverage Built-in Methods:** Utilize Python's built-in list methods for optimal performance and readability.

- **Example: Finding Two Numbers that Add Up to a Target (Two Sum)**

  ```python
  def two_sum(nums, target):
      num_map = {}
      for i, num in enumerate(nums):
          complement = target - num
          if complement in num_map:
              return [num_map[complement], i]
          num_map[num] = i
      return []

  # Usage
  nums = [2, 7, 11, 15]
  target = 9
  print(two_sum(nums, target))  # Output: [0, 1]
  ```

  **Explanation:**  
  This function iterates through the list `nums`, and for each element, it checks if the complement (i.e., `target - num`) exists in the `num_map`. If it does, it returns the indices of the two numbers that add up to the target. Otherwise, it adds the current number and its index to the `num_map`. This approach ensures O(n) time complexity.

## 2. Sorting

- **Description:**  
  Sorting is a fundamental operation that arranges elements in a particular order, typically in ascending or descending order. In Python, the `sort()` method is used to sort lists in place, modifying the original list, while the `sorted()` function returns a new sorted list from any iterable without altering the original. Python's sorting capabilities are versatile, allowing sorting of integers, floating-point numbers, strings, tuples, and even complex data structures with custom sorting criteria using the `key` parameter. The underlying time complexity of Python's sorting algorithms is generally **O(n log n)**.

- **When to Use:**  
  Use sorting when you need to:
  - Arrange data in a specific order (e.g., numerical, lexicographical).
  - Simplify the problem by ordering elements, making it easier to apply other algorithms (like binary search).
  - Eliminate duplicates or identify unique elements.
  - Optimize algorithms that benefit from sorted data, such as greedy algorithms.

- **Key Patterns:**
  - **Ordered Data Requirements:** Problems that require data to be in a specific order to simplify processing.
  - **Greedy Algorithms:** Many greedy strategies depend on processing elements in a sorted order.
  - **Two-Pointer Techniques:** Sorting can facilitate the use of two-pointer approaches for efficient solutions.
  - **Finding K-th Elements:** Identifying the k-th largest or smallest elements often involves sorting.
  - **Eliminating Duplicates:** Sorting can help in removing or counting duplicates efficiently.
  - **Interval Problems:** Sorting intervals by start or end times to merge or allocate resources.

- **LeetCode Problem Types:**
  - **Two Sum (Problem #1):** Can be optimized using sorting and the two-pointer technique.
  - **3Sum (Problem #15):** Requires sorting to efficiently find triplets that sum to zero.
  - **Kth Largest Element in an Array (Problem #215):** Involves sorting to identify the k-th largest element.
  - **Merge Intervals (Problem #56):** Requires sorting intervals to merge overlapping ones.
  - **Meeting Rooms II (Problem #253):** Involves sorting start and end times to determine the number of rooms needed.
  - **Find the Duplicate Number (Problem #287):** Sorting can help identify duplicates efficiently.

- **Python Implementation:**

  ```python
  # Example 1: Basic Sorting in Ascending Order
  numbers = [3, 1, 4, 1, 5, 9]
  numbers.sort()
  print("Sorted in Ascending Order:", numbers)
  # Output: [1, 1, 3, 4, 5, 9]

  # Example 2: Sorting in Descending Order
  numbers = [3, 1, 4, 1, 5, 9]
  numbers.sort(reverse=True)
  print("Sorted in Descending Order:", numbers)
  # Output: [9, 5, 4, 3, 1, 1]

  # Example 3: Sorting with a Custom Key Function
  # Sorting a list of tuples by the second element
  list_of_tuples = [(1, 3), (2, 1), (4, 2)]
  list_of_tuples.sort(key=lambda x: x[1])
  print("Sorted by Second Element:", list_of_tuples)
  # Output: [(2, 1), (4, 2), (1, 3)]

  # Example 4: Sorting Strings by Length
  words = ["banana", "apple", "cherry", "date"]
  words.sort(key=len)
  print("Sorted by Length:", words)
  # Output: ['date', 'apple', 'banana', 'cherry']

  # Example 5: Using sorted() to Return a New Sorted List
  original_list = [3, 1, 4, 1, 5, 9]
  sorted_list = sorted(original_list)
  print("Original List:", original_list)
  print("Sorted List:", sorted_list)
  # Output:
  # Original List: [3, 1, 4, 1, 5, 9]
  # Sorted List: [1, 1, 3, 4, 5, 9]

  # Example 6: Sorting a List of Dictionaries by a Specific Key
  students = [
      {"name": "Alice", "age": 25},
      {"name": "Bob", "age": 30},
      {"name": "Charlie", "age": 22},
      {"name": "David", "age": 28},
  ]
  students.sort(key=lambda x: x["age"])
  print("Students Sorted by Age:", students)
  # Output:
  # [
  #     {'name': 'Charlie', 'age': 22},
  #     {'name': 'Alice', 'age': 25},
  #     {'name': 'David', 'age': 28},
  #     {'name': 'Bob', 'age': 30}
  # ]
  ```

- **Time Complexity:**
  
  - **Sort Method (`list.sort()`):**  
    - **Best Case:** O(n) when the list is already sorted.
    - **Average and Worst Case:** O(n log n) due to the underlying Timsort algorithm.
  
  - **Sorted Function (`sorted()`):**  
    - **Best Case:** O(n) when the iterable is already sorted.
    - **Average and Worst Case:** O(n log n).

- **Space Complexity:**  
  - **Sort Method (`list.sort()`):**  
    - **Space Complexity:** O(n) due to the Timsort algorithm's temporary storage.
  
  - **Sorted Function (`sorted()`):**  
    - **Space Complexity:** O(n) for creating a new sorted list.

- **Additional Notes:**
  
  - **`sort()` vs `sorted()`:**
    - `sort()` is a list method that sorts the list in place and returns `None`. It may not be stable.
    - `sorted()` is a built-in function that returns a new sorted list from any iterable without modifying the original. It is stable.
  
  - **Custom Sorting:**  
    Leveraging the `key` parameter allows for sophisticated sorting criteria, enabling sorting based on multiple attributes or complex rules.
  
  - **Stable Sorting:**  
    Python's sorting algorithms are stable, meaning that elements with equal keys maintain their original order relative to each other.

- **Best Practices:**
  
  - **Use `sort()` When:**
    - You need to sort a list in place and do not require the original order.
    - Memory usage is a concern, as `sort()` does not create a new list.
  
  - **Use `sorted()` When:**
    - You need to maintain the original iterable without modification.
    - Sorting iterables other than lists, such as tuples or dictionaries.
  
  - **Leverage the `key` Parameter:**
    - For complex sorting criteria, such as sorting objects based on multiple attributes or nested data structures.
    - To improve code readability and efficiency by encapsulating the sorting logic within the `key` function.
  
  - **Combine with Other Algorithms:**
    - Use sorting as a preliminary step to simplify problems, making it easier to apply algorithms like binary search or two-pointers.

## 3. Itertools

- **Description:**  
  The `itertools` module in Python provides a collection of functions for creating iterators to generate combinations, permutations, and other operations on iterable data structures. These functions are highly efficient and memory-friendly, allowing for the generation of complex sequences without storing them in memory. Common functions include `product()`, `permutations()`, `combinations()`, and `groupby()`, among others. By leveraging `itertools`, you can efficiently solve problems that involve generating or processing combinations, permutations, and subsequences.

### 3.1 Combinations

- **When to Use:** 
  Use combinations when you need to:
  - Generate all possible subsets of a specific size from a given set of elements.
  - Enumerate all distinct ways to select a subset of elements without repetition.
  - Solve problems that involve selecting a subset of elements that satisfy specific conditions.

- **Key Patterns:**
  - **Subset Generation:** Enumerating all possible subsets of a given size.
  - **Combination Sum Problems:** Finding combinations that sum to a target value.
  - **Unique Combinations:** Generating distinct subsets without repetition.
  - **Subset Sum Problems:** Identifying subsets that satisfy specific conditions.
  - **Combinatorial Problems:** Solving problems that involve selecting elements from a set.

- **LeetCode Problem Types:**
  - **Combination Sum (Problem #39):** Involves finding all unique combinations that sum to a target value.
  - **Subsets (Problem #78):** Requires generating all possible subsets of a given set of elements.
  - **Letter Combinations of a Phone Number (Problem #17):** Involves generating all possible letter combinations based on a phone number.
  - **Combination Sum II (Problem #40):** Requires finding unique combinations that sum to a target value.
  - **Subsets II (Problem #90):** Involves generating unique subsets without repetition.

- **Python Implementation:**

  ```python
  from itertools import combinations

  # Example 1: Generating Combinations of a List
  nums = [1, 2, 3]
  for r in range(1, len(nums) + 1):
      print(list(combinations(nums, r)))

  # Output:
  # [(1,), (2,), (3,)]
  # [(1, 2), (1, 3), (2, 3)]
  # [(1, 2, 3)]

  # Example 2: Using Combinations to Solve a Problem
  def combination_sum(nums, target):
      result = []
      for r in range(1, len(nums) + 1):
          for combination in combinations(nums, r):
              if sum(combination) == target:
                  result.append(combination)
      return result

  # Usage
  nums = [2, 3, 6, 7]
  target = 7

  print(combination_sum(nums, target))

  # Output: [(7,), (2, 2, 3)]
  ```

- **Time Complexity:**
  - **Generation of Combinations:** O(2^n) for generating all possible subsets of size n.
  - **Checking Combinations:** O(n) for checking the sum of each combination.

- **Space Complexity:**
  - **Generation of Combinations:** O(2^n) for storing all possible subsets of size n.
  - **Checking Combinations:** O(n) for storing the current combination.

- **Additional Notes:**
  - **Memory Efficiency:** `itertools` functions are memory-efficient as they generate elements on the fly without storing them in memory.
  - **Combinatorial Problems:** Problems involving combinations often require a brute-force approach to generate all possible subsets efficiently.
  - **Optimization Techniques:** For large input sizes, consider optimizing the solution to avoid generating all possible combinations.

- **Best Practices:**
  - **Use Itertools for Combinatorial Problems:** Leverage `itertools` functions for generating combinations, permutations, and subsequences efficiently.
  - **Optimize for Large Inputs:** For problems with large input sizes, consider optimizing the solution to avoid generating all possible combinations.
  - **Combine with Other Techniques:** Integrate `itertools` functions with other algorithms to solve complex combinatorial problems effectively.

### 3.2 Combinations with Replacement

- **When to Use:**  
  Use combinations with replacement when you need to:
  - Generate all possible combinations of a specific size from a given set of elements, allowing for repetition.
  - Enumerate all distinct ways to select a subset of elements with the possibility of repetition.
  - Solve problems that involve selecting elements with replacement to satisfy specific conditions.

- **Key Patterns:**
  - **Combination Generation with Repetition:** Enumerating all possible combinations with the option of selecting the same element multiple times.
  - **Repetitive Selections:** Solving problems that involve selecting elements with replacement to achieve a specific target.
  - **Permutations with Duplicates:** Generating permutations of elements with duplicates or repetitions.
  - **Combinatorial Problems with Multiplicity:** Addressing problems that require selecting elements with varying frequencies.

- **LeetCode Problem Types:**
  - **Combination Sum IV (Problem #377):** Involves finding the number of combinations that sum to a target value with repetitions allowed.
  - **Subsets II (Problem #90):** Requires generating unique subsets with the possibility of duplicates.
  - **Letter Combinations of a Phone Number (Problem #17):** Involves generating all possible letter combinations based on a phone number with repetitions allowed.
  - **Combination Sum III (Problem #216):** Requires finding unique combinations that sum to a target value with a specific number of elements.

- **Python Implementation:**

  ```python
  from itertools import combinations_with_replacement

  # Example 1: Generating Combinations with Replacement
  nums = [1, 2, 3]
  for r in range(1, len(nums) + 1):
      print(list(combinations_with_replacement(nums, r)))

  # Output:
  # [(1,), (2,), (3,)]
  # [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
  # [(1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 2, 2), (1, 2, 3), (1, 3, 3), (2, 2, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3)]

  # Example 2: Using Combinations with Replacement to Solve a Problem
  def combination_sum_with_replacement(nums, target):
      result = []
      for r in range(1, len(nums) + 1):
          for combination in combinations_with_replacement(nums, r):
              if sum(combination) == target:
                  result.append(combination)
      return result

  # Usage
  nums = [2, 3, 6, 7]

  print(combination_sum_with_replacement(nums, 7))

  # Output: [(7,), (2, 2, 3)]
  ```

- **Time Complexity:**
  - **Generation of Combinations:** O((n + r - 1) choose r) for generating all possible combinations with replacement.
  - **Checking Combinations:** O(n) for checking the sum of each combination.

- **Space Complexity:**
  - **Generation of Combinations:** O((n + r - 1) choose r) for storing all possible combinations with replacement.
  - **Checking Combinations:** O(n) for storing the current combination.

- **Additional Notes:**
  - **Repetitive Selections:** Combinations with replacement allow for selecting the same element multiple times in a combination.
  - **Combinatorial Problems with Multiplicity:** Problems involving selecting elements with varying frequencies can be efficiently solved using combinations with replacement.
  - **Optimization Techniques:** For large input sizes, consider optimizing the solution to avoid generating all possible combinations with replacement.

- **Best Practices:**
  - **Use Itertools for Combinatorial Problems:** Leverage `itertools` functions for generating combinations with replacement efficiently.
  - **Optimize for Large Inputs:** For problems with large input sizes, consider optimizing the solution to avoid generating all possible combinations with replacement.
  - **Combine with Other Techniques:** Integrate `itertools` functions with other algorithms to solve complex combinatorial problems effectively.

### 3.3 Permutations

- **When to Use:**  
  Use permutations when you need to:
  - Generate all possible arrangements of a specific size from a given set of elements.
  - Enumerate all distinct ways to order a subset of elements without repetition.
  - Solve problems that involve arranging elements in different orders to satisfy specific conditions.

- **Key Patterns:**
  - **Permutation Generation:** Enumerating all possible arrangements of elements.
  - **Ordering Problems:** Solving problems that involve ordering elements in distinct ways.
  - **Unique Arrangements:** Generating permutations without repetition.
  - **String Permutations:** Finding all possible arrangements of characters in a string.
  - **Combinatorial Problems with Ordering:** Addressing problems that require ordering elements in different ways.

- **LeetCode Problem Types:**
  - **Permutations (Problem #46):** Involves finding all possible permutations of a set of distinct integers.
  - **Next Permutation (Problem #31):** Requires generating the lexicographically next greater permutation of a sequence.
  - **Permutations II (Problem #47):** Involves finding unique permutations of a set of integers with duplicates.
  - **String Permutations:** Problems that involve generating all possible arrangements of characters in a string.
  - **Combinatorial Problems with Ordering:** Problems that require ordering elements in different ways to achieve specific outcomes.

- **Python Implementation:**

  ```python
  from itertools import permutations

  # Example 1: Generating Permutations of a List
  nums = [1, 2, 3]
  for r in range(1, len(nums) + 1):
      print(list(permutations(nums, r)))

  # Output:
  # [(1,), (2,), (3,)]
  # [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
  # [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

  # Example 2: Using Permutations to Solve a Problem
  def permute(nums):
      return list(permutations(nums))

  # Usage
  nums = [1, 2, 3]
  print(permute(nums))

  # Output: [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
  ```

- **Time Complexity:**
  - **Generation of Permutations:** O(n!) for generating all possible permutations of size n.
  - **Checking Permutations:** O(n) for checking each permutation.

- **Space Complexity:**
  - **Generation of Permutations:** O(n!) for storing all possible permutations of size n.
  - **Checking Permutations:** O(n) for storing the current permutation.

- **Additional Notes:**
  - **Unique Arrangements:** Permutations generate all possible unique arrangements of elements without repetition.
  - **Ordering Problems:** Problems involving ordering elements in different ways can be efficiently solved using permutations.
  - **Optimization Techniques:** For large input sizes, consider optimizing the solution to avoid generating all possible permutations.

- **Best Practices:**
  - **Use Itertools for Combinatorial Problems:** Leverage `itertools` functions for generating permutations efficiently.
  - **Optimize for Large Inputs:** For problems with large input sizes, consider optimizing the solution to avoid generating all possible permutations.
  - **Combine with Other Techniques:** Integrate `itertools` functions with other algorithms to solve complex combinatorial problems effectively.

## 3. Dict

### 3.1 Hash Tables (Dictionaries in Python)

- **Description:**  
  A hash table is a data structure that provides efficient lookup, insertion, and deletion operations by mapping keys to values. In Python, dictionaries (`dict`) serve as the primary implementation of hash tables. They store key-value pairs, where keys must be hashable (immutable and unique), and values can be of any data type. Hash tables achieve average-case time complexity of O(1) for insertions, lookups, and deletions, making them highly efficient for various applications.

- **When to Use:**  
  Use hash tables when:
  - You need fast access to data via unique keys.
  - Implementing mappings between keys and values, such as dictionaries or caches.
  - Counting frequencies or aggregating data based on unique identifiers.
  - Performing lookups, insertions, and deletions efficiently.

- **Key Patterns:**
  - **Frequency Counting:** Tallying occurrences of elements.
  - **Caching:** Storing computed results for quick retrieval.
  - **Grouping:** Categorizing items based on a common key.
  - **Index Mapping:** Creating a reverse index from values to keys.
  - **Dynamic Programming:** Storing intermediate results with unique keys.

- **LeetCode Problem Types:**
  - **Two Sum (Problem #1)**
  - **Longest Substring Without Repeating Characters (Problem #3)**
  - **Group Anagrams (Problem #49)**
  - **Top K Frequent Elements (Problem #347)**
  - **Valid Anagram (Problem #242)**
  - **Intersection of Two Arrays II (Problem #350)**

- **Python Implementation:**

  ```python
  # Example 1: Basic Dictionary Operations
  hash_map = {}
  hash_map['key'] = 'value'    # Insert key-value pair
  print(hash_map)              # Output: {'key': 'value'}

  value = hash_map.get('key')  # Access value by key
  print(value)                 # Output: value

  hash_map.pop('key')          # Remove key-value pair
  print(hash_map)              # Output: {}

  # Example 2: Counting Frequencies
  words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
  frequency = {}
  for word in words:
      if word in frequency:
          frequency[word] += 1
      else:
          frequency[word] = 1
  print(frequency)
  # Output: {'apple': 3, 'banana': 2, 'orange': 1}

  # Example 3: Using get() with Default Values
  counts = {}
  items = ['a', 'b', 'c', 'a', 'b', 'a']
  for item in items:
      counts[item] = counts.get(item, 0) + 1
  print(counts)
  # Output: {'a': 3, 'b': 2, 'c': 1}

  # Example 4: Checking for Key Existence
  user_info = {'name': 'Alice', 'age': 25}
  if 'email' in user_info:
      print(user_info['email'])
  else:
      print("Email not found.")
  # Output: Email not found.

  # Example 5: Iterating Over Keys and Values
  student_scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78}
  for student, score in student_scores.items():
      print(f"{student}: {score}")
  # Output:
  # Alice: 85
  # Bob: 92
  # Charlie: 78

  # Example 6: Dictionary Comprehension
  squares = {x: x**2 for x in range(5)}
  print(squares)
  # Output: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
  ```

- **Time Complexity:**
  
  - **Insert:** O(1) average
  - **Access:** O(1) average
  - **Delete:** O(1) average
  - **Search:** O(1) average
  - **Iteration:** O(n), where n is the number of key-value pairs

- **Space Complexity:**  
  O(n), where n is the number of key-value pairs stored in the hash table.

- **Additional Notes:**
  
  - **Hash Function:**  
    Python uses a robust hash function for its keys, ensuring a uniform distribution of keys to minimize collisions.
  
  - **Handling Collisions:**  
    Internally, Python handles collisions using methods like open addressing, ensuring that even with collisions, operations remain efficient.
  
  - **Immutable Keys:**  
    Keys in a dictionary must be immutable types (e.g., strings, numbers, tuples), ensuring their hash values remain constant.

- **Best Practices:**
  
  - **Use Immutable Types as Keys:**  
    Only use immutable and hashable types as keys to prevent unexpected behavior.
  
  - **Leverage `get()` for Safe Access:**  
    Use the `get()` method to safely access values without risking `KeyError` exceptions.
  
  - **Use Dictionary Comprehensions:**  
    They provide a concise and efficient way to create dictionaries.
  
  - **Avoid Modifying Keys:**  
    Once a key is added to a dictionary, avoid modifying it to maintain hash integrity.

- **Example: Implementing Two Sum Using a Hash Table**

  ```python
  def two_sum(nums, target):
      hash_map = {}
      for i, num in enumerate(nums):
          complement = target - num
          if complement in hash_map:
              return [hash_map[complement], i]
          hash_map[num] = i
      return []

  # Usage
  nums = [2, 7, 11, 15]
  target = 9
  print(two_sum(nums, target))  # Output: [0, 1]
  ```

  **Explanation:**  
  This function uses a hash table (`hash_map`) to store each number and its index as it iterates through the list. For each number, it calculates the complement (`target - num`) and checks if it exists in the hash table. If it does, it returns the indices of the two numbers that add up to the target. This approach ensures O(n) time complexity.

### 3.2 OrderedDict

- **Description:**  
  `OrderedDict` is a subclass of the built-in `dict` class in Python's `collections` module. Unlike standard dictionaries (prior to Python 3.7), which do not maintain the order of keys, an `OrderedDict` preserves the insertion order of keys. This means that when iterating over an `OrderedDict`, items are returned in the order they were added. Additionally, `OrderedDict` provides specialized methods such as `move_to_end()` and `popitem()` that offer more control over the ordering of elements.

- **When to Use:**  
  Use `OrderedDict` when:
  - **Order Preservation is Crucial:** When the sequence of key insertions matters, such as in scenarios where the order impacts the logic or output.
  - **Implementing LRU Caches:** `OrderedDict` can efficiently manage least recently used (LRU) caches by moving accessed items to the end.
  - **Reordering Elements:** When you need to dynamically reorder elements, such as moving a specific key to the beginning or end.
  - **Comparing Dictionaries with Order Sensitivity:** When the order of key-value pairs is significant for equality comparisons.

- **Key Patterns:**
  - **LRU Cache Implementation:** Managing cache entries with efficient eviction policies based on usage order.
  - **Maintaining Sequence in Data Processing:** Ensuring data is processed in the exact order of insertion.
  - **Reordering Based on Priority or Frequency:** Dynamically adjusting the order of elements based on changing priorities or frequencies.
  - **Iterating in a Specific Order:** When the iteration order of key-value pairs affects the outcome of algorithms or processes.

- **LeetCode Problem Types:**
  - **LRU Cache (Problem #146):** Implementing an LRU cache requires maintaining the order of key accesses to efficiently evict the least recently used items.
  - **Design a Hit Counter (Problem #362):** Managing time-based events in the order they occur.
  - **Design a File System (Problem #588):** Maintaining the order of file and directory creations.
  - **First Unique Character in a String (Problem #387):** Tracking the order of character occurrences to identify uniqueness efficiently.

- **Python Implementation:**

  ```python
  from collections import OrderedDict

  # Example 1: Basic Usage of OrderedDict
  print("Example 1: Basic OrderedDict")
  od = OrderedDict()
  od['a'] = 1
  od['b'] = 2
  od['c'] = 3
  od['d'] = 4

  for key, value in od.items():
      print(key, value)
  # Output:
  # a 1
  # b 2
  # c 3
  # d 4

  # Example 2: Changing Value of a Key
  print("\nExample 2: Changing Value of a Key")
  od['c'] = 5
  for key, value in od.items():
      print(key, value)
  # Output:
  # a 1
  # b 2
  # c 5
  # d 4

  # Example 3: Equality Comparison
  print("\nExample 3: Equality Comparison")
  od1 = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
  od2 = OrderedDict([('c', 3), ('b', 2), ('a', 1)])
  print(od1 == od2)  # Output: False

  # Example 4: Reversing an OrderedDict
  print("\nExample 4: Reversing OrderedDict")
  reversed_od = OrderedDict(reversed(list(od.items())))
  for key, value in reversed_od.items():
      print(key, value)
  # Output:
  # d 4
  # c 5
  # b 2
  # a 1

  # Example 5: Using popitem()
  print("\nExample 5: Using popitem()")
  last_item = od.popitem(last=True)
  print("Popped Item:", last_item)  # Output: ('d', 4)
  for key, value in od.items():
      print(key, value)
  # Output:
  # a 1
  # b 2
  # c 5

  # Example 6: Moving Keys to End or Beginning
  print("\nExample 6: Moving Keys")
  od.move_to_end('a')  # Move 'a' to the end
  od.move_to_end('b', last=False)  # Move 'b' to the beginning
  for key, value in od.items():
      print(key, value)
  # Output:
  # b 2
  # c 5
  # a 1
  ```

- **Time Complexity:**
  
  - **Get Item (`od[key]`):** O(1)
  - **Set Item (`od[key] = value`):** O(1)
  - **Delete Item (`del od[key]`):** O(1)
  - **Move to End (`move_to_end`):** O(1)
  - **Pop Item (`popitem`):** O(1)
  - **Iteration:** O(n)

- **Space Complexity:**  
  O(n), where n is the number of items in the `OrderedDict`.

- **Additional Notes:**
  
  - **Order Preservation in Python 3.7+:** Starting from Python 3.7, the built-in `dict` class maintains insertion order as an implementation detail (officially part of the language specification from Python 3.8 onwards). However, `OrderedDict` still offers additional methods that are not available in the standard `dict`, making it useful for specific scenarios that require order manipulation.
  
  - **Reordering Capabilities:** `OrderedDict` provides methods like `move_to_end()` and `popitem()` with parameters to facilitate dynamic reordering, which are not available in standard dictionaries.
  
  - **Use in Caching Mechanisms:** Due to its ordered nature and efficient reordering methods, `OrderedDict` is ideal for implementing caching strategies like LRU (Least Recently Used).

- **Best Practices:**
  
  - **Choose `OrderedDict` for Explicit Order Requirements:** Even though standard dictionaries maintain order in Python 3.7+, use `OrderedDict` when you need explicit control over the ordering of elements.
  
  - **Leverage `move_to_end()` for Efficient Reordering:** Utilize `move_to_end()` to adjust the position of elements without reconstructing the entire dictionary.
  
  - **Implement Caching Mechanisms:** `OrderedDict` is highly suitable for implementing caches that require maintaining the order of item usage, such as LRU caches.
  
  - **Use in Algorithms Requiring Ordered Data:** When the order of elements is critical for the correctness or efficiency of the algorithm.

- **Example: Implementing an LRU Cache Using `OrderedDict`**

  ```python
  from collections import OrderedDict

  class LRUCache:
      def __init__(self, capacity: int):
          self.cache = OrderedDict()
          self.capacity = capacity

      def get(self, key: int) -> int:
          if key not in self.cache:
              return -1
          self.cache.move_to_end(key)
          return self.cache[key]

      def put(self, key: int, value: int) -> None:
          if key in self.cache:
              self.cache.move_to_end(key)
          self.cache[key] = value
          if len(self.cache) > self.capacity:
              self.cache.popitem(last=False)

  # Usage
  lru = LRUCache(2)
  lru.put(1, 1)
  lru.put(2, 2)
  print(lru.get(1))  # Output: 1
  lru.put(3, 3)      # Evicts key 2
  print(lru.get(2))  # Output: -1
  lru.put(4, 4)      # Evicts key 1
  print(lru.get(1))  # Output: -1
  print(lru.get(3))  # Output: 3
  print(lru.get(4))  # Output: 4
  ```

  **Explanation:**  
  This implementation of an LRU Cache uses `OrderedDict` to maintain the order of key insertions and accesses. When a key is accessed via `get`, it is moved to the end to mark it as recently used. When adding a new key via `put`, if the cache exceeds its capacity, the least recently used item (the first item) is evicted using `popitem(last=False)`.

### 3.3 DefaultDict

- **Description:**  
  `DefaultDict` is a subclass of Python’s built-in `dict` class, available in the `collections` module. Unlike a standard dictionary, a `DefaultDict` automatically assigns a default value to any key that does not exist, thereby preventing the typical `KeyError` that arises when accessing non-existent keys. This default value is provided by a factory function specified during the creation of the `DefaultDict`. Common factory functions include `list`, `int`, `str`, and custom lambda functions. This feature makes `DefaultDict` particularly useful for tasks that involve grouping, counting, or aggregating data without the need to explicitly check for the existence of keys.

- **When to Use:**  
  Use `DefaultDict` in scenarios where:
  - **Handling Missing Keys:** When you frequently access keys that may not exist and want to avoid handling `KeyError`.
  - **Grouping Data:** When grouping items based on certain criteria, such as categorizing words by their lengths or grouping numbers by their remainders.
  - **Counting Frequencies:** When counting occurrences of items, such as characters in a string or elements in a list.
  - **Aggregating Data:** When aggregating values into lists, sets, or other collections without initializing them manually.
  - **Simplifying Code:** To write cleaner and more concise code by eliminating the need for key existence checks.

- **Key Patterns:**
  - **Frequency Counting:** Efficiently count occurrences of elements without initializing counts.
  - **Grouping Items:** Group elements based on a common key or property.
  - **Accumulating Values:** Collect values into lists, sets, or other containers for each key.
  - **Dynamic Data Aggregation:** Aggregate data on-the-fly without prior knowledge of all possible keys.
  - **Simplifying Nested Dictionaries:** Create nested dictionaries with default values to represent multi-level data structures.

- **LeetCode Problem Types:**
  - **Group Anagrams (Problem #49):** Group words that are anagrams of each other.
  - **Top K Frequent Elements (Problem #347):** Identify the most frequent elements in a list.
  - **Letter Combinations of a Phone Number (Problem #17):** Group letters based on digit mappings.
  - **Binary Tree Level Order Traversal (Problem #102):** Group tree nodes by their levels.
  - **Insert Delete GetRandom O(1) (Problem #380):** Manage dynamic data with efficient access.
  - **Word Pattern (Problem #290):** Match words based on a specific pattern.

- **Python Implementation:**

  ```python
  from collections import defaultdict

  # Example 1: Basic Usage of DefaultDict
  print("Example 1: Basic DefaultDict")
  d = defaultdict(list)
  d['fruits'].append('apple')
  d['vegetables'].append('carrot')
  print(d)
  # Output: defaultdict(<class 'list'>, {'fruits': ['apple'], 'vegetables': ['carrot']})

  print("\nAccessing a non-existent key:")
  print(d['juices'])
  # Output: []

  # Example 2: Using int as Default Factory for Counting
  print("\nExample 2: Counting with DefaultDict(int)")
  count = defaultdict(int)
  items = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
  for item in items:
      count[item] += 1
  print(count)
  # Output: defaultdict(<class 'int'>, {'apple': 3, 'banana': 2, 'orange': 1})

  # Example 3: Using str as Default Factory
  print("\nExample 3: DefaultDict with str")
  greetings = defaultdict(str)
  greetings['morning'] = 'Good morning!'
  print(greetings['evening'])
  # Output: ''

  # Example 4: Grouping Items Using DefaultDict(list)
  print("\nExample 4: Grouping with DefaultDict(list)")
  group = defaultdict(list)
  pairs = [('a', 1), ('b', 2), ('a', 3), ('b', 4), ('c', 5)]
  for key, value in pairs:
      group[key].append(value)
  print(group)
  # Output: defaultdict(<class 'list'>, {'a': [1, 3], 'b': [2, 4], 'c': [5]})
  ```

- **Time Complexity:**
  
  - **Accessing an Item (`d[key]`):** O(1)
  - **Setting an Item (`d[key] = value`):** O(1)
  - **Deleting an Item (`del d[key]`):** O(1)
  - **Iteration (`for key in d`):** O(n), where n is the number of keys
  - **Default Factory Invocation:** O(1) when a missing key is accessed

- **Space Complexity:**  
  O(n), where n is the number of unique keys stored in the `DefaultDict`.

- **Additional Notes:**
  
  - **Default Factory Function:**  
    The `default_factory` is a callable that provides the default value for missing keys. If `default_factory` is `None`, `DefaultDict` behaves like a regular `dict` and raises a `KeyError` for missing keys.
  
  - **Avoid Using Mutable Default Factories Unnecessarily:**  
    When using mutable default factories like `list` or `set`, be cautious to avoid unintended side effects by modifying shared default values.
  
  - **Nested DefaultDicts:**  
    You can create nested `DefaultDicts` to handle multi-level dictionaries seamlessly.
  
    ```python
    from collections import defaultdict

    nested_dict = defaultdict(lambda: defaultdict(int))
    nested_dict['outer']['inner'] += 1
    print(nested_dict)
    # Output: defaultdict(<function <lambda> at 0x...>, {'outer': defaultdict(<class 'int'>, {'inner': 1})})
    ```
  
  - **Immutable Default Factories:**  
    Use immutable default factories like `int`, `str`, or `tuple` when you do not intend to modify the default values after creation.

- **Best Practices:**
  
  - **Choose the Appropriate Default Factory:**  
    Select a default factory that aligns with your data aggregation needs. For example, use `list` for grouping items, `int` for counting, and `set` for collecting unique items.
  
  - **Leverage DefaultDict to Simplify Code:**  
    Utilize `DefaultDict` to eliminate the need for explicit key existence checks, resulting in cleaner and more readable code.
  
  - **Use Nested DefaultDicts for Complex Structures:**  
    For multi-level data structures, nested `DefaultDicts` can simplify the process of building and accessing nested data.
  
  - **Combine with Other Data Structures:**  
    `DefaultDict` can be effectively combined with other data structures like `OrderedDict` to maintain order while handling defaults.
  
  - **Be Mindful of Memory Usage:**  
    While `DefaultDict` provides convenience, be aware of the potential memory overhead, especially when dealing with a large number of default values.

- **Example: Counting Word Frequencies Using `DefaultDict(int)`**

  ```python
  from collections import defaultdict

  # Sample text
  text = "the quick brown fox jumps over the lazy dog the fox was quick"

  # Initialize DefaultDict with int to count word frequencies
  word_count = defaultdict(int)

  # Split text into words and count frequencies
  for word in text.split():
      word_count[word] += 1

  # Display word counts
  for word, count in word_count.items():
      print(f"{word}: {count}")

  # Output:
  # the: 3
  # quick: 2
  # brown: 1
  # fox: 2
  # jumps: 1
  # over: 1
  # lazy: 1
  # dog: 1
  # was: 1
  ```

- **Example: Grouping Students by Grade Using `DefaultDict(list)`**

  ```python
  from collections import defaultdict

  # List of students with their grades
  students = [
      ('Alice', 'A'),
      ('Bob', 'B'),
      ('Charlie', 'A'),
      ('David', 'C'),
      ('Eve', 'B'),
      ('Frank', 'A')
  ]

  # Initialize DefaultDict with list to group students by grade
  grade_groups = defaultdict(list)

  # Group students by their grades
  for name, grade in students:
      grade_groups[grade].append(name)

  # Display grouped students
  for grade, names in grade_groups.items():
      print(f"Grade {grade}: {', '.join(names)}")

  # Output:
  # Grade A: Alice, Charlie, Frank
  # Grade B: Bob, Eve
  # Grade C: David
  ```

- **DefaultDict in Python – FAQs**

  **1. What is `DefaultDict` in Python?**  
  `DefaultDict` is a subclass of the built-in `dict` class in Python's `collections` module. It overrides one method and adds one writable instance variable. The main feature of `DefaultDict` is that it provides a default value for a key that does not exist, thereby preventing `KeyError` exceptions.

  **2. How does `DefaultDict` differ from a regular `dict`?**  
  - **Default Values:**  
    - `dict`: Raises a `KeyError` when accessing a non-existent key.
    - `DefaultDict`: Automatically assigns a default value to a non-existent key based on the provided factory function.
  - **Initialization:**  
    - `dict`: Initialized without a default factory.
    - `DefaultDict`: Requires a default factory function at initialization.
  
  **3. What is the `default_factory` in `DefaultDict`?**  
  The `default_factory` is a callable that provides the default value for missing keys. It is specified when creating a `DefaultDict`. If `default_factory` is `None`, `DefaultDict` behaves like a regular `dict`.

  **4. Can `DefaultDict` handle complex data structures?**  
  Yes, `DefaultDict` can handle complex data structures by using appropriate factory functions, such as `list`, `set`, `dict`, or even custom lambda functions to create nested structures.

  **5. How does `DefaultDict` prevent `KeyError`?**  
  When accessing a key that does not exist, `DefaultDict` uses the `default_factory` to create a default value for that key, inserts it into the dictionary, and returns the default value instead of raising a `KeyError`.

  **6. When should you prefer `DefaultDict` over `dict.setdefault()`?**  
  - **Readability and Efficiency:**  
    `DefaultDict` provides a cleaner and more readable way to handle default values without repeatedly calling `setdefault()`.
  - **Performance:**  
    `DefaultDict` can offer better performance in scenarios with numerous default value assignments.
  
  **7. Can you convert a `DefaultDict` to a regular `dict`?**  
  Yes, you can convert a `DefaultDict` to a regular `dict` using the `dict()` constructor:

  ```python
  from collections import defaultdict

  dd = defaultdict(int)
  dd['a'] += 1
  dd['b'] += 2

  regular_dict = dict(dd)
  print(regular_dict)
  # Output: {'a': 1, 'b': 2}
  ```

  **8. Are `DefaultDicts` ordered?**  
  Starting from Python 3.7, regular dictionaries maintain insertion order as part of the language specification. `DefaultDict`, being a subclass of `dict`, also maintains this order. However, `DefaultDict` does not provide additional ordering capabilities beyond those of `dict`.

  **9. Can `DefaultDict` be used with immutable default factories?**  
  Yes, `DefaultDict` can be used with any callable that returns an immutable type, such as `int`, `str`, or `tuple`. However, be cautious when using mutable default factories like `list` or `dict` to prevent unintended side effects.

  **10. How do you create a nested `DefaultDict`?**  
  You can create a nested `DefaultDict` by using a lambda function or another `DefaultDict` as the `default_factory`:

  ```python
  from collections import defaultdict

  nested_dd = defaultdict(lambda: defaultdict(int))
  nested_dd['outer']['inner'] += 1
  print(nested_dd)
  # Output: defaultdict(<function <lambda> at 0x...>, {'outer': defaultdict(<class 'int'>, {'inner': 1})})
  ```

By leveraging `DefaultDict`, you can simplify your code for tasks involving default values, grouping, counting, and aggregating data, making it an invaluable tool for competitive programming and data manipulation tasks.

### 3.4 Counter

- **Description:**  
  The `Counter` class is a specialized container provided by Python's `collections` module. It is a subclass of `dict` designed specifically for counting hashable objects. Internally, `Counter` creates a hash table that maps elements to their counts, making it highly efficient for frequency counting, grouping, and aggregating tasks. The `elements()` method of a `Counter` object returns an iterator over elements, repeating each as many times as its count. Notably, elements with a count less than one are omitted from the iteration. This makes `Counter` particularly useful in scenarios where you need to process or manipulate data based on the frequency of elements.

- **When to Use:**  
  Use `Counter` when:
  - **Frequency Counting:** When you need to count the occurrences of elements in an iterable, such as words in a text or items in a list.
  - **Grouping Items:** When grouping items based on their counts or other properties.
  - **Aggregating Data:** When aggregating values, such as summing counts from multiple sources.
  - **Simplifying Code:** To write cleaner and more concise code for counting and aggregating without manual dictionary handling.
  - **Handling Missing Data Gracefully:** When you want to avoid `KeyError` exceptions while accessing counts of non-existent keys.

- **Key Patterns:**
  - **Counting Frequencies:** Efficiently tallying occurrences of elements without manual initialization.
  - **Finding Most Common Elements:** Quickly identifying the most frequent elements using built-in methods.
  - **Expanding Compact Representations:** Using `elements()` to convert a compact count representation back into a full iterable form.
  - **Arithmetic Operations on Counts:** Performing addition, subtraction, intersection, and union of counts.
  - **Handling Multisets:** Managing collections where elements can appear multiple times, similar to mathematical multisets.

- **LeetCode Problem Types:**
  - **Group Anagrams (Problem #49):** Grouping words that are anagrams by counting character frequencies.
  - **Top K Frequent Elements (Problem #347):** Identifying the most frequent elements in a list.
  - **Letter Combinations of a Phone Number (Problem #17):** Mapping digits to letters and counting combinations.
  - **Binary Tree Level Order Traversal (Problem #102):** Counting nodes at each level of a binary tree.
  - **Word Pattern (Problem #290):** Matching words based on specific frequency patterns.
  - **First Unique Character in a String (Problem #387):** Identifying characters with a frequency of one.

- **Python Implementation:**

  ```python
  from collections import Counter

  # Example 1: Working of elements() on a simple data container
  print("Example 1: elements() with a string")
  x = Counter("geeksforgeeks")
  for i in x.elements():
      print(i, end=" ")
  # Output: g g e e e e k k s s f o r g e e k s
  print("\n")

  # Example 2: Creating Counter with a list
  print("Example 2: Counter with a list")
  a = [12, 3, 4, 3, 5, 11, 12, 6, 7]
  x = Counter(a)
  print(x)
  # Output: Counter({12: 2, 3: 2, 4: 1, 5: 1, 11: 1, 6: 1, 7: 1})

  for i in x.keys():
      print(f"{i} : {x[i]}")
  # Output:
  # 12 : 2
  # 3 : 2
  # 4 : 1
  # 5 : 1
  # 11 : 1
  # 6 : 1
  # 7 : 1

  x_keys = list(x.keys())
  x_values = list(x.values())
  print(x_keys)
  # Output: [12, 3, 4, 5, 11, 6, 7]
  print(x_values)
  # Output: [2, 2, 1, 1, 1, 1, 1]

  # Example 3: Elements on a variety of Counter objects with different data-containers
  print("\nExample 3: elements() with various Counter objects")
  
  # Example - 1
  a = Counter("geeksforgeeks")
  for i in a.elements():
      print(i, end=" ")
  print()
  
  # Example - 2
  b = Counter({'geeks': 4, 'for': 1, 'gfg': 2, 'python': 3})
  for i in b.elements():
      print(i, end=" ")
  print()
  
  # Example - 3
  c = Counter([1, 2, 21, 12, 2, 44, 5, 13, 15, 5, 19, 21, 5])
  for i in c.elements():
      print(i, end=" ")
  print()
  
  # Example - 4
  d = Counter(a=2, b=3, c=6, d=1, e=5)
  for i in d.elements():
      print(i, end=" ")
  # Output:
  # g g e e e e k k s s f o r g e e k s 
  # geeks geeks geeks geeks for gfg gfg python python python 
  # 1 2 2 21 21 12 44 5 5 5 13 15 19 
  # a a b b b c c c c c c d e e e e e 
  ```

  ```python
  # Example 4: Demonstrating what elements() returns when printed directly
  from collections import Counter

  # Creating a raw data-set
  x = Counter("geeksforgeeks")

  # Will return an itertools.chain object
  print(x.elements())
  # Output: itertools.chain object at 0x037209F0
  ```

  ```python
  # Example 5: Handling zero and negative counts
  from collections import Counter

  # Creating a raw data-set using keyword arguments
  x = Counter(a=2, x=3, b=3, z=1, y=5, c=0, d=-3)

  # Printing out the elements
  for i in x.elements():
      print(f"{i} : {x[i]}")
  # Output:
  # a : 2
  # a : 2
  # x : 3
  # x : 3
  # x : 3
  # b : 3
  # b : 3
  # b : 3
  # z : 1
  # y : 5
  # y : 5
  # y : 5
  # y : 5
  # y : 5
  ```

- **Time Complexity:**
  
  - **Creating a Counter (`Counter(iterable)`):** O(n), where n is the number of elements in the iterable.
  - **Accessing an Item (`counter[key]`):** O(1)
  - **Updating Counts (`counter[key] += 1`):** O(1)
  - **elements() Method:** O(k), where k is the total count of all elements.
  - **Iteration (`for key in counter`):** O(n), where n is the number of unique keys.

- **Space Complexity:**  
  O(n), where n is the number of unique elements in the `Counter`.

- **Additional Notes:**
  
  - **Immutable and Hashable:**  
    `Counter` only works with hashable and immutable objects, such as strings, numbers, and tuples.
  
  - **Arithmetic Operations:**  
    `Counter` supports arithmetic operations like addition, subtraction, intersection, and union, enabling the combination and comparison of counts.
  
  - **most_common() Method:**  
    Retrieve the most common elements and their counts.
    
    ```python
    from collections import Counter

    c = Counter('abracadabra')
    print(c.most_common(2))
    # Output: [('a', 5), ('b', 2)]
    ```
  
  - **subtract() Method:**  
    Subtract counts from another `Counter` or iterable.
    
    ```python
    from collections import Counter

    c1 = Counter(a=4, b=2, c=0)
    c2 = Counter(a=1, b=2)
    c1.subtract(c2)
    print(c1)
    # Output: Counter({'a': 3, 'b': 0, 'c': 0})
    ```
  
  - **Support for Negative Counts:**  
    `Counter` allows negative counts, which can be useful in certain algorithms but should be handled carefully to avoid logical errors.

- **Best Practices:**
  
  - **Use `Counter` for Frequency-Based Problems:**  
    Leverage `Counter` in scenarios where frequency of elements is a primary concern, such as in word count, inventory management, or analyzing patterns.
  
  - **Combine with Other Data Structures:**  
    `Counter` can be effectively combined with lists, sets, and other collections to perform complex data manipulations.
  
  - **Avoid Mutable Default Factories:**  
    When using `Counter` in conjunction with other mutable structures, ensure that modifications do not lead to unintended side effects.
  
  - **Utilize Built-in Methods:**  
    Take advantage of methods like `most_common()`, `elements()`, and arithmetic operations to simplify your code and improve performance.
  
  - **Handle Negative Counts Appropriately:**  
    If your application logic does not require negative counts, ensure that your operations do not inadvertently create them.

- **Applications:**
  
  `Counter` objects and their methods are invaluable for processing large datasets efficiently. They are extensively used in:
  
  - **Text Analysis:** Counting word frequencies, identifying common phrases, or analyzing character distributions.
  - **Data Aggregation:** Summarizing data from logs, databases, or real-time streams.
  - **Competitive Programming:** Solving problems that require efficient counting and frequency management.
  - **Inventory Systems:** Tracking quantities of items in stock.
  - **Statistical Analysis:** Gathering counts for categorical data in statistics and machine learning.

- **Example: Counting Word Frequencies Using `Counter`**

  ```python
  from collections import Counter

  # Sample text
  text = "the quick brown fox jumps over the lazy dog the fox was quick"

  # Initialize Counter to count word frequencies
  word_count = Counter(text.split())

  # Display word counts
  for word, count in word_count.items():
      print(f"{word}: {count}")

  # Output:
  # the: 3
  # quick: 2
  # brown: 1
  # fox: 2
  # jumps: 1
  # over: 1
  # lazy: 1
  # dog: 1
  # was: 1
  ```

- **Example: Finding the Most Common Elements**

  ```python
  from collections import Counter

  data = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
  counter = Counter(data)
  most_common = counter.most_common(2)
  print(most_common)
  # Output: [('apple', 3), ('banana', 2)]
  ```

- **Counter in Python – FAQs**

  **1. How to Use the `elements()` Method in Python Counter?**  
  The `elements()` method in Python's `Counter` class returns an iterator over elements, repeating each as many times as its count. Elements with counts less than one are excluded. This method is useful for expanding a compact count representation into its full iterable form.

  **Example:**
  ```python
  from collections import Counter

  counter = Counter(a=3, b=2, c=1)
  elements = list(counter.elements())
  print(elements)  # Output: ['a', 'a', 'a', 'b', 'b', 'c']
  ```

  **2. How to Count Items in an Iterable Using Python Counter?**  
  The `Counter` class can count the occurrences of each item in an iterable, such as a list or a string, by passing the iterable to the `Counter` constructor. It returns a `Counter` object where keys are the elements and values are their counts.

  **Example:**
  ```python
  from collections import Counter

  items = ['apple', 'banana', 'apple', 'orange', 'banana']
  counter = Counter(items)
  print(counter)  # Output: Counter({'apple': 2, 'banana': 2, 'orange': 1})
  ```

  **3. Can Counter Handle Negative Counts in Python?**  
  Yes, `Counter` can handle negative counts. This feature allows for arithmetic operations on `Counter` objects, such as subtraction, which can result in negative counts. However, elements with a negative count are still part of the `Counter` object and are excluded from methods like `elements()`.

  **Example:**
  ```python
  from collections import Counter

  counter = Counter(a=3, b=-2, c=1)
  print(counter)  # Output: Counter({'a': 3, 'c': 1, 'b': -2})
  ```

  **4. How to Combine Counters in Python?**  
  You can combine `Counter` objects using arithmetic operations like addition and subtraction, or by using the `update()` method. These operations allow you to aggregate counts, find differences, or update counts based on another `Counter` object.

  - **Using Addition:**
    ```python
    from collections import Counter

    counter1 = Counter(a=3, b=2)
    counter2 = Counter(a=1, b=2, c=3)
    combined = counter1 + counter2
    print(combined)  # Output: Counter({'a': 4, 'b': 4, 'c': 3})
    ```

  - **Using Subtraction:**
    ```python
    from collections import Counter

    counter1 = Counter(a=3, b=2)
    counter2 = Counter(a=1, b=2, c=3)
    difference = counter1 - counter2
    print(difference)  # Output: Counter({'a': 2})
    ```

  - **Using `update()` Method:**
    ```python
    from collections import Counter

    counter1 = Counter(a=3, b=2)
    counter2 = Counter(a=1, b=2, c=3)
    counter1.update(counter2)
    print(counter1)  # Output: Counter({'a': 4, 'b': 4, 'c': 3})
    ```

  **5. What is the Difference Between `Counter` and `dict` in Python?**  
  - **Purpose:**  
    - `dict`: A general-purpose dictionary for storing key-value pairs.
    - `Counter`: A specialized dictionary subclass designed for counting hashable objects.
  
  - **Default Values:**  
    - `dict`: Raises a `KeyError` when accessing a non-existent key.
    - `Counter`: Initializes missing keys with a default count of zero.
  
  - **Methods:**  
    - `Counter` provides additional methods like `most_common()`, `elements()`, and supports arithmetic operations.
  
  **Example:**
  ```python
  from collections import Counter

  # Using dict
  d = {}
  d['a'] = d.get('a', 0) + 1
  print(d)  # Output: {'a': 1}

  # Using Counter
  c = Counter()
  c['a'] += 1
  print(c)  # Output: Counter({'a': 1})
  ```

  **6. Can `Counter` Be Used with Immutable Default Factories?**  
  Yes, `Counter` works with any hashable and immutable objects, such as strings, numbers, and tuples. While `Counter` inherently deals with counts (integers), it can be used in conjunction with other immutable types as keys.

  **Example:**
  ```python
  from collections import Counter

  counter = Counter([(1, 2), (3, 4), (1, 2)])
  print(counter)  # Output: Counter({(1, 2): 2, (3, 4): 1})
  ```

  **7. How to Convert a `Counter` to a Regular `dict`?**  
  You can convert a `Counter` object to a regular `dict` using the `dict()` constructor.

  **Example:**
  ```python
  from collections import Counter

  c = Counter(a=3, b=2, c=1)
  regular_dict = dict(c)
  print(regular_dict)  # Output: {'a': 3, 'b': 2, 'c': 1}
  ```

  **8. Are `Counter` Objects Ordered?**  
  Starting from Python 3.7, regular dictionaries maintain insertion order as part of the language specification. Since `Counter` is a subclass of `dict`, it also maintains this order. However, `Counter` does not provide additional ordering capabilities beyond those of `dict`.

  **Example:**
  ```python
  from collections import Counter

  c = Counter(['a', 'b', 'a', 'c'])
  print(c)  # Output: Counter({'a': 2, 'b': 1, 'c': 1})
  ```

  **9. Can `Counter` Handle Nested Data Structures?**  
  `Counter` can handle nested data structures by using tuples or other hashable types as keys. However, for multi-level counting, it's often more effective to use nested `Counter` objects or combine `Counter` with other data structures like `defaultdict`.

  **Example:**
  ```python
  from collections import Counter

  nested_counter = Counter()
  nested_counter[('a', 1)] += 1
  nested_counter[('b', 2)] += 2
  print(nested_counter)  # Output: Counter({('b', 2): 2, ('a', 1): 1})
  ```

  **10. How to Handle Zero or Negative Counts in `Counter`?**  
  Elements with counts less than one are excluded from the `elements()` iterator. However, they remain part of the `Counter` object and can be accessed or manipulated like any other elements.

  **Example:**
  ```python
  from collections import Counter

  c = Counter(a=3, b=0, c=-1)
  print(list(c.elements()))  # Output: ['a', 'a', 'a']
  print(c)  # Output: Counter({'a': 3, 'b': 0, 'c': -1})
  ```

By leveraging the `Counter` class and its `elements()` method, you can efficiently manage and manipulate frequency-based data, making it an essential tool for competitive programming and data analysis tasks.

## 4. Sets

- **Description:**  
  A Set in Python is used to store a collection of unique items with the following properties:
  - **No Duplicate Elements:** If you try to insert the same item again, it overwrites the previous one.
  - **Unordered Collection:** Sets are unordered, meaning that when you access all items, they are accessed without any specific order, and you cannot access items using indices as you can with lists.
  - **Efficient Operations:** Internally implemented using hashing, making sets efficient for search, insert, and delete operations.
  - **Mutable:** You can add or remove elements after their creation, but the individual elements within the set cannot be changed directly.

- **When to Use:**  
  Ideal for scenarios where:
  - You need to store unique elements.
  - You require efficient membership testing.
  - You need to perform set operations like union, intersection, and difference.
  - Eliminating duplicates from a collection.

- **Key Patterns:**
  - **Eliminating Duplicates:** Removing duplicate elements from a list or other iterable.
  - **Membership Testing:** Quickly checking if an element exists within a collection.
  - **Set Operations:** Performing unions, intersections, differences, and symmetric differences.
  - **Frequency Counting:** When combined with `Counter` for counting occurrences of unique elements.

- **LeetCode Problem Types:**
  - **Two Sum (Problem #1)**
  - **Group Anagrams (Problem #49)**
  - **Top K Frequent Elements (Problem #347)**
  - **Intersection of Two Arrays (Problem #349)**
  - **Distinct Elements in an Array**
  - **Check if an Array is a Subset of Another**
  
- **Python Implementation:**

  ```python
  # Example 1: Creating a Set
  s = {10, 50, 20}
  print(s)          # Output: {10, 50, 20}
  print(type(s))    # Output: <class 'set'>
  
  # Example 2: Type Casting with set()
  # Typecasting list to set
  s = set(["a", "b", "c"])
  print(s)          # Output: {'a', 'b', 'c'}
  
  # Adding elements to the set
  s.add("d")
  print(s)          # Output: {'a', 'b', 'c', 'd'}
  
  # Adding multiple elements using a loop
  for i in range(1, 6):
      s.add(i)
  print(s)          # Output: {1, 2, 3, 4, 5, 'a', 'b', 'c', 'd'}

  # check if an element is present in the set
  print("a" in s)   # Output: True
  ```

- **Time Complexity:**
  - **Add (`add`):** O(1) average
  - **Remove (`remove`):** O(1) average
  - **Membership Test (`in`):** O(1) average
  - **Union (`|`), Intersection (`&`), Difference (`-`), Symmetric Difference (`^`):** O(len(s) + len(t))
  
- **Space Complexity:**  
  O(n), where n is the number of elements in the set.

- **Additional Notes:**
  - **Immutable Elements:** Only immutable (hashable) types can be added to a set. Mutable types like lists or dictionaries cannot be added.
  - **No Order Guarantee:** The order of elements in a set is not guaranteed and may vary.
  - **Frozen Sets:** For immutable sets, use `frozenset()`, which allows sets to be used as dictionary keys or elements of other sets.

- **Best Practices:**
  - **Use Sets for Unordered Unique Collections:** When the order of elements is not important, and uniqueness is required.
  - **Leverage Set Operations for Efficient Computations:** Utilize built-in set operations for tasks like finding common elements or differences.
  - **Avoid Using Lists for Membership Tests:** Sets provide faster membership testing compared to lists.
  - **Combine with Other Data Structures:** Use sets alongside lists or dictionaries for more complex data manipulation tasks.

- **Examples:**

  #### Example 1: Checking for Unique Elements
  ```python
  # Removing duplicates from a list
  numbers = [1, 2, 2, 3, 4, 4, 5]
  unique_numbers = set(numbers)
  print(unique_numbers)  # Output: {1, 2, 3, 4, 5}
  ```

  #### Example 2: Set Operations
  ```python
  set1 = {1, 2, 3, 4}
  set2 = {3, 4, 5, 6}

  # Union
  union_set = set1 | set2
  print("Union:", union_set)  # Output: Union: {1, 2, 3, 4, 5, 6}

  # Intersection
  intersection_set = set1 & set2
  print("Intersection:", intersection_set)  # Output: Intersection: {3, 4}

  # Difference
  difference_set = set1 - set2
  print("Difference:", difference_set)  # Output: Difference: {1, 2}

  # Symmetric Difference
  sym_diff_set = set1 ^ set2
  print("Symmetric Difference:", sym_diff_set)  # Output: Symmetric Difference: {1, 2, 5, 6}
  ```

  #### Example 3: Iterating Over a Set
  ```python
  fruits = {"apple", "banana", "cherry"}
  for fruit in fruits:
      print(fruit)
  # Output (order may vary):
  # apple
  # banana
  # cherry
  ```

  #### Example 4: Using `frozenset`
  ```python
  # Creating a frozenset
  fs = frozenset([1, 2, 3])
  print(fs)  # Output: frozenset({1, 2, 3})
  
  # Using frozenset as a dictionary key
  my_dict = {fs: "immutable set"}
  print(my_dict[frozenset([1, 2, 3])])  # Output: immutable set
  ```

- **FAQs:**

  **1. What are sets in Python?**  
  Sets in Python are unordered collections of unique elements. They are defined using curly braces `{}` or the `set()` function and are useful for storing distinct items and performing mathematical set operations like union, intersection, and difference.

  **2. How do you perform set operations in Python?**  
  Sets in Python support various operations:
  - **Union:** `set1 | set2` or `set1.union(set2)`
  - **Intersection:** `set1 & set2` or `set1.intersection(set2)`
  - **Difference:** `set1 - set2` or `set1.difference(set2)`
  - **Symmetric Difference:** `set1 ^ set2` or `set1.symmetric_difference(set2)`

  **Example:**
  ```python
  set1 = {1, 2, 3}
  set2 = {3, 4, 5}

  print(set1 | set2)  # Output: {1, 2, 3, 4, 5}
  print(set1 & set2)  # Output: {3}
  print(set1 - set2)  # Output: {1, 2}
  print(set1 ^ set2)  # Output: {1, 2, 4, 5}
  ```

  **3. What is the difference between a set and a tuple in Python?**  
  - **Set:**  
    - **Unordered:** No guaranteed order of elements.
    - **Unique Elements:** Cannot contain duplicates.
    - **Mutable:** Elements can be added or removed.
    - **Defined using `{}` or `set()`.
  
  - **Tuple:**  
    - **Ordered:** Maintains the order of elements.
    - **Can Contain Duplicates:** Elements can repeat.
    - **Immutable:** Cannot be changed after creation.
    - **Defined using `()` or `tuple()`.

  **4. Can you add mutable elements like lists to a set in Python?**  
  No, sets can only contain hashable (immutable) elements. Attempting to add a mutable element like a list will raise a `TypeError`.

  **Example:**
  ```python
  my_set = {1, 2, 3}
  my_set.add([4, 5])  # Raises TypeError: unhashable type: 'list'
  ```

  **5. How do you input a set from the user in Python?**  
  You can use the `input()` function to get user input and then convert it into a set. For example, to read a string of characters separated by spaces and convert them to a set:

  ```python
  # Input a set from user
  input_str = input("Enter elements separated by space: ")
  input_set = set(input_str.split())
  print(input_set)
  ```

  **6. How to find the maximum and minimum elements in a set in Python?**  
  You can use the built-in `max()` and `min()` functions to find the maximum and minimum elements in a set, respectively.

  **Example:**
  ```python
  numbers = {10, 50, 20, 40}
  print("Max:", max(numbers))  # Output: Max: 50
  print("Min:", min(numbers))  # Output: Min: 10
  ```

  **7. How to remove elements from a set in Python?**  
  You can remove elements using methods like `remove()`, `discard()`, and `clear()`.

  **Example:**
  ```python
  my_set = {1, 2, 3, 4, 5}
  
  # Remove an element (raises KeyError if not present)
  my_set.remove(3)
  
  # Discard an element (does not raise an error if not present)
  my_set.discard(10)
  
  # Clear the entire set
  my_set.clear()
  
  print(my_set)  # Output: set()
  ```

  **4. What are frozen sets in Python?**  
  `frozenset` is an immutable version of a set. Once created, you cannot add or remove elements from a `frozenset`. They are hashable and can be used as dictionary keys or elements of other sets.

  **Example:**
  ```python
  fs = frozenset([1, 2, 3])
  print(fs)  # Output: frozenset({1, 2, 3})
  
  # Using frozenset as a dictionary key
  my_dict = {fs: "immutable set"}
  print(my_dict[frozenset([1, 2, 3])])  # Output: immutable set
  ```

  **9. Can sets be nested in Python?**  
  No, sets cannot contain other sets because sets are mutable and unhashable. However, you can include `frozenset` objects within a set.

  **Example:**
  ```python
  # Nested sets using frozenset
  s = {frozenset([1, 2]), frozenset([3, 4])}
  print(s)  # Output: {frozenset({1, 2}), frozenset({3, 4})}
  ```

  **10. How to iterate over a set in Python?**  
  You can iterate over a set using a `for` loop.

  **Example:**
  ```python
  fruits = {"apple", "banana", "cherry"}
  for fruit in fruits:
      print(fruit)
  # Output (order may vary):
  # apple
  # banana
  # cherry
  ```

### 4.2 Frozen Set

- **Description:**  
  Frozen sets in Python are immutable objects that only support methods and operators that produce a result without affecting the frozen set or sets to which they are applied. They are created using the `frozenset()` method. Unlike regular sets, frozen sets cannot have their elements modified after creation, making them suitable for use as keys in dictionaries or elements of other sets.

- **When to Use:**  
  Use frozen sets when:
  - You need an immutable set that can be used as a dictionary key or stored in another set.
  - Ensuring that the set cannot be modified after its creation.
  - Implementing hashable collections that require uniqueness without mutability.

- **Key Patterns:**
  - **Immutable Collections:** Storing unique elements in a collection that should not change.
  - **Dictionary Keys:** Using sets as keys in dictionaries by converting them to frozensets.
  - **Set Operations on Immutable Sets:** Performing set operations while maintaining immutability.

- **LeetCode Problem Types:**
  - **Group Anagrams (Problem #49)**
  - **Top K Frequent Elements (Problem #347)**
  - **Intersection of Two Arrays (Problem #349)**
  - **Two Sum (Problem #1)**
  - **Check if Array is a Subset of Another**
  
- **Python Implementation:**

  ```python
  # Example 1: Creating a Frozen Set
  fs = frozenset([1, 2, 3])
  print(fs)  # Output: frozenset({1, 2, 3})
  
  # Example 2: Using frozenset as a Dictionary Key
  my_dict = {frozenset([1, 2, 3]): "immutable set"}
  print(my_dict[frozenset([1, 2, 3])])  # Output: immutable set
  
  # Example 3: Attempting to Modify a Frozen Set
  fs = frozenset([1, 2, 3])
  try:
      fs.add(4)
  except AttributeError as e:
      print(e)  # Output: 'frozenset' object has no attribute 'add'
  
  # Example 4: Nested Frozen Sets
  nested_fs = {frozenset([1, 2]), frozenset([3, 4])}
  print(nested_fs)  # Output: {frozenset({1, 2}), frozenset({3, 4})}
  ```

- **Time Complexity:**
  - **Creation (`frozenset()`):** O(n), where n is the number of elements.
  - **Membership Test (`in`):** O(1) average
  - **Set Operations (union, intersection, etc.):** O(len(s) + len(t))
  
- **Space Complexity:**  
  O(n), where n is the number of elements in the frozen set.

- **Additional Notes:**
  - **Immutability:** Once created, a frozen set cannot be altered, ensuring the integrity of the data.
  - **Hashable:** Frozen sets are hashable and can be used as keys in dictionaries or elements of other sets.
  - **No Modification Methods:** Methods like `add()`, `remove()`, or `clear()` are not available for frozen sets.

- **Best Practices:**
  - **Use Frozen Sets for Immutable Collections:** When you need a set that should not change throughout the program.
  - **Combine with Dictionaries:** Use frozen sets as keys in dictionaries to map unique sets to values.
  - **Leverage for Nested Sets:** When you need to include sets within other sets, use frozen sets to maintain immutability.

- **Example: Implementing a Dictionary with Frozen Set Keys**

  ```python
  from collections import defaultdict

  # Initialize a dictionary with frozenset keys
  group_dict = defaultdict(list)

  # Sample data: grouping words by their unique character sets
  words = ["eat", "tea", "tan", "ate", "nat", "bat"]
  for word in words:
      key = frozenset(word)
      group_dict[key].append(word)

  # Display grouped words
  for key, group in group_dict.items():
      print(f"Group {key}: {group}")

  # Output:
  # Group frozenset({'e', 'a', 't'}): ['eat', 'tea', 'ate']
  # Group frozenset({'n', 'a', 't'}): ['tan', 'nat']
  # Group frozenset({'b', 'a', 't'}): ['bat']
  ```

  **Explanation:**  
  This example groups words that are anagrams by their unique character sets using frozen sets as keys in a dictionary.

### 4.3 Set Operations in Python

- **Description:**  
  Python sets support various operations that allow you to perform mathematical set operations such as union, intersection, difference, and symmetric difference. These operations are highly efficient due to the underlying hash table implementation of sets.

- **When to Use:**  
  Use set operations when you need to:
  - Combine multiple sets of unique elements.
  - Find common elements between sets.
  - Determine elements present in one set but not in another.
  - Identify elements that are unique to each set.

- **Key Patterns:**
  - **Union of Sets:** Combining all unique elements from multiple sets.
  - **Intersection of Sets:** Finding common elements between sets.
  - **Difference of Sets:** Identifying elements present in one set but not in another.
  - **Symmetric Difference of Sets:** Finding elements that are in either of the sets but not in both.

- **LeetCode Problem Types:**
  - **Union of Two Arrays**
  - **Intersection of Two Arrays**
  - **Find the Duplicate Number (Problem #287)**
  - **Check if Array is a Subset of Another**
  - **Distinct Elements in an Array**

- **Python Implementation:**

  ### Union Operation

  ```python
  # Union using union() function
  people = {"Jay", "Idrish", "Archil"}
  vampires = {"Karan", "Arjun"}
  dracula = {"Deepanshu", "Raju"}

  population = people.union(vampires)
  print("Union using union() function")
  print(population)
  # Output: {'Idrish', 'Arjun', 'Jay', 'Karan', 'Archil'}

  # Union using '|' operator
  population = people | dracula
  print("\nUnion using '|' operator")
  print(population)
  # Output: {'Idrish', 'Deepanshu', 'Raju', 'Jay', 'Archil'}
  ```

  ### Intersection Operation

  ```python
  # Intersection using intersection() function
  set1 = set()
  set2 = set()

  for i in range(5):
      set1.add(i)

  for i in range(3, 9):
      set2.add(i)

  set3 = set1.intersection(set2)
  print("Intersection using intersection() function")
  print(set3)
  # Output: {3, 4}

  # Intersection using '&' operator
  set3 = set1 & set2
  print("\nIntersection using '&' operator")
  print(set3)
  # Output: {3, 4}
  ```

  ### Difference Operation

  ```python
  # Difference using difference() function
  set1 = set()
  set2 = set()

  for i in range(5):
      set1.add(i)

  for i in range(3, 9):
      set2.add(i)

  set3 = set1.difference(set2)
  print("Difference of two sets using difference() function")
  print(set3)
  # Output: {0, 1, 2}

  # Difference using '-' operator
  set3 = set1 - set2
  print("\nDifference of two sets using '-' operator")
  print(set3)
  # Output: {0, 1, 2}
  ```

  ### Symmetric Difference Operation

  ```python
  set1 = {1, 2, 3, 4}
  set2 = {3, 4, 5, 6}

  # Symmetric Difference using symmetric_difference() function
  sym_diff = set1.symmetric_difference(set2)
  print("Symmetric Difference using symmetric_difference() function")
  print(sym_diff)
  # Output: {1, 2, 5, 6}

  # Symmetric Difference using '^' operator
  sym_diff = set1 ^ set2
  print("\nSymmetric Difference using '^' operator")
  print(sym_diff)
  # Output: {1, 2, 5, 6}
  ```

### 4.4 Adding and Removing Elements in Python Sets

- **Description:**  
  Adding and removing elements in Python sets can be done using methods like `add()`, `remove()`, `discard()`, `update()`, and `clear()`. These operations allow you to dynamically modify the contents of a set.

- **When to Use:**  
  Use these methods when you need to:
  - Add new unique elements to a set.
  - Remove existing elements from a set.
  - Update a set with multiple elements.
  - Clear all elements from a set.

- **Key Patterns:**
  - **Dynamic Modification:** Adding or removing elements based on conditions.
  - **Updating Sets:** Combining multiple elements into a set efficiently.
  - **Clearing Sets:** Resetting a set to empty when needed.

- **LeetCode Problem Types:**
  - **Distinct Elements in an Array**
  - **Check Pair with Target Sum**
  - **Duplicate within K Distance**
  - **Find the Duplicate Number (Problem #287)**
  - **Check if Array is a Subset of Another**

- **Python Implementation:**

  ### Adding Elements

  ```python
  # Adding elements to a set
  people = {"Jay", "Idrish", "Archil"}
  print("Initial set")
  print(people)
  # Output: {'Idrish', 'Archil', 'Jay'}

  # Adding a single element
  people.add("Daxit")
  
  # Adding multiple elements using a loop
  for i in range(1, 6):
      people.add(i)
  
  print("\nSet after adding elements:")
  print(people)
  # Output: {1, 2, 3, 4, 5, 'Daxit', 'Archil', 'Jay', 'Idrish'}
  ```

  ### Removing Elements

  ```python
  # Removing elements from a set
  my_set = {1, 2, 3, 4, 5, 6}

  print("Initial set:")
  print(my_set)
  # Output: {1, 2, 3, 4, 5, 6}

  # Removing an element using remove()
  my_set.remove(3)
  print("\nSet after removing 3:")
  print(my_set)
  # Output: {1, 2, 4, 5, 6}

  # Removing an element using discard() (no error if element not present)
  my_set.discard(10)
  print("\nSet after discarding 10 (no error):")
  print(my_set)
  # Output: {1, 2, 4, 5, 6}

  # Clearing the set
  my_set.clear()
  print("\nSet after clearing:")
  print(my_set)
  # Output: set()
  ```

### 4.5 Heterogeneous Elements in Python Sets

- **Description:**  
  Python sets can store heterogeneous elements, meaning a set can contain a mixture of different data types such as strings, integers, booleans, etc.

- **When to Use:**  
  Use when you need a collection of unique elements of various data types.

- **Python Implementation:**

  ```python
  # Python example demonstrating that a set can store heterogeneous elements
  s = {"Geeks", "for", 10, 52.7, True}
  print(s)  # Output: {True, 'for', 'Geeks', 10, 52.7}
  ```

  **Explanation:**  
  The set `s` contains a mix of strings, integers, a float, and a boolean. Sets handle heterogeneous data types seamlessly as long as the elements are hashable.

### 4.6 Python Frozen Sets

- **Description:**  
  Frozen sets in Python are immutable objects that only support methods and operators that produce a result without affecting the frozen set or sets to which they are applied. They are created using the `frozenset()` method. Unlike regular sets, frozen sets cannot have their elements modified after creation.

- **When to Use:**  
  Use frozen sets when:
  - You need an immutable set that can be used as a dictionary key or stored in another set.
  - Ensuring that the set cannot be modified after its creation.
  - Implementing hashable collections that require uniqueness without mutability.

- **Key Patterns:**
  - **Immutable Collections:** Storing unique elements in a collection that should not change.
  - **Dictionary Keys:** Using sets as keys in dictionaries by converting them to frozensets.
  - **Set Operations on Immutable Sets:** Performing set operations while maintaining immutability.

- **LeetCode Problem Types:**
  - **Group Anagrams (Problem #49)**
  - **Top K Frequent Elements (Problem #347)**
  - **Intersection of Two Arrays (Problem #349)**
  - **Two Sum (Problem #1)**
  - **Check if Array is a Subset of Another**
  
- **Python Implementation:**

  ```python
  from collections import OrderedDict

  # Example 1: Basic Usage of OrderedDict
  print("Example 1: Basic OrderedDict")
  od = OrderedDict()
  od['a'] = 1
  od['b'] = 2
  od['c'] = 3
  od['d'] = 4

  for key, value in od.items():
      print(key, value)
  # Output:
  # a 1
  # b 2
  # c 3
  # d 4

  # Example 2: Changing Value of a Key
  print("\nExample 2: Changing Value of a Key")
  od['c'] = 5
  for key, value in od.items():
      print(key, value)
  # Output:
  # a 1
  # b 2
  # c 5
  # d 4

  # Example 3: Equality Comparison
  print("\nExample 3: Equality Comparison")
  od1 = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
  od2 = OrderedDict([('c', 3), ('b', 2), ('a', 1)])
  print(od1 == od2)  # Output: False

  # Example 4: Reversing an OrderedDict
  print("\nExample 4: Reversing OrderedDict")
  reversed_od = OrderedDict(reversed(list(od.items())))
  for key, value in reversed_od.items():
      print(key, value)
  # Output:
  # d 4
  # c 5
  # b 2
  # a 1

  # Example 5: Using popitem()
  print("\nExample 5: Using popitem()")
  last_item = od.popitem(last=True)
  print("Popped Item:", last_item)  # Output: ('d', 4)
  for key, value in od.items():
      print(key, value)
  # Output:
  # a 1
  # b 2
  # c 5

  # Example 6: Moving Keys to End or Beginning
  print("\nExample 6: Moving Keys")
  od.move_to_end('a')  # Move 'a' to the end
  od.move_to_end('b', last=False)  # Move 'b' to the beginning
  for key, value in od.items():
      print(key, value)
  # Output:
  # b 2
  # c 5
  # a 1
  ```

  **Explanation:**  
  This example demonstrates various `OrderedDict` operations, which are useful for maintaining the order of elements. Although Python 3.7+ dictionaries maintain insertion order by default, `OrderedDict` provides additional methods like `move_to_end()` and `popitem()` for more controlled ordering.

### 4.7 Internal Working of Sets

- **Description:**  
  Sets in Python are implemented using a hash table. This allows for efficient storage and retrieval of elements, ensuring that operations like search, insert, and delete can be performed in constant time on average.

- **When to Use:**  
  Use when:
  - You need fast membership testing.
  - You require uniqueness of elements.
  - Performing frequent insertions and deletions.

- **Key Patterns:**
  - **Hashing:** Utilizing hash functions to map elements to indices in the hash table.
  - **Handling Collisions:** Implementing collision resolution strategies like chaining (linked lists) when multiple elements hash to the same index.

- **Python Implementation:**

  ### Adding Elements to Python Sets

  ```python
  # Python program to demonstrate adding elements in a set

  # Creating a Set
  people = {"Jay", "Idrish", "Archil"}
  print("People:", end = " ")
  print(people)
  # Output: People: {'Idrish', 'Archil', 'Jay'}

  # This will add 'Daxit' to the set
  people.add("Daxit")

  # Adding elements to the set using a loop
  for i in range(1, 6):
      people.add(i)

  print("\nSet after adding elements:", end = " ")
  print(people)
  # Output: Set after adding elements: {1, 2, 3, 4, 5, 'Daxit', 'Archil', 'Jay', 'Idrish'}
  ```

  **Explanation:**  
  This example shows how to add single and multiple elements to a set using the `add()` method and a loop. The set automatically ensures that all elements remain unique.

### 4.8 Time Complexity of Sets

- **Description:**  
  Understanding the time complexity of various set operations is crucial for writing efficient Python code, especially in competitive programming and performance-critical applications.

- **Time Complexity Table:**

  | Operation                    | Average Case       | Worst Case          | Notes                                                      |
  |------------------------------|---------------------|---------------------|------------------------------------------------------------|
  | `x in s`                     | O(1)                | O(n)                | Membership test                                            |
  | `s | t` (Union)               | O(len(s) + len(t))  | O(len(s) + len(t))    | Combining all unique elements from both sets              |
  | `s & t` (Intersection)        | O(min(len(s), len(t))) | O(len(s) * len(t)) | Finding common elements                                   |
  | `s - t` (Difference)          | O(len(s))           | O(len(s))            | Elements in s not in t                                     |
  | `s ^ t` (Symmetric Difference)| O(len(s) + len(t))  | O(len(s) + len(t))    | Elements in either s or t but not in both                  |
  | `add(x)`                     | O(1)                | O(n)                | Adding an element                                          |
  | `remove(x)`                  | O(1)                | O(n)                | Removing an element (raises KeyError if not present)      |
  | `discard(x)`                 | O(1)                | O(n)                | Removing an element (does not raise an error if absent)    |
  | `clear()`                    | O(n)                | O(n)                | Removing all elements from the set                         |
  | `copy()`                     | O(n)                | O(n)                | Creating a shallow copy of the set                          |
  | `update(iterable)`           | O(k)                | O(k)                | Adding multiple elements from an iterable to the set        |
  | `intersection_update(t)`     | O(len(t))           | O(len(t))            | Updating the set with the intersection of itself and t       |
  | `difference_update(t)`       | O(len(t))           | O(len(t))            | Updating the set by removing elements found in t             |
  | `symmetric_difference_update(t)` | O(len(t))        | O(len(t))            | Updating the set with the symmetric difference of itself and t|

- **Space Complexity:**  
  O(n), where n is the number of elements in the set.

### 4.9 Problems Based on Sets

- **Description:**  
  Sets are versatile and can be applied to a wide range of problems that involve uniqueness, membership testing, and set operations. Below are some common problem types where sets are particularly useful.

- **Problem Types:**
  - **Distinct Elements in an Array:** Find the number of unique elements.
  - **Union of Two Arrays:** Combine elements from two arrays without duplicates.
  - **Intersection of Two Arrays:** Find common elements between two arrays.
  - **Repeating Elements:** Identify elements that appear multiple times.
  - **Check if an Array is a Subset of Another:** Determine if all elements of one array are present in another.
  - **Check Pair with Target Sum:** Find if any pair of elements sums up to a target value.
  - **Check for Disjoint Sets:** Verify if two sets have no elements in common.
  - **Duplicate within K Distance:** Check if duplicates are within a certain distance from each other.
  - **Longest Consecutive Sequence:** Find the length of the longest sequence of consecutive numbers.
  - **Find Two Numbers that Add Up to a Target (Two Sum):** Identify two numbers that sum up to a specific target.

### 4.10 Clearing Python Sets

- **Description:**  
  The `clear()` method in Python sets removes all elements from the set, resulting in an empty set.

- **When to Use:**  
  Use when you need to reset a set to an empty state without creating a new set.

- **Python Implementation:**

  ```python
  # Python program to demonstrate clearing a set

  set1 = {1, 2, 3, 4, 5, 6}
  
  print("Initial set")
  print(set1)
  # Output: Initial set
  # {1, 2, 3, 4, 5, 6}
  
  # This method will remove all elements of the set
  set1.clear()
  
  print("\nSet after using clear() function")
  print(set1)
  # Output:
  # Set after using clear() function
  # set()
  ```

  **Explanation:**  
  The `clear()` method removes all elements from `set1`, leaving it empty.

### 4.11 Pitfalls of Python Sets

- **Description:**  
  While sets are powerful and efficient, there are some pitfalls to be aware of when using them in Python.

- **Pitfalls:**
  - **No Specific Order:**  
    Sets do not maintain elements in any particular order, which means you cannot rely on the order of elements when iterating over a set.
  
  - **Only Immutable Elements:**  
    Only instances of immutable types (e.g., strings, numbers, tuples) can be added to a set. Mutable types like lists or dictionaries cannot be added and will raise a `TypeError`.

- **Example:**
  
  ```python
  # Attempting to add a mutable element to a set
  try:
      my_set = {1, 2, 3}
      my_set.add([4, 5])  # This will raise a TypeError
  except TypeError as e:
      print(e)  # Output: unhashable type: 'list'
  ```

  **Explanation:**  
  The above code attempts to add a list to a set, which is not allowed because lists are mutable and unhashable.

Python sets are an essential data structure for handling collections of unique elements with efficient operations. Understanding their properties, operations, and potential pitfalls can help you leverage sets effectively in your programming tasks, especially in competitive programming and data analysis scenarios.

By utilizing sets and their various methods, you can perform complex data manipulations with ease and efficiency, making sets a powerful tool in your Python toolkit.

## 5. Stacks (Using list or deque)

	•	Description: A stack follows the Last In, First Out (LIFO) principle. It is useful for maintaining the state of operations.
	•	When to Use: Use when you need to handle matching pairs (e.g., parentheses), backtracking, or reversing order.
	•	Key Patterns:
	•	Parentheses matching.
	•	Reversing sequences.
	•	Backtracking.
	•	LeetCode Problem Types:
	•	Valid Parentheses (Problem #20)
	•	Daily Temperatures (Problem #739)

Python Implementation:

stack = []
stack.append(1)  # Push
stack.pop()      # Pop

Time Complexity:

	•	Push/Pop: O(1)

## 6. Queues 

### 6.1 Queue (Using `collections.deque`)

- **Description:**  
  A queue follows the First In, First Out (FIFO) principle. It is used when processing elements in the order they arrive.

- **When to Use:**  
  Ideal for problems involving breadth-first search (BFS), task scheduling, or any scenario requiring processing in the order of arrival.

- **Key Patterns:**
  - **BFS Traversal:** Processing nodes level by level in a graph or tree.
  - **Order-Preserving Task Scheduling:** Managing tasks in the order they are received.

- **LeetCode Problem Types:**
  - **Binary Tree Level Order Traversal (Problem #102)**
  - **Sliding Window Maximum (Problem #239)**

- **Python Implementation:**

  ```python
  from collections import deque
  queue = deque()
  queue.append(1)       # Enqueue
  queue.popleft()       # Dequeue
  ```

- **Time Complexity:**
  
  - **Enqueue/Dequeue:** O(1)

- **Space Complexity:**  
  O(n), where n is the number of elements in the queue.

- **Additional Notes:**
  
  - **Efficient Operations:** `deque` allows for O(1) time complexity for both appending and popping elements from either end, making it ideal for implementing queues.
  
  - **Double-Ended Nature:** While primarily used as a FIFO queue, `deque` can also function as a LIFO stack if needed.

- **Best Practices:**
  
  - **Use `deque` for Implementing Queues:** It provides efficient O(1) time complexity for append and popleft operations, unlike lists which have O(n) time complexity for popping from the front.
  
  - **Avoid Using Lists for Queue Operations:** Lists are not optimized for queue operations as popping from the front is inefficient.

- **Example: BFS Traversal of a Binary Tree**

  ```python
  from collections import deque

  class TreeNode:
      def __init__(self, val=0, left=None, right=None):
          self.val = val
          self.left = left
          self.right = right

  def bfs(root):
      if not root:
          return
      queue = deque([root])
      while queue:
          node = queue.popleft()
          print(node.val)
          if node.left:
              queue.append(node.left)
          if node.right:
              queue.append(node.right)

  # Usage
  # Creating a simple binary tree:
  #     1
  #    / \
  #   2   3
  root = TreeNode(1, TreeNode(2), TreeNode(3))
  bfs(root)
  # Output:
  # 1
  # 2
  # 3
  ```

### 6.2 Deque (Double-Ended Queue using `collections.deque`)

- **Description:**  
  A deque (double-ended queue) supports adding and removing elements from both ends efficiently. Unlike regular queues that operate on FIFO (First In, First Out) principles, a deque allows for both FIFO and LIFO (Last In, First Out) operations, providing greater flexibility in data manipulation.

- **When to Use:**  
  Use in problems involving sliding windows or managing sequences from both ends.

- **Key Patterns:**
  - **Sliding Window Problems:** Maintaining a window of elements with specific properties, such as finding the maximum in a sliding window.
  - **Maintaining Monotonic Sequences:** Keeping track of elements in a specific order to optimize certain operations.

- **LeetCode Problem Types:**
  - **Sliding Window Maximum (Problem #239)**

- **Python Implementation:**

  ```python
  from collections import deque
  dq = deque()
  dq.append(1)
  dq.appendleft(2)
  dq.pop()
  dq.popleft()
  ```

- **Time Complexity:**
  
  - **Append/Pop:** O(1)

- **Space Complexity:**  
  O(n), where n is the number of elements in the deque.

- **Additional Notes:**
  
  - **Versatile Operations:** `deque` provides methods like `append`, `appendleft`, `pop`, `popleft`, `extend`, `extendleft`, `remove`, `rotate`, `clear`, `count`, `index`, and `reverse`, allowing versatile operations on both ends.
  
  - **Doubly-Linked List Implementation:** `deque` is implemented as a doubly-linked list, ensuring constant time operations at both ends.

- **Best Practices:**
  
  - **Choose `deque` Over `list` for Deque Operations:** It provides O(1) time complexity for append and pop operations on both ends, making it more efficient than lists for these use cases.
  
  - **Leverage `rotate()` for Cyclic Operations:** Use the `rotate()` method to perform cyclic shifts of elements within the deque.
  
  - **Maintain Monotonic Deque for Sliding Window Problems:** When solving sliding window maximum problems, maintaining a monotonic deque can help in efficiently finding the maximum element.
  
  - **Avoid Using Lists for Double-Ended Queue Operations:** Lists have O(n) time complexity for insertions and deletions from the front, making `deque` a better choice for double-ended operations.

- **Example: Sliding Window Maximum**

  ```python
  from collections import deque

  def maxSlidingWindow(nums, k):
      if not nums or k == 0:
          return []
      dq = deque()
      result = []
      for i in range(len(nums)):
          # Remove elements outside the current window
          while dq and dq[0] < i - k + 1:
              dq.popleft()
          # Remove smaller elements in the deque
          while dq and nums[dq[-1]] < nums[i]:
              dq.pop()
          # Add the current element's index to the deque
          dq.append(i)
          # Append the current max to the result
          if i >= k - 1:
              result.append(nums[dq[0]])
      return result

  # Usage
  nums = [1,3,-1,-3,5,3,6,7]
  k = 3
  print(maxSlidingWindow(nums, k))  # Output: [3,3,5,5,6,7]
  ```

  **Explanation:**

  This function finds the maximum in each sliding window of size `k` using a deque to store indices of potential maximum elements, ensuring O(n) time complexity.

- **Operations on `deque`:**

  Here’s a table listing built-in operations of a `deque` in Python with descriptions and their corresponding time complexities:

  | Operation          | Description                                                            | Time Complexity |
  |--------------------|------------------------------------------------------------------------|------------------|
  | `append(x)`        | Adds x to the right end of the deque.                                  | O(1)             |
  | `appendleft(x)`    | Adds x to the left end of the deque.                                   | O(1)             |
  | `pop()`            | Removes and returns an element from the right end of the deque.        | O(1)             |
  | `popleft()`        | Removes and returns an element from the left end of the deque.         | O(1)             |
  | `extend(iterable)` | Adds all elements from iterable to the right end of the deque.         | O(k)             |
  | `extendleft(iterable)` | Adds all elements from iterable to the left end of the deque (reversed order). | O(k) |
  | `remove(value)`    | Removes the first occurrence of value from the deque. Raises `ValueError` if not found. | O(n) |
  | `rotate(n)`        | Rotates the deque n steps to the right. If n is negative, rotates to the left. | O(k) |
  | `clear()`          | Removes all elements from the deque.                                  | O(n)             |
  | `count(value)`     | Counts the number of occurrences of value in the deque.                | O(n)             |
  | `index(value)`     | Returns the index of the first occurrence of value in the deque. Raises `ValueError` if not found. | O(n) |
  | `reverse()`        | Reverses the elements of the deque in place.                          | O(n)             |

- **Best Practices:**
  
  - **Choose `deque` Over `list` for Queues and Stacks:** `deque` provides O(1) time complexity for append and pop operations on both ends, making it more efficient than lists for these use cases.
  
  - **Use `appendleft()` and `popleft()` for FIFO Queues:** When implementing FIFO queues, use `append()` to enqueue and `popleft()` to dequeue elements.
  
  - **Use `append()` and `pop()` for LIFO Stacks:** For stack operations, use `append()` to push and `pop()` to remove elements from the end.
  
  - **Leverage `rotate()` for Cyclic Operations:** Use the `rotate()` method for operations requiring cyclic shifts of elements within the deque.
  
  - **Maintain Monotonic Deque for Sliding Window Problems:** When solving sliding window maximum problems, maintaining a monotonic deque can help in efficiently finding the maximum element.

- **Deque in Python – FAQs**

  **1. Why use `deque` instead of `list` in Python?**  
  `deque` (double-ended queue) in Python, from the `collections` module, provides optimized operations for appending and popping elements from both ends of the sequence. Compared to `list`, which provides constant time complexity for append operations (amortized O(1)), `deque` offers consistent O(1) time complexity for append and pop operations from both ends. This makes `deque` suitable for scenarios where efficient appends and pops are required from both ends of the sequence, such as implementing queues and stacks.

  **2. Is `deque` better than `queue` in Python?**  
  In Python, `queue` is a module that provides different types of queues like `Queue`, `LifoQueue`, and `PriorityQueue`, built on top of `deque` or `list`. `deque` itself is not better or worse than `queue`, but rather serves as a fundamental component that can be used to implement efficient queues (`Queue`), stacks (`LifoQueue`), and double-ended queues (`deque`) depending on the use case.

  **3. Why is `deque` faster than `queue`?**  
  `deque` itself is not faster than `queue` because `deque` is often used as the underlying data structure to implement queues (`Queue`), stacks (`LifoQueue`), and double-ended queues (`deque`) in Python. The efficiency of operations (such as append and pop) depends on the specific implementation and usage context rather than `deque` being inherently faster than `queue`.

  **4. Why is `deque` faster than a stack?**  
  `deque` is not necessarily faster than a stack (`LifoQueue`) because both can be implemented using `deque` as the underlying data structure. However, if comparing `deque` to a straightforward list-based stack implementation (list used as a stack), `deque` may offer faster performance for pop and append operations due to its optimized internals for these operations.

  **5. What are the two types of deque?**  
  In Python’s `collections` module, there are two primary types of deque:
  - `deque`: A general-purpose double-ended queue.
  - `deque(maxlen=N)`: A bounded deque that restricts the maximum number of elements (N) it can hold. When new items are added and the deque is full, the oldest items are automatically removed to accommodate the new items.

  **6. What is the difference between a simple queue and deque?**  
  A simple queue, such as those implemented using `queue.Queue` in Python, typically refers to a FIFO (First-In-First-Out) data structure where elements are inserted at the rear and removed from the front. `deque`, on the other hand, supports efficient insertion and deletion operations from both ends (front and rear) of the queue. It can function as a double-ended queue (`collections.deque`) or as a general-purpose data structure that can mimic a FIFO queue (`queue.Queue`) or LIFO stack (`queue.LifoQueue`) depending on how it’s used.

By understanding and utilizing queues and deques through the `collections.deque` module, you can efficiently manage ordered and flexible data sequences in various algorithmic scenarios, making them powerful tools for competitive programming and data processing tasks.

## 7. Heaps (Using `heapq`)

### 7.1 Min Heap (Priority Queue)

- **Description:**  
  A priority queue is a data structure that allows elements to be inserted and removed based on their priority. In Python, the `heapq` module implements a priority queue using a min-heap by default. A min-heap is a binary heap where the smallest element is always at the root, enabling efficient access to the minimum element. The `heapq` module allows treating a list as a heap, providing efficient methods for adding and removing elements while maintaining the heap property.

- **When to Use:**  
  Use a priority queue when:
  - You need to dynamically extract the minimum (or maximum) element.
  - Implementing algorithms like Dijkstra’s or Prim’s that rely on efficient priority-based operations.
  - Managing tasks that need to be processed based on priority.
  - Solving problems that require the k-th smallest or largest element.

- **Key Patterns:**
  - **Kth Smallest or Largest Element:** Efficiently finding the k-th smallest or largest element in a dataset.
  - **Greedy Algorithms:** Many greedy strategies utilize priority queues to make optimal choices at each step.
  - **Real-Time Stream of Data:** Handling streaming data where elements are continuously added and removed based on priority.
  - **Event Simulation:** Managing events that need to be processed in a specific order based on time or priority.
  - **Task Scheduling:** Scheduling tasks based on their urgency or importance.

- **LeetCode Problem Types:**
  - **Kth Largest Element in an Array (Problem #215)**
  - **Merge K Sorted Lists (Problem #23)**
  - **Top K Frequent Elements (Problem #347)**
  - **Find Median from Data Stream (Problem #295)**
  - **Smallest Range Covering Elements from K Lists (Problem #632)**
  - **Rearrange Characters to Make Target String (Problem #2287)**

- **Python Implementation:**

  ```python
  import heapq

  # Example 1: Basic Min Heap Operations
  print("Example 1: Basic Min Heap Operations")
  min_heap = []
  heapq.heappush(min_heap, 3)
  heapq.heappush(min_heap, 1)
  heapq.heappush(min_heap, 4)
  heapq.heappush(min_heap, 2)
  print("Min Heap:", min_heap)
  # Output: Min Heap: [1, 2, 4, 3]

  min_element = heapq.heappop(min_heap)  # Extract min
  print("Popped Min Element:", min_element)
  print("Heap after popping:", min_heap)
  # Output:
  # Popped Min Element: 1
  # Heap after popping: [2, 3, 4]

  # Example 2: Heapify an Existing List
  print("\nExample 2: Heapify an Existing List")
  li = [10, 20, 15, 30, 40]
  heapq.heapify(li)
  print("Heapified List:", li)
  # Output: Heapified List: [10, 20, 15, 30, 40]

  # Example 3: Using heappushpop()
  print("\nExample 3: Using heappushpop()")
  h = [10, 20, 15, 30, 40]
  heapq.heapify(h)
  popped = heapq.heappushpop(h, 5)
  print("Pushed 5 and Popped:", popped)
  print("Heap after heappushpop:", h)
  # Output:
  # Pushed 5 and Popped: 5
  # Heap after heappushpop: [10, 20, 15, 30, 40]

  # Example 4: Finding the 3 Smallest Elements
  print("\nExample 4: Finding the 3 Smallest Elements")
  h = [10, 20, 15, 30, 40]
  heapq.heapify(h)
  smallest = heapq.nsmallest(3, h)
  print("3 Smallest Elements:", smallest)
  # Output: 3 Smallest Elements: [10, 15, 20]

  # Example 5: Finding the 3 Largest Elements
  print("\nExample 5: Finding the 3 Largest Elements")
  h = [10, 20, 15, 30, 40]
  largest = heapq.nlargest(3, h)
  print("3 Largest Elements:", largest)
  # Output: 3 Largest Elements: [40, 30, 20]

  # Example 6: Merging Two Heaps
  print("\nExample 6: Merging Two Heaps")
  h1 = [10, 20, 15, 30, 40]
  h2 = [5, 7, 3, 8]
  merged = list(heapq.merge(h1, h2))
  print("Merged Heap:", merged)
  # Output: Merged Heap: [3, 5, 7, 8, 10, 15, 20, 30, 40]
  ```

- **Time Complexity:**
  
  - **Insert (`heappush`):** O(log n)
  - **Pop (`heappop`):** O(log n)
  - **Push and Pop (`heappushpop`):** O(log n)
  - **Heapify (`heapify`):** O(n)
  - **Find k Smallest/Largest (`nsmallest`/`nlargest`):** O(n log k), where k is the number of elements to find
  - **Merge (`merge`):** O(n log k), where k is the number of iterables being merged

- **Space Complexity:**  
  O(n), where n is the number of elements in the heap.

- **Additional Notes:**
  
  - **Heap Invariants:**  
    The heap property must be maintained after each operation. In a min-heap, each parent node is less than or equal to its child nodes.
  
  - **Heap as a List:**  
    Python's `heapq` module uses a regular list to implement the heap. The smallest element is always at index 0.
  
  - **Negative Values for Max Heap:**  
    Since `heapq` only supports min-heaps, you can simulate a max-heap by pushing negative values.

- **Best Practices:**
  
  - **Use `heapq` for Efficient Priority Queues:**  
    Utilize the `heapq` module for implementing priority queues where quick access to the smallest element is required.
  
  - **Simulate Max Heaps Using Negative Values:**  
    To implement a max-heap, store negative values in the heap. This allows the largest original values to be treated as the smallest in the min-heap.
  
  - **Avoid Using Heaps for Unsorted Data Retrieval:**  
    Heaps are optimized for access to the smallest (or largest) element. If you need to retrieve all elements in sorted order, consider sorting the list instead.
  
  - **Leverage Built-in Heap Functions:**  
    Utilize functions like `heapify()`, `heappush()`, `heappop()`, `heappushpop()`, `nlargest()`, and `nsmallest()` for efficient heap operations.
  
  - **Use Heaps for Real-Time Data Streams:**  
    Heaps are ideal for managing real-time data where elements are continuously added and the minimum or maximum needs to be accessed efficiently.

- **Example: Managing a Stream of Integers to Find the Kth Largest Element**

  ```python
  import heapq

  class KthLargest:
      def __init__(self, k, nums):
          self.k = k
          self.min_heap = nums
          heapq.heapify(self.min_heap)
          while len(self.min_heap) > k:
              heapq.heappop(self.min_heap)

      def add(self, val):
          if len(self.min_heap) < self.k:
              heapq.heappush(self.min_heap, val)
          elif val > self.min_heap[0]:
              heapq.heappushpop(self.min_heap, val)
          return self.min_heap[0]

  # Usage
  kthLargest = KthLargest(3, [4, 5, 8, 2])
  print(kthLargest.add(3))  # returns 4
  print(kthLargest.add(5))  # returns 5
  print(kthLargest.add(10)) # returns 5
  print(kthLargest.add(9))  # returns 8
  print(kthLargest.add(4))  # returns 8
  ```

  **Explanation:**  
  This class maintains a min-heap of size `k` to keep track of the k-th largest element in a stream of integers. When a new value is added:
  - If the heap has fewer than `k` elements, the value is pushed onto the heap.
  - If the value is larger than the smallest element in the heap, it replaces the smallest element.
  - The smallest element in the heap is always the k-th largest element.

  This ensures that the `add` method operates in O(log k) time, maintaining efficiency even with large streams of data.

### 7.2 Max Heap (Reverse Priority Queue)

- **Description:**  
  Python’s `heapq` module only supports min-heaps, where the smallest element is always at the root. However, you can simulate a max-heap by pushing the negative of each value onto the heap. This inversion allows the largest original values to be treated as the smallest in the min-heap, effectively creating a max-heap. This technique enables efficient extraction of the maximum element while leveraging the `heapq` module's optimized heap operations.

- **When to Use:**  
  Use a max heap when:
  - You need to dynamically extract the maximum element.
  - Implementing algorithms that require frequent access to the largest element.
  - Managing tasks that prioritize higher values over lower ones.
  - Solving problems that involve finding the k-th largest element efficiently.

- **Key Patterns:**
  - **Extracting the Largest Element:** Efficiently retrieving the largest element from a dynamic dataset.
  - **Managing Large Data Streams:** Handling streaming data where the largest elements need to be tracked continuously.
  - **Top K Elements:** Finding the top k largest elements in a dataset.
  - **Greedy Algorithms:** Many greedy strategies require access to the largest elements first.
  - **Scheduling Tasks:** Prioritizing tasks based on their importance or urgency.

- **LeetCode Problem Types:**
  - **K Closest Points to Origin (Problem #973)**
  - **Sliding Window Maximum (Problem #239)**
  - **Top K Frequent Elements (Problem #347)**
  - **Merge K Sorted Lists (Problem #23)**
  - **Find Median from Data Stream (Problem #295)**
  - **Task Scheduler (Problem #621)**

- **Python Implementation:**

  ```python
  import heapq

  # Example 1: Simulating a Max Heap by Pushing Negative Values
  print("Example 1: Simulating a Max Heap by Pushing Negative Values")
  max_heap = []
  heapq.heappush(max_heap, -3)
  heapq.heappush(max_heap, -1)
  heapq.heappush(max_heap, -4)
  heapq.heappush(max_heap, -2)
  print("Max Heap (as negatives):", max_heap)
  # Output: Max Heap (as negatives): [-4, -2, -3, -1]

  max_element = -heapq.heappop(max_heap)  # Extract max
  print("Popped Max Element:", max_element)
  print("Heap after popping:", max_heap)
  # Output:
  # Popped Max Element: 4
  # Heap after popping: [-3, -2, -1]

  # Example 2: Heapify with Negative Values for Max Heap
  print("\nExample 2: Heapify with Negative Values for Max Heap")
  li = [10, 20, 15, 30, 40]
  max_heap = [-x for x in li]
  heapq.heapify(max_heap)
  print("Heapified Max Heap (as negatives):", max_heap)
  # Output: Heapified Max Heap (as negatives): [-40, -30, -15, -10, -20]

  # Example 3: Using heappushpop() for Max Heap
  print("\nExample 3: Using heappushpop() for Max Heap")
  h = [-10, -20, -15, -30, -40]
  heapq.heapify(h)
  popped = heapq.heappushpop(h, -5)  # Push -5 and pop the smallest (which is -40)
  print("Pushed -5 and Popped:", -popped)
  print("Heap after heappushpop:", h)
  # Output:
  # Pushed -5 and Popped: 40
  # Heap after heappushpop: [-30, -20, -15, -10, -5]

  # Example 4: Finding the 3 Largest Elements Using a Max Heap
  print("\nExample 4: Finding the 3 Largest Elements Using a Max Heap")
  h = [10, 20, 15, 30, 40]
  max_heap = [-x for x in h]
  heapq.heapify(max_heap)
  largest_three = [-heapq.heappop(max_heap) for _ in range(3)]
  print("3 Largest Elements:", largest_three)
  # Output: 3 Largest Elements: [40, 30, 20]

  # Example 5: Finding the Top K Frequent Elements Using a Max Heap
  print("\nExample 5: Finding the Top K Frequent Elements Using a Max Heap")
  from collections import Counter

  data = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
  counter = Counter(data)
  max_heap = [(-count, item) for item, count in counter.items()]
  heapq.heapify(max_heap)
  top_k = [heapq.heappop(max_heap)[1] for _ in range(2)]
  print("Top 2 Frequent Elements:", top_k)
  # Output: Top 2 Frequent Elements: ['apple', 'banana']
  ```

  ```python
  # Example 6: Merging Two Max Heaps
  import heapq

  print("\nExample 6: Merging Two Max Heaps")
  h1 = [10, 20, 15, 30, 40]
  h2 = [5, 7, 3, 8]

  # Convert to max heaps by negating the values
  max_heap1 = [-x for x in h1]
  max_heap2 = [-x for x in h2]
  heapq.heapify(max_heap1)
  heapq.heapify(max_heap2)

  # Merge the two max heaps
  merged_heap = max_heap1 + max_heap2
  heapq.heapify(merged_heap)
  merged = [-x for x in merged_heap]
  print("Merged Max Heap:", merged)
  # Output: Merged Max Heap: [40, 30, 15, 20, 10, 8, 7, 5, 3]
  ```

- **Time Complexity:**
  
  - **Insert (`heappush`):** O(log n)
  - **Pop (`heappop`):** O(log n)
  - **Push and Pop (`heappushpop`):** O(log n)
  - **Heapify (`heapify`):** O(n)
  - **Find k Largest (`nlargest`):** O(n log k)
  - **Merge (`merge`):** O(n log k), where k is the number of iterables being merged

- **Space Complexity:**  
  O(n), where n is the number of elements in the heap.

- **Additional Notes:**
  
  - **Simulating Max Heap:**  
    Since `heapq` only supports min-heaps, simulating a max-heap involves pushing the negative of each value. This inversion allows the largest original values to behave as the smallest in the min-heap.
  
  - **Heap Invariants:**  
    The heap property must be maintained after each operation. In a max-heap simulation, each parent node (as a negative value) is less than or equal to its child nodes.
  
  - **Heap as a List:**  
    Similar to min-heaps, max-heaps are implemented using lists. The smallest element (most negative) is at index 0, representing the largest original value.
  
  - **No Direct Max Heap Support:**  
    For more complex heap operations or if you require a dedicated max-heap structure, consider using third-party libraries or implementing a custom heap class.

- **Best Practices:**
  
  - **Simulate Max Heap Using Negatives:**  
    Consistently invert values when pushing and popping to maintain the max-heap behavior.
  
  - **Use Heaps for Priority-Based Operations:**  
    Leverage heaps for scenarios where you need quick access to the highest priority (largest) elements.
  
  - **Avoid Frequent Inversions:**  
    To minimize performance overhead, handle the inversion logic carefully, especially in performance-critical applications.
  
  - **Combine with Other Data Structures:**  
    Use `Counter` with heaps to efficiently find top k elements based on frequency or other criteria.
  
  - **Use Built-in Heap Functions:**  
    Utilize functions like `heapify()`, `heappush()`, `heappop()`, `heappushpop()`, `nlargest()`, and `nsmallest()` for efficient heap operations.

- **Example: Finding the Top K Frequent Elements Using a Max Heap**

  ```python
  from collections import Counter
  import heapq

  def top_k_frequent(nums, k):
      count = Counter(nums)
      # Create a max heap by pushing negative counts
      max_heap = [(-freq, num) for num, freq in count.items()]
      heapq.heapify(max_heap)
      
      top_k = []
      for _ in range(k):
          top_k.append(heapq.heappop(max_heap)[1])
      
      return top_k

  # Usage
  nums = [1,1,1,2,2,3]
  k = 2
  print(top_k_frequent(nums, k))  # Output: [1, 2]
  ```

  **Explanation:**  
  This function first counts the frequency of each element using `Counter`. It then creates a max heap by pushing negative frequencies along with the corresponding numbers. By popping the top `k` elements from the heap, it efficiently retrieves the `k` most frequent elements.

- **Example: Managing a Stream of Integers to Find the Kth Largest Element**

  ```python
  import heapq

  class KthLargest:
      def __init__(self, k, nums):
          self.k = k
          self.max_heap = [-x for x in nums]
          heapq.heapify(self.max_heap)
          while len(self.max_heap) > k:
              heapq.heappop(self.max_heap)

      def add(self, val):
          heapq.heappush(self.max_heap, -val)
          if len(self.max_heap) > self.k:
              heapq.heappop(self.max_heap)
          return -self.max_heap[0]

  # Usage
  kthLargest = KthLargest(3, [4, 5, 8, 2])
  print(kthLargest.add(3))  # returns 4
  print(kthLargest.add(5))  # returns 5
  print(kthLargest.add(10)) # returns 5
  print(kthLargest.add(9))  # returns 8
  print(kthLargest.add(4))  # returns 8
  ```

  **Explanation:**  
  This class maintains a max heap of size `k` by storing the negative of each number. When a new value is added, it is pushed onto the heap, and if the heap exceeds size `k`, the smallest element (which represents the largest original value) is popped. The top of the heap always contains the k-th largest element.

By understanding and utilizing max heaps through the `heapq` module, you can efficiently manage and extract the largest elements in various algorithmic scenarios, making them a powerful tool for competitive programming and data processing tasks.

## 9. Linked List

	•	Description: Linked lists are sequential structures where each element points to the next. They allow for efficient insertions and deletions at any point in the list.
	•	When to Use: Use when you need dynamic resizing and frequent insertions/deletions.
	•	Key Patterns:
	•	Reversing lists.
	•	Merging sorted lists.
	•	Implementing LRU caches.
	•	LeetCode Problem Types:
	•	Reverse Linked List (Problem #206)
	•	Merge Two Sorted Lists (Problem #21)

Python Implementation:

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

Time Complexity:

	•	Access: O(n)
	•	Insert/Delete: O(1)

## 10. Binary Search Trees (BST)

	•	Description: A Binary Search Tree (BST) is a tree structure where each node has at most two children, and for every node, the left child is smaller, and the right child is larger.
	•	When to Use: Use when you need to maintain a dynamic set of sorted elements or perform range queries.
	•	Key Patterns:
	•	Dynamic sets.
	•	Searching and inserting in sorted data.
	•	LeetCode Problem Types:
	•	Validate Binary Search Tree (Problem #98)
	•	Kth Smallest Element in a BST (Problem #230)

Python Implementation (using sortedcontainers.SortedDict):

from sortedcontainers import SortedDict
bst = SortedDict()
bst[10] = 'value'
del bst[10]

Time Complexity:

	•	Insert/Access/Delete: O(log n)

## 11. Segment Tree

	•	Description: Segment trees allow for efficient range queries and updates on an array of data, often used when you need to perform sum, minimum, or maximum queries.
	•	When to Use: Use when you need to query and update ranges of data efficiently.
	•	Key Patterns:
	•	Range sum or range min/max queries.
	•	Point updates.
	•	LeetCode Problem Types:
	•	Range Sum Query - Mutable (Problem #307)

Python Implementation:

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (2 * self.n)
        for i in range(self.n):
            self.tree[self.n + i] = arr[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, pos, value):
        pos += self.n
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]

    def sum_range(self, left, right):
        res = 0
        left += self.n
        right += self.n
        while left < right:
            if left % 2:
                res += self.tree[left]
                left += 1
            if right % 2:
                right -= 1
                res += self.tree[right]
            left //= 2
            right //= 2
        return res

Time Complexity:

	•	Build: O(n)
	•	Update: O(log n)
	•	Query: O(log n)

## 12. Union-Find (Disjoint Set)

	•	Description: Union-Find is used to keep track of a partition of a set into disjoint subsets and supports union and find operations.
	•	When to Use: Use in problems requiring dynamic connectivity, detecting cycles, or solving minimum spanning trees.
	•	Key Patterns:
	•	Dynamic connectivity.
	•	Detecting cycles in graphs.
	•	LeetCode Problem Types:
	•	Number of Connected Components in an Undirected Graph (Problem #323)
	•	Redundant Connection (Problem #684)

Python Implementation:

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

Time Complexity:

	•	Find/Union: O(α(n)), where α is the inverse Ackermann function

## 13. Tries (Prefix Trees)

	•	Description: Tries are tree-like structures used to store strings where each node represents a character.
	•	When to Use: Use in problems involving prefix matching or searching a collection of strings.
	•	Key Patterns:
	•	Autocomplete systems.
	•	Prefix search.
	•	LeetCode Problem Types:
	•	Implement Trie (Prefix Tree) (Problem #208)
	•	Word Search II (Problem #212)

Python Implementation:

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

Time Complexity:

	•	Insert/Search: O(m), where m is the length of the word

## 14. Balanced Trees (Using SortedDict)

	•	Description: A self-balancing binary search tree like AVL or Red-Black Tree is used when you need to maintain a dynamic sorted dataset.
	•	When to Use: Use when you need dynamic sorted data or range queries with balancing.
	•	Key Patterns:
	•	Maintaining a sorted set of data.
	•	Range queries.
	•	LeetCode Problem Types:
	•	Kth Largest Element in a Stream (Problem #703)

Python Implementation:

from sortedcontainers import SortedDict
bst = SortedDict()
bst[10] = 'value'
del bst[10]

Time Complexity:

	•	Insert/Delete/Access: O(log n)

By understanding when to apply each of these data structures and their associated time and space complexities, you can better tackle a wide variety of competitive coding problems on platforms like LeetCode.