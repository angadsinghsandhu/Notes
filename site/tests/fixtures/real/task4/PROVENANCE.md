# Task 4 archive fixtures

All inputs are copied from this repository; fixtures are never executed.

- `transformers.md`: exact `Interview/Applied Science/breadth/6.6.2-transformers.md`.
- `masters-theorem.md`: exact `Interview/Notes/Abdul Bari/2 Divide and Conquer/4.1 Masters Theorem in Algorithms for Dividing Function (part-1).md`.
- `78_Subsets.py`: exact `Interview/leetcode/Solutions/78_Subsets.py`.
- `gpu-excerpt.json`: first six cells (indices 0–5), unchanged parsed cells and original top-level metadata/nbformat, from `Tutorials/GPU/nv-gpu-workshop/1.0_CPU_GPU_Comparison.ipynb`; JSON serialization only.
- `pytorch-excerpt.json`: first four cells (indices 0–3), unchanged parsed cells and original top-level metadata/nbformat, from `Classes/Stanford/Stanford CS234 - Reinforcement Learning (2019)/Practice/DL_PyTorch_Tutorial_17th_Jan_2023.ipynb`; JSON serialization only.
- `nlp-week2-excerpt.md`: exact first 46 lines of `Classes/Johns Hopkins/Sem 1/NLP/Week 2/ReadMe.md`, inclusive. Excerpt intentionally covers inline, one-line display, and multiline math.

Notebook attachments/security/malformed inputs in the tests are explicitly synthetic. `tests/fixtures/synthetic/task4/unicode.md` is synthetic because actual Japanese README placeholders are empty.
