# Week 2: Lecture 6-13

## Lecture 6

## Lecture 8 : Parsing CKY

### What is parsing

A parser in NLP uses the grammar rules to verify if the input text is valid or not syntactically. The parser helps us to get the meaning of the provided text. As the parser helps us to analyze the syntax error in the text; so, the parsing process is also known as the syntax analysis or the Syntactic analysis.

![Parsing](imgs/parsing.png)

Where Programming Laguages are easy to parse and Natural Language is hard to parse as there are no set grammar rules, no scope or precidence and lots of overloading.

### Ambiguity

Ambiguity is a type of meaning uncertainty giving rise to more than one plausible interpretation. Being ambiguous is therefore a semantic attribute of a form (a word, an idea, a sentence, even a picture) whose meaning cannot be resolved according to a rule or process with a finite number of steps.

Parse 1:
![Ambigious Grammar 1](imgs/ambigious1.png)

Parse 2:
![Ambigious Grammar 2](imgs/ambigious2.png)

Pence the parsing problem is defined as giving different sentences to a parser, and scoring the arse with respect to their respective best parse to get the accuracy

### Applications

- Machine Translation
- Speech Synthesis from parses
- Speech Recognition using parsing
- Grammar Checking
- Indexing for Information Retrival
- Inormation Extraction

### Algorithm

Liguistic properties are defined over trees and one needs to parse to make subtle distinctions. Parsing also gives us the semanics of order (**COmpositional Semantics**). Eg: what is the parse of $5*(6+2/4)$

Making Parsing Algorithm:

- Parse all terminals to their pre-terminals
- List each constituent in the format (`left_index`, `right_index`, `terminal`)
- if there are 2 adjacent terminals such as (`A`, `i`, `MID`) and (`B`, `MID`, `j`) and a grammar rule $Z \rightarrow A \ B$, then combine constituents in nonterminals (`Z`, `i`, `j`).
- Keep running this loop untill we parse the entire sentence.
- If get stuck at some terminal that doesnot combine with any adjacent terminals, then backtrack and try another rule.

Problems:

- Duplicate work ,we keep checking the same pairs
- Findinf new pairs are expensive as we look at rules list again and again.

To solve this we use a Parse chart

### Parse Chart

Now, we use this tabe to visualize our parsing:

![Parse Chart](imgs/table.png)

Where the contituents on the diagnal are the non-terminals and any elements to the right of this diagnal (at position `i` and `j` of the table) are the possible combinations of nontermnials from the index `i` to `j` in the sentence.

![Alt text](imgs/table-full.png)

For example $VP$ at position (1,4) is is the cominaion of all constituents from 1 to 3 in the sentence.

We construt these consitioents by decreasing width from the diagnal to avoid duplicates

### CYK Recognizer Algorithm

Aruguements:

- **Input**: string of `n` words.
- **Output**: Yes/no (only a recognizer)
- Data Structure: `n`x`n` table

The rows are labeled 0 to n-1, columns are 1 to n, cell [i, j] lists constituents found between i and j. Width = diagnol. Basic Idea: Fill cells of width-1 first then width-2 and so on.

Base Algo (Recognizer Version):

```ps
for end := 1 to n
    Add to [end-1, end] for all categories of the Jth word
for width := 2 to n
    for start := 0 to n-width           // This is I
    Define end := start + width         // this is J 
    for mid := start+1 to end-1         // find all I-to-J phrases 
        for every nonterminal Y in [start,mid] 
            for every nonterminal Z in [mid,end] 
                for all nonterminals X 
                    if X -> Y Z is in the grammar then add X to [start,end]
```

Optimized Base:

```ps
for J := 1 to n
    Add to [J-1, J] for all categories of the Jth word
for width := 2 to n
    for start := 0 to n-width           // This is I
    Define end := start + width         // this is J 
    for mid := start+1 to end-1         // find all I-to-J phrases 
      for every nonterminal Y in [start, mid]
          for every X -> Y Z is in the grammar
            if Z in [mid, end]
              then add X to [start, end]
```

Alternate Version with inner loop:

```ps
for J := 1 to n
    Add to [J-1, J] for all categories of the Jth word
for width := 2 to n
    for start := 0 to n-width           // This is I
    Define end := start + width         // this is J 
    for mid := start+1 to end-1         // find all I-to-J phrases 
        for every X -> Y Z is in the grammar
          if Y in [start, mid] and Z in [mid, end]
            then add X to [start, end]
```

Incremental left-to-right parsing?

Full CYK:

```ps
for J := 1 to n
    Add to [J-1, J] for all categories of the Jth word
for width := 2 to n
    for start := 0 to n-width           // This is I
    Define end := start + width         // this is J 
    for mid := start+1 to end-1         // find all I-to-J phrases 
        for every nonterminal Y in [start, mid] 
          for every nonterminal Z in [mid, end] 
            for every X -> Y Z is in the grammar 
              add X to [start, end]
```

Incremental CYK:

Visit columns left to right and fill each bottom-up.

```ps
for J := 1 to n
    Add to [J-1, J] for all categories of the Jth word
for width := 2 to n
    for start := 0 to n-width           // This is I
    Define end := start + width         // this is J 
    for mid := start+1 to end-1         // find all I-to-J phrases 
        for every nonterminal Y in [start, mid] 
          for every nonterminal Z in [mid, end] 
            for every X -> Y Z is in the grammar 
              add X to [start, end]
```

### What is space and Runtime

### Dyna

```pc
phrase(X,I,J):-  rewrite(X,W), word(W,I,J).
phrase(X,I,J):-  rewrite(X,Y,Z), phrase(Y,I,Mid), phrase(Z,Mid,J).
goal         :-  phrase(start_symbol, 0, sentence_length).
```

![Alt text](imgs/dyna-rules.png)

We give a rule and corresponding phrases to combine into pharse that has a larger span. A phrase that covers the whole sentence is a parse.

### Procedural Algorithm

The Dyna program runs fine.
It nicely displays the abstract structure of the algorithm.  

But Dyna is a declarative programming language that hides the details of the actual execution from you.
If you had to find the possible phrases by hand (or with a procedural programming language), what steps would you go through?

## Lecture 10 : Earley's Algorithm

Features of Earley's Algorithm:

- It is able to work with either left recursive or right recursive grammar that other parsers (recursive descent and bottom up parsers) have a hard time dealing with.
- It works with ambigious grammar (multiple parses)
- Allows for good error reporting.

Disadvantages of Earley's Algorithm:

- it's not efficient O(n^3) for ambigious grammar O(n^2) oherwise. while alternatives are O(n) in best case.

### Overview

Earley's Algorithm only parses from left to right and is contraint by it. this causes it to save time by not building impossible things.

for impllementing Earley's Algorithm:

- Find full and partial constituents (e.g. $A \rightarrow B \ C \ . \ D \ E$)
- Proceed incrementally from left to right, before reading word **'n'**, we have already created all hypothesis for words **'n-1'**
- Attaching the hypothesis of D to $A \rightarrow B \ C \ . \ D \ E$ gives $A \rightarrow B \ C \ D \ . \ E$.
- For a sentence of length 'n' we creeate 'n+1' numbered divisions between and around the words.

**Recursive Descent** fails with **Left Recursion** as our stack gets overflowed from infinite expansion.

### Changing to appropriate grammar

Left Recursion can be converted into **Right Recursion** by changine specific rules, example:

$$
VP \rightarrow V \ NP\\
VP \rightarrow VP \ PP
$$

above is a grammar with Left Recrsion, which can be converted by introducing some new nn-terminals and rules:

$$
VP \rightarrow V \ NP\\
VP \rightarrow V \ NP \ PPlist\\
PPlist \rightarrow PP\\
PPlist \rightarrow PP \ PPlist\\
$$

Even after doing this, parsing could be very slow (solving the same NP problem). Hence we need **Dynamic Programming** to speed things up.

### Parse Table

Similar to CKY parsing, we can look up anythin we have created so far to combine (dynamic programming).

**Vernacular**: Entries in column $5$ looks like $(3, S \rightarrow NP \ . \ VP)$ this means that the input substring from 3 to 5 matches the initial NP portion of the $S \rightarrow NP \ VP$ rule. The Dot (.) shows how much of the rule has been matches in that specific column. This means that some dotted rule back in Column 3 is looking for an $S$ that starts at 3. Hence if we are able to find a $VP$ starting in column 5 we will be able to attach $S$ to something.

In short Top-Down (Goal-Directed) parser does not start building because of input but because of context needs. Operations of algorithm:

- Process all hypothesis one at a time. This might lead to new hypothesis being formed orold ones being reused dependent on what fits the next word Process a hypothesis according to what follows the dot – just as in recursive descent:
- **SCAN**: See if terminal word matches input
- **PREDICT**: For nonerminals, find ways to match it (can look ahead to only select appropriate options)
- **ATTACH**: if there is nothing more to attach then we say that we have a complete constituent that can be attached to the previous incomplete constituent.

All entires ending at $j^{th}$ index of sentence are stored in $j^{th}$ column.

### Left Recursion vs Top-Down Parsing

### Complexity

## Lecture 11 : Weighted Probabalistic Parsing Parsing CKY

## Lecture 12

## Lecture 13
