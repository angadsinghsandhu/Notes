# Section 2: JavaScript Refresher

## 12. Module Introduction

- **Scope:** Core JavaScript concepts you need for building React apps  
- **Optional:** Skip if you’re comfortable with JS; revisit anytime you need a refresher  
- **Not a full JS course:** Assumes basic JS/web development experience  
- **Focus:**  
  - Modern JS syntax & rules  
  - Essential features used throughout this React course  

## 13. Starting Project

- **CodeSandbox setup:**  
  - Basic web project (HTML + assets folder)  
  - No JS code initially  
- **Workflow:**  
  - Write JS in `app.js` under new `scripts/` folder  
  - View output in the **Console** tab of the sandbox  
- **Goal:** Experiment with syntax and language features, not build UI

## 14. Adding JavaScript To A Page & How React Projects Differ

- **Execution environments:**  
  - Browser (original JS runtime)  
  - Node.js, Deno (server‑side or other)  
- **Including JS in HTML:**  
  1. **Inline** `<script>…</script>` (for tiny snippets)  
  2. **External** `<script src="scripts/app.js" defer></script>`  
     - `defer` delays execution until after HTML is parsed  
     - Best practice: keep code in separate `.js` files  
- **ES Modules:**  
  - Add `type="module"` to `<script>` to enable `import`/`export`  
- **React projects:**  
  - You won’t manually add `<script>` tags—build tools inject them for you

## 15. React Projects Use a Build Process

- **No manual `<script>` in `index.html`**—React’s build injects them  
- **Build tools (e.g., React Scripts, Vite):**  
  - **Transform JSX** into browser‑compatible JS  
  - **Minify/optimize** code for production (shorten names, remove whitespace)  
  - **Serve via dev server** that watches & rebuilds on save  
- **Why Node.js?**  
  - Required for build scripts and package management (npm/yarn)

## 16. `"import"` & `"export"`

- **Modules:** Split code across `.js` files for maintainability  
- **Named exports:**

  ```js
  // util.js
  export const apiKey = '123-abc';

  // app.js
  import { apiKey } from './util.js';
  console.log(apiKey);
  ```

- **Default exports (one per file):**

  ```js
  // util.js
  export default 'DEFAULT_VALUE';
  ```

  ```js
  // app.js
  import anyName from './util.js';
  console.log(anyName);
  ```

- **Mixed exports:** You can have one default + many named in the same file
- **Import all named as object:**

  ```js
  import * as utils from './util.js';
  console.log(utils.apiKey);
  ```

- **Aliases:**

  ```js
  import { apiKey as key } from './util.js';
  ```

## 17. Revisiting Variables & Values

- **Value types:**

  - Primitives: strings, numbers, booleans, `null`, `undefined`
  - Reference: objects, arrays
- **Variables vs. constants:**

  - `let x = …;` allows reassignment
  - `const y = …;` cannot be reassigned
- **Naming conventions:**

  - camelCase, start with a letter, no spaces/dashes ( `$` and `_` allowed )
- **Why use variables?**

  - Reuse values, improve readability, centralize updates

## 18. Revisiting Operators

- **Arithmetic:** `+`, `-`, `*`, `/`
- **String concatenation:** `"hello" + " world"` → `"hello world"`
- **Comparison:**

  - Strict equality: `===` → returns `true`/`false`
  - Greater/less than: `<`, `>`, `<=`, `>=`
- **Usage:** Often combined with `if` statements for control flow

## 19. Revisiting Functions & Parameters

- **Declaration:**

  ```js
  function greet(userName, message = 'Hello!') {
    return `Hi, I am ${userName}. ${message}`;
  }
  ```

- **Invocation:**

  ```js
  const greeting = greet('Max', 'What’s up?');
  console.log(greeting);
  ```

- **Key points:**

  - Functions bundle reusable logic
  - Parameters accept inputs; can have defaults
  - Use `return` to produce values
  - Name functions to describe their action

## 20. Arrow Functions

- **Syntax:**

  ```js
  const greet = (name, msg) => {
    console.log(`${name}: ${msg}`);
  };
  ```

- **Characteristics:**

  - Always anonymous; assigned to a variable
  - No `function` keyword
  - Suitable for callbacks and concise definitions

## 21. More on the Arrow Function Syntax

- **Single param:** omit parentheses

  ```js
  name => console.log(name);
  ```

- **No params:** use empty `()`

  ```js
  () => console.log('Hi');
  ```

- **Implicit return:** omit `{}` and `return` for one‑liner

  ```js
  num => num * 3
  ```

- **Returning object literal:** wrap in `(...)`

  ```js
  () => ({ age: 30 })
  ```

## 22. Revisiting Objects & Classes

- **Objects:**

  ```js
  const user = { name: 'Max', age: 34 };
  console.log(user.name);
  ```

- **Methods & `this`:**

  ```js
  const user = {
    name: 'Max',
    greet() {
      console.log(`Hi, I am ${this.name}`);
    }
  };
  user.greet();
  ```

- **Classes (ES6):**

  ```js
  class Person {
    constructor(name, age) {
      this.name = name;
      this.age = age;
    }
    printName() {
      console.log(this.name);
    }
  }
  const p = new Person('Manuel', 35);
  p.printName();
  ```

- **Inheritance:**

  ```js
  class Human { species = 'human'; }
  class Person extends Human { /* ... */ }
  ```

## 23. Arrays & Array Methods (like map)

- **Definition & access:**

  ```js
  const hobbies = ['Sports', 'Cooking', 'Reading'];
  console.log(hobbies[0]); // 'Sports'
  ```

- **Mutating methods:**

  - `hobbies.push('Working')` adds an element
- **`findIndex(fn)`:**

  - Returns index of first element where `fn(item) === true`
- **`map(fn)`:**

  - Transforms each item into a new array
  - Does **not** mutate original

  ```js
  const excited = hobbies.map(h => `${h}!`);
  ```

## 24. Destructuring

- **Array destructuring:**

  ```js
  const userNameData = ['Max', 'Schwarzmüller'];
  const [firstName, lastName] = userNameData;
  ```

- **Object destructuring:**

  ```js
  const user = { name: 'Max', age: 34 };
  const { name, age } = user;
  ```

- **Aliasing:**

  ```js
  const { name: userName } = user;
  ```

## 25. Destructuring in Function Parameter Lists

- **Example:**

  ```js
  function storeOrder({ id, currency }) {
    localStorage.setItem('id', id);
    localStorage.setItem('currency', currency);
  }
  storeOrder({ id: 5, currency: 'USD', amount: 15.99 });
  ```

- **Note:** Function still takes one argument (an object)

## 26. The Spread Operator

- **Arrays:**

  ```js
  const all = [...hobbies, ...moreHobbies];
  ```

- **Objects:**

  ```js
  const extendedUser = { ...user, isAdmin: true };
  ```

- **Use cases:**

  - Merging lists/objects
  - Shallow cloning to avoid mutating originals

## 27. Revisiting Control Structures

- **`if / else if / else`:** conditional branching
- **Example:** prompt for password, grant or deny access
- **`for…of` loop:** iterate over arrays

  ```js
  for (const hobby of hobbies) {
    console.log(hobby);
  }
  ```

## 28. Manipulating the DOM – Not With React

- **Vanilla JS:** `document.querySelector()` & direct DOM updates
- **In React:** avoid manual DOM manipulation; use React’s declarative rendering

## 29. Using Functions as Values

- **Callbacks:** pass functions to functions

  ```js
  setTimeout(() => console.log('Timed out'), 1000);
  ```

- **Named handlers:**

  ```js
  function handleTimeout() { console.log('Timed out'); }
  setTimeout(handleTimeout, 500);
  ```

- **Custom example:**

  ```js
  function greeter(fn) { fn(); }
  greeter(() => console.log('Hi'));
  ```

## 30. Defining Functions Inside Of Functions

- **Nested functions:** inner functions are scoped to their parent

  ```js
  function init() {
    function greet() { console.log('Hi'); }
    greet();
  }
  init();
  ```

## 31. Reference vs Primitive Values

- **Primitives (string, number, boolean):** immutable, operations return new values
- **Reference types (objects, arrays):** mutable, methods (e.g., `push`) change the original
- **`const` with objects/arrays:** prevents rebinding the variable, but not mutation of its contents

## 32. Next‑Gen JavaScript – Summary

- **Recap of key features:**

  - `let` & `const`
  - Arrow functions & concise syntax
  - Modules: `export`/`import` (named & default)
  - Classes & inheritance
  - Spread/rest operator (`...`)
  - Destructuring arrays/objects
- **Resources:** MDN links embedded in lecture

## 33. JS Array Functions

- **Important methods:**

  - `map()`, `find()`, `findIndex()`, `filter()`, `reduce()`
  - `concat()`, `slice()`, `splice()`
- **MDN Reference:** [Array prototype methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)

## 34. Module Resources

- **Finished Code (CodeSandbox):**
  [https://codesandbox.io/s/javascript-refresher-j56djd](https://codesandbox.io/s/javascript-refresher-j56djd)
- **GitHub Snapshot:**
  [https://github.com/academind/react-complete-guide-code/tree/02-js-refresher](https://github.com/academind/react-complete-guide-code/tree/02-js-refresher)
- **Slides & instructions:** available in the GitHub repo above
