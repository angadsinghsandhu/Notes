# Amazon Functional Interview Questions, Preparation, Low Level Design (LLD) Notes

### **System Design & OOD**  
1. **Design Problems**  
   - **Parking Lot System**: Design with support for small/medium/large vehicles. <[AlgoMonster Video](https://www.youtube.com/watch?v=nwioCA5nrYc)>
   - **Design a Tic Tac Toe Game**: Implement a two-player game with a 3x3 grid. Include functionality to check for a win, draw, and reset the game. <[GeeksforGeeks Article](https://www.geeksforgeeks.org/design-tic-tac-toe-game/)>
   - **File System**: Implement search functionality (e.g., by size, creation date).  
   - **Task Scheduler**: In-memory scheduler with dependency resolution.  
   - **Warehouse Class**: Constraints on product storage.  
   - **Restaurant Table Booking System**: Optimize table allocation based on party size and time slots.  
   - **Automated Valet Parking**: Optimal slot assignment and token generation.  
   - **Coupon System**: Generate and apply coupons based on product categories.  
   - **LRU Cache with TTL**: Implement a cache with time-to-live feature.
   - **LRU Cache with TTL**: Implement a cache <[NeetCode](https://www.youtube.com/watch?v=7ABFKPK2hD4)>
   - **Amazons Locker Delivery SYstem**: code amazon's locker delivery system for a city block. provided a block of the city (m x n matrix) and (x, y) coordicates for existing locations.

   - **Vending Machine**: Design a vending machine that dispenses items based on user input.
   - **Elevator System**: Design an elevator system for a building with multiple floors.
   - **Design Chess Game**: Implement a chess game with all the rules and functionalities.
   - **Design Snake and Ladder Game**: Implement a snake and ladder game with all the rules and functionalities.
   - **Design SPlitwise**: Design a system like Splitwise where users can add expenses and split them among friends.
   - **Design Logging Framework**: Design a logging framework that supports different log levels and loggers.
   - **Hotel Management System**: Design a hotel management system that supports booking rooms, checking in/out, and room service.
   - **Movie Ticket Booking System**: Design a movie ticket booking system that supports booking tickets, canceling tickets, and viewing available seats.
   - **Load Balancer**: Design a load balancer that distributes incoming requests to multiple servers.

1. **Design Patterns**  
   - Singleton, Factory, Observer patterns.  
     - [Singleton Pattern](https://www.youtube.com/watch?v=sJ-c3BA-Ypo)
     - [Factory Pattern](https://www.youtube.com/watch?v=phTXrJqRgnI)
     - [Observer Pattern](https://www.youtube.com/watch?v=-oLDJ2dbadA)
   - SOLID principles in class design.  <[SOLID in Python](https://www.youtube.com/watch?v=ZkknJI3QMss)>
   - Dependency Injection, Inversion of Control.

2. **API/Class Design**  
   - **Unix Find Command**: Design a search API for a file system.  
   - **Most Recently Played Songs Playlist**: Support `addSong` and `getSong`.  
   - **AutoComplete Feature**: Trie-based implementation with priorities.  

3. **Real-World Scenarios**  
   - **Top 20 Items Sold in Last Hour**: Stream processing for real-time analytics.  
   - **Log Analysis**: Calculate average runtime of operations from timestamped logs. 

## Overview

- **Purpose of Functional Interview Questions:**
  - Test your expertise and depth in your subject matter.
  - Assess how you tackle real-life problems by using data, making assumptions, and iterating on your answers.

- **Sample Questions by Role:**
  - **Software Development Engineer (SDE):**  
    *“Code Amazon's Locker delivery system for a city block. You’re provided with the number of blocks in your city represented by an array and a list of (x, y) coordinates for existing locker locations.”*
  - **Solutions Architect/Software Engineer:**  
    *“Design Twitter, considering tweet throughput, database design, encryption, autoscaling, etc.”*
  - **Product Manager (PM):**  
    *“You are in charge of launching Alexa in a new territory (e.g., South Africa) with 12 months and a $3M budget. How would you do it?”*
  - **Finance:**  
    *“Build a discounted cash flow valuation model for acquiring the exclusive rights to the next Hollywood blockbuster for Prime Video.”*

## The 4-Step Process to Answer Functional Questions

### Step 1: Ask Clarifying Questions
- **What to do:**
  - Pause and ask questions to clarify requirements.
  - Examples (SDE case): Ask which programming language to use, scalability needs, encryption requirements, and launch deadlines.
- **Benefits:**
  - Demonstrates courage and a desire to understand the problem fully.
  - Shows that you consider multiple perspectives before committing to an answer.
- **Note:** Do not ask too many questions—one or two well-placed questions are enough.

### Step 2: Make Assumptions and Declare Them
- **What to do:**
  - Be specific with your answer by stating all concrete assumptions.
  - Use data and illustrations to back up your assumptions.
- **Examples (Solutions Architect case):**
  - Specify assumptions such as tweets per second (read/write), number of users, storage sizes, database table designs, and security/encryption needs.
- **Benefits:**
  - If your assumptions are correct, you impress the interviewer.
  - If incorrect, the interviewer can correct you, and you demonstrate adaptability by adjusting your logic.

### Step 3: Describe How You’d Fix the Problem in the Short-Term
- **What to do:**
  - Explain how you’d resolve the immediate problem.
  - Use the example (PM case) of launching Alexa:
    - Truncate the project timeline (e.g., deliver in 9 months) to handle immediate issues and reserve time at the end to manage unforeseen challenges.
- **Benefits:**
  - Shows you can act quickly to stop a “fire” and stabilize the situation.

### Step 4: Describe How You’d Fix the Problem in the Long-Term
- **What to do:**
  - Explain how you’d address and eliminate the root cause.
  - Use the example (Finance case) of building a DCF valuation model:
    - Not only build the short-term solution (the model) but also propose sharing and standardizing this approach across teams.
- **Benefits:**
  - Illustrates long-term strategic thinking beyond just putting out fires.

## Practice Using AI Tools (e.g., ChatGPT)
- **How to Practice:**
  - Prompt AI with your resume and the job description to generate relevant and challenging functional questions.
  - Iterate on the questions by adding specific constraints (e.g., numerical data, KPIs).
- **What to Avoid:**
  - Relying on AI analysis of your answers—focus on practicing your own detailed and data-backed responses.

## Final Recap
- **Four Essential Parts:**
  1. **Clarify:** Ask questions to gain clarity.
  2. **Assume:** Declare specific, data-driven assumptions.
  3. **Short-Term Fix:** Describe immediate remediation steps.
  4. **Long-Term Fix:** Outline how to permanently resolve the problem.
- **Key Advice:**
  - Practice with both functional and behavioral questions.
  - While functional questions are important, success in behavioral interviews often has the final impact on your hiring decision.