# Stack and Heap Memory: An Overview

Looking at **stack** and **heap** memory and see how your code and your variables are stored in memory when your application is running. Understanding what your code is doing in memory can be really helpful to figure out why things have different scopes.

---

## Memory in an Application

The memory of your application is stored in three main parts:

1. **Machine Code**  
   This is where your application is converted into instructions that your computer can understand.

2. **Stack**  
3. **Heap**

---

## The Stack

### The Stack Data Structure

- The stack data structure is like a stack of books.
- You can only add or remove items from the **top**.
- You **cannot** access items from the middle or the bottom of the stack.

### The Call Stack

In applications, we refer to the **call stack**, which has two main responsibilities:

1. **Method Control:**  
   - Keeps track of the method to which control should return after the current method finishes executing.
   - Each time you call a method, it gets added to the call stack. As methods complete, they are removed from the stack.

2. **Local Variables:**  
   - The call stack also keeps track of the local variables within each method.
   - Once the method execution is finished, its block on the call stack is removed along with its local variables.

---

## The Heap

- Unlike the stack, the heap allows you to store items in any order.
- You can access any item directly without having to follow a strict top-only rule.
- Due to its flexible nature, **adding and removing items** in the heap comes with a higher overhead compared to the stack.

### When to Use the Heap

- The heap is typically used for data that needs to **outlive** the scope of the call stack.
- For example, if you have a variable that needs to be accessed across different methods, it will usually be stored on the heap.

---

## Variable Storage Rules

There are some general rules to determine where variables are stored:

### Value Types vs. Reference Types

- **Value Types:**  
  - Store the actual value.
  - Example: `int` is typically stored as a single value.
  - Storage depends on where they are declared.  
    - **Local Variables:** Stored on the call stack.
    - **Global Variables or Class Members:** Stored on the heap.

- **Reference Types:**  
  - Store a pointer (or address) to the actual value.
  - The pointer might be on the call stack (if declared locally), but the actual value is stored on the **heap**.

### Local Variables

- When you declare a local variable inside a method, it’s stored on the call stack.
- Once the method execution is finished, that stack block (and its local variables) is removed.

### Reference Type Variables Declared Locally

- The pointer remains on the call stack while the actual object (the value) resides on the heap.
- After the method finishes, if nothing is pointing to that heap-allocated value, it becomes inaccessible.

---

## The Garbage Collector

- **Garbage Collection:**  
  Most runtimes include a garbage collector that automatically goes through the heap to clean up memory that is no longer used.
- For instance, if a reference type variable is no longer referenced after the method execution, the garbage collector will eventually reclaim that memory.

**General Rule:**  
- **Reference types** are always on the **heap**.
- **Value types** can be on the **stack** or **heap** depending on where they are declared.

---

## Exceptions to the General Rules

### Static Variables

- **Static Variables:**  
  - Always stored on the heap.
  - Accessible from anywhere in your code.

### Anonymous Functions

- **Anonymous Functions:**  
  - Created and called within another method.
  - They require access to variables declared in the calling method.
  - To allow this access, these variables may be temporarily stored on the heap since you can only access the top of the stack.

### Asynchronous Methods

- **Asynchronous Methods:**  
  - Run on a different thread, each having its own call stack.
  - As threads are independent, the results of asynchronous methods are stored on the heap so that they can be accessed later.

---

## Conclusion

That’s a quick overview of how stack and heap memory work, including where different types of variables are stored and the role of the garbage collector. Understanding these concepts is crucial for managing scope and memory in your applications.