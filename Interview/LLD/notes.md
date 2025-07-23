# Amazon Functional Interview Questions, Preparation, Low Level Design (LLD) Notes

### **System Design & OOD**  
1. **Design Problems**
   
   [IMP]
   - **Design Logging Framework**: Design a logging framework that supports different log levels and loggers. [GitHub Answer](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/logging-framework.md)
   - **Rate Limiter**: Design a rate limiter that limits the number of requests per second. [YouTube anSWER](https://www.youtube.com/watch?v=Eg5uH5sU3zw&list=PLMCXHnjXnTnvQVh7WsgZ8SurU1O2v_UM7&index=9)
   - **Design a Calculator**: Design a calculator that supports basic arithmetic operations.
   - **File System**: Implement search functionality (e.g., by size, creation date).  
   - **Task Scheduler**: In-memory scheduler with dependency resolution.  


  [Later]
   - **Warehouse Class**: Constraints on product storage.  
   - **Restaurant Table Booking System**: Optimize table allocation based on party size and time slots.  
   - **Automated Valet Parking**: Optimal slot assignment and token generation.  
   - **Design Chess Game**: Implement a chess game with all the rules and functionalities. ([answer repo](https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/python/chessgame))
   - **Design Snake and Ladder Game**: Implement a snake and ladder game with all the rules and functionalities. [GitHub Answer](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/snake-and-ladder.md)
   - **Design Splitwise**: Design a system like Splitwise where users can add expenses and split them among friends. [GitHub Answer](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/splitwise.md)
   - **Movie Ticket Booking System**: Design a movie ticket booking system that supports booking tickets, canceling tickets, and viewing available seats. [GitHub Answer](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/movie-ticket-booking-system.md)

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

## Low Level Design (LLD): Structuring and Answering a LLD Question

### Steps for Answering a LLD Interview Problem

1. **Clarify Requirements and Identify Core Use Cases:**
   - Ask clarifying questions to fully understand the real-world problem.
   - Determine the core functionalities (use cases) that the system must support.
   - *Example:* In a "Stack Overflow" design question, clarify whether to support user registration, login, posting questions/answers, and commenting.

2. **Identify Key Entities:**
   - Break down the problem and list the main entities (or objects) needed.
   - *Example Entities for a Q&A Platform:* User, Question, Answer, Comment.

3. **Define Classes and Their Attributes:**
   - Translate each identified entity into a class.
   - Identify and list key attributes for each class.
   - *Example:* A `User` class might include attributes like username, password, and email.

4. **Determine Core Methods Based on Use Cases:**
   - Identify the main operations for each class.
   - *Example:* The `User` class might include methods such as `register()`, `login()`, and `postQuestion()`.

5. **Define Relationships Between Classes:**
   - Use UML diagrams to illustrate class relationships.
   - Determine associations such as aggregation, composition, or inheritance.
   - *Example:* A `Question` class might hold a list of `Answer` objects.

6. **Implement Necessary Methods:**
   - Implement key methods based on the core requirements.
   - Discuss with the interviewer which methods to fully implement and which can be stubbed.
   
7. **Exception Handling and Edge Cases:**
   - Explain how you would handle errors, exceptions, and unexpected inputs.
   - Discuss strategies for robust error handling and validations.

8. **Follow Good Coding Practices:**
   - Use meaningful names for classes, methods, and variables.
   - Strive for simplicity and readability.
   - Prefer composition over inheritance to promote flexibility and reduce tight coupling.
   - Use interfaces or abstract classes to define contracts between components.
   - Aim for modularity and separation of concerns to enhance maintainability and scalability.

9. **Apply Design Principles and Patterns:**
   - **Design Patterns:**  
     - **Singleton Pattern:** Ensure a class has only one instance.  
       - [Singleton Pattern](https://www.youtube.com/watch?v=sJ-c3BA-Ypo)
     - **Factory Pattern:** Create objects without specifying the exact class of object that will be created.  
       - [Factory Pattern](https://www.youtube.com/watch?v=phTXrJqRgnI)
     - **Observer Pattern:** Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified.  
       - [Observer Pattern](https://www.youtube.com/watch?v=-oLDJ2dbadA)
   - **SOLID Principles in Class Design:**  
     - Design classes to be open for extension but closed for modification.  
       - [SOLID in Python](https://www.youtube.com/watch?v=ZkknJI3QMss)
   - **Dependency Injection & Inversion of Control:**
     - Design components to receive their dependencies from the outside, making them easier to test and maintain.

10. **Consider Scalability and Maintainability:**
    - Ensure your design can handle large data sets and evolving requirements.
    - Explain how your design separates concerns and is easily maintainable.

## Additional Tips and Insights from the Live Session

- **Understanding Your Audience and Course Focus:**
  - The live session highlighted that most candidates (especially SD1, SD2, and college undergrads) benefit from strong fundamentals in OOP, design patterns, and basic data structures.
  - While advanced LLD questions (often asked in SD3+ interviews) require detailed code optimizations, the basics must be crystal clear for beginners.

- **Practical Application Over Theoretical Knowledge:**
  - Emphasis was placed on implementing designs in code. For instance, real-world problems like a social media system or e-commerce platforms are broken down into manageable parts (e.g., user profiles, feeds, payment gateways).
  - It was noted that understanding the trade-offs and being able to explain why one design pattern was chosen over another is crucial.

- **Language Agnostic Concepts with Minor Language-Specific Differences:**
  - Although languages like Java, C++, and Python may handle design pattern implementations differently, the core concepts remain the same.
  - The transcript reinforced that the majority of work is done in planning (requirements, use cases, class diagrams) rather than in the final code signatures.

- **Visual Representation and Engagement:**
  - Candidates are encouraged to use visual aids (UML diagrams, class diagrams) to clearly explain their design.
  - Visual representations help in understanding relationships between entities and make your design more compelling during the interview.

- **Interactive Learning and Continuous Improvement:**
  - The live session included Q&A, feedback, and even live debugging examples. This interactive approach is beneficial for grasping the nuances of LLD.
  - Regular feedback (via Zoom sessions and discussion panels) can help you fine-tune your design approach.

- **Focus on Implementation and Testing:**
  - In LLD interviews, it's important not only to design but also to discuss how you would implement and test the system.
  - Discuss strategies for unit tests, handling concurrency, and ensuring code readability and maintainability.

- **Design Patterns as Tools, Not End-All Solutions:**
  - Design patterns should be used as tools to solve specific problems. Their theory is valuable, but the focus should be on where and how to apply them in real projects.
  - It was suggested that learning through examples (code snippets, diagrams) is far more effective than solely watching theory videos.

## Best Practices for LLD Interviews

- **Clarify:** Always ask for clarifications before diving into your design.
- **Plan:** Identify core use cases and break down the problem into manageable components.
- **Design:** Map out your classes, relationships, and responsibilities using UML or class diagrams.
- **Implement:** Write clean, modular, and well-documented code that follows OOP best practices.
- **Iterate:** Discuss both short-term implementations and long-term improvements.
- **Engage:** Use visual aids, ask questions, and consider feedback to continuously improve your design.

## Practice Using AI Tools (e.g., ChatGPT)
- **How to Practice:**
  - Prompt AI with your resume and job description to generate challenging functional and LLD questions.
  - Iterate on questions by adding specific constraints (e.g., numerical data, KPIs).
- **What to Avoid:**
  - Rely solely on AI analysis of your answers—focus on building detailed, data-backed responses on your own.

## Final Recap

- **Four Essential Parts for Functional Questions:**
  1. **Clarify:** Ask questions to gain clarity.
  2. **Assume:** Declare specific, data-driven assumptions.
  3. **Short-Term Fix:** Describe immediate remediation steps.
  4. **Long-Term Fix:** Outline how to permanently resolve the problem.

- **LLD Specific Steps:**
  1. Clarify requirements and use cases.
  2. Identify key entities and define classes.
  3. Determine attributes and core methods.
  4. Establish relationships with UML diagrams.
  5. Implement key methods and handle exceptions.
  6. Follow coding best practices and design principles.
  7. Utilize design patterns and SOLID principles.
  8. Focus on scalability and maintainability.

- **Key Advice:**
  - Practice with both functional and behavioral questions.
  - Use an iterative process to refine your designs.
  - Stay engaged by using visual tools and feedback sessions.
  - Continually update your knowledge on design patterns and trade-offs.
  - Focus on implementation details, testing strategies, and clear communication of your design rationale.
