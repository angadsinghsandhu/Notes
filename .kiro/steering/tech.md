# Tech Stack

## Languages
- **Python**: Primary language for algorithms, ML/DL, and LLD implementations
- **JavaScript/TypeScript**: React and web development courses
- **Jupyter Notebooks**: ML/DL experimentation and course materials

## ML/DL Frameworks
- PyTorch
- TensorFlow / Keras
- fastai

## Web Development
- React
- Tailwind CSS
- D3.js (data visualization)

## Tools
- Docker
- Git

## Python Conventions
- Use type hints (`List`, `Optional`, `Dict` from `typing`)
- Use `abc.ABC` and `@abstractmethod` for interfaces
- Include docstrings with Args/Returns documentation
- Follow PEP 8 style guidelines

## LeetCode Solution Format
```python
# File header with problem metadata
"""
Problem Number: X
Problem Name: Name
Difficulty: Easy/Medium/Hard
Tags: Array, Hash Table, etc.
Company (Frequency): Company (N)
Leetcode Link: <url>

DESCRIPTION
...
"""

class Solution:
    def brute_force_solution(self, ...):
        """
        Approach: ...
        T.C.: O(n)
        S.C.: O(1)
        """
        pass

    def optimized_solution(self, ...):
        pass

if __name__ == "__main__":
    # Test cases
    pass
```

## LLD Implementation Format
- File header with description and design steps covered
- Use abstract base classes for interfaces
- Apply design patterns: Factory, Singleton, Strategy, Observer
- Include `demo.py` for usage examples
- Follow Single Responsibility Principle
