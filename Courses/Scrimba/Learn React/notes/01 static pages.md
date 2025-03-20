# Static Pages

Building static pages is a common task in web development. In this chapter, we will learn how to create static pages using React. We will also learn how to organize the static pages in a React project.

We will do this by building a simple website with a single static page, that talks aboyt some facts about React.

## What we will learnt

- Why should we care about React
- Setting up a React project
- JSX
- Custom Components
- Styling

## First React Code

To render content in React, we need to include a **root element** in our HTML file where React will insert content dynamically.

index.html:

```html
<html>
    <head>
        <link rel="stylesheet" href="/index.css">
    </head>
    <body>
        <div id="root"></div>
        <script src="/index.jsx" type="module"></script>
    </body>
</html>
```

index.css:

```css
body {
    font-family: Arial, Helvetica, sans-serif;
    background: #27292c;
    color: white;
    text-align: center;
}

h1 {
    margin-top: 40px;
}
```

Instead of manually adding elements inside the `<div id="root"></div>`, React takes control and dynamically inserts content.

index.jsx:

```jsx
import { createRoot } from "react-dom/client"

// 1. Create a root
const root = createRoot(document.getElementById("root"))
// 2. Render some markup to the root
root.render(<h1>Hello, React!</h1>)
```

### Understanding the Setup

- We use createRoot() from ReactDOM to create a React root container.
- The render() function takes JSX (which looks like HTML) and inserts it into the root.
- React's approach differs from traditional HTML because JavaScript manages the UI dynamically.

## First React Challenge

### Objective

- Set up a React app again from scratch.
- Render an unordered list (`<ul>`) with **two or three list items**.
- The list items should **enumerate reasons why you're excited to learn React**.

### Code

index.jsx:

```jsx
import { createRoot } from "react-dom/client"

const root = createRoot(document.getElementById("root"))
root.render(
    <ul>
        <li>React is a popular JavaScript library!</li>
        <li>It makes building UIs more efficient.</li>
        <li>It will help me become more employable!</li>
    </ul>
)
```

### Breakdown of the Solution

- We import createRoot from "react-dom/client".
- We create a root container that points to the `<div id="root"></div>` in `index.html`.
- We render an unordered list (<ul>) with three list items (<li>), each explaining a reason to learn React.

## Local Setup via Vite

Unlike simply double-clicking an HTML file to open it in a browser, modern frontend development relies on **build tools** to manage dependencies, compile code, and optimize performance.

With Vite, you can start building and experimenting with React projects locally. If you're still new to React, it’s recommended to continue practicing in **Scrimba** for hands-on learning before diving deeper into **local development and deployment**.

### Why Vite

We will use **Vite**, a **fast and lightweight** build tool recommended for modern React projects. The name **"Vite"** is French for "quick," emphasizing its **speed and efficiency** in development.

### Prerequisites

Before installing Vite, ensure you have `Node.js` and `npm` installed on your system.

#### **Check if Node.js and npm are installed**

Open a terminal and type:

```sh
node -v
```

Check if npm (Node Package Manager) is installed by running:

```sh
npm -v
```

### Setting Up a React Project with Vite

Once Node.js and npm are installed, follow these steps to create a new React project using Vite.

#### Step 1: Create a New Vite Project

Run the following command in your terminal:

```sh
npm create vite@latest
```

This command initializes a **Vite project setup wizard**.

#### **Step 2: Configure Your Project**

1. **Enter a project name** (e.g., `first-react-app`).
2. **Select a framework**: Use arrow keys to choose **React**.
3. **Choose a variant**: Select **JavaScript** (not TypeScript for now).

#### Step 3: Install Dependencies

Navigate into your project directory:

```sh
cd first-react-app
```

Install necessary dependencies:

```sh
npm install
```

#### Step 4: Start the Development Server

Run the development server using:

```sh
npm run dev
```

This will start a **live server** at `http://localhost:5173/` where you can see your React app in action.

To test this out, go to the [First React Project](src\projects\01-first-react\README.md).

### Exploring the Project Structure

Inside your **Vite-powered React project**, you will find:

- A **`src/` (source) folder** containing key files like `App.jsx` and `main.jsx`.
- A **`public/` folder** for static assets.
- A **`package.json`** file that manages project dependencies.

To start customizing your app:

1. Open `src/App.jsx`
2. Modify the JSX inside `<App />` and see changes live.

### Why Vite?

Vite is preferred over older tools like **Create React App (CRA)** because:

- **Faster startup times** – Uses **ES Modules** instead of bundling everything upfront.
- **Lightning-fast Hot Module Replacement (HMR)** – Instantly reflects changes in the browser.
- **Optimized builds** – Produces highly efficient production-ready code.

## Libraries/Frameworks

JavaScript **libraries** and **frameworks** are both essential tools in modern web development, but they serve different purposes.

### What is a Library?

A **library** is a collection of reusable code that developers can use to perform common tasks. It helps reduce the need to write **repetitive** or **complex** code from scratch.

- **Flexibility:** Libraries give you full control over when and how to use them.
- **No strict boundaries:** You can structure your application as you see fit.
- **Example:** jQuery, React (React is technically a library but is often used within a framework like Next.js).

### What is a Framework?

A **framework** is a more structured way of developing applications. It provides a **predetermined architecture** and expects developers to follow specific patterns.

- **Opinionated structure:** Frameworks define a "right" and "wrong" way to do things.
- **Strict boundaries:** You work within the rules set by the framework.
- **Example:** Angular, Vue.js, Next.js (a framework that uses React).

| **Libraries**                                       | **Frameworks**                                         |
|-----------------------------------------------------|-------------------------------------------------------|
| Collection of reusable code                         | Predetermined architecture - you follow a specified pattern of development |
| Reduces need to write repetitive/complex things from scratch | You work within the boundaries set by the framework |
| You control how/when it’s used. No/few boundaries.  | "Right" and "wrong" ways to use it. |

### Is React a Library or a Framework?

React defines itself as a **library** for building user interfaces. However, with its ecosystem (like **React Router** and **state management tools**), it can function similarly to a framework. Many developers use React within a framework like **Next.js** to structure their applications efficiently.

### Brief History of JavaScript Libraries and Frameworks

- **2006** – jQuery: Simplified cross-browser compatibility and DOM manipulation.
- **2010** – AngularJS, Ember, Backbone: Introduced structured ways of building applications.
- **2013** – React: Popularized component-based architecture.
- **2016** – Next.js, Svelte: Full-stack frameworks utilizing React and other tools.
- **2020-Present** – New frameworks like Remix, Solid, Astro, and Redwood continue to innovate.

### Why Choose React?

- **Job demand**: React has the highest demand among front-end technologies.
- **Ecosystem & community**: A vast ecosystem of npm packages, documentation, and support.
- **Less "magic"**: Unlike some frameworks, React relies on core JavaScript concepts.
- **Declarative & composable**: Makes UI development intuitive and maintainable.

### When NOT to Use a Library or Framework

- **For small projects**: If you're building a simple static site, HTML, CSS, and JavaScript might be enough.
- **Network concerns**: Frameworks add extra code, which may impact performance on slow networks.
- **Complex learning curve**: Some frameworks require a steep learning investment.
- **Existing codebase limitations**: A framework might not integrate well with legacy projects.

While libraries and frameworks have their place in web development, choosing the right tool depends on the **project requirements**, **team experience**, and **long-term maintainability**.

## React.createElement()

In React, the `createElement()` function is the core method for creating React elements. It takes three arguments:

1. **Type**: The type of element to create (e.g., a string for HTML elements or a React component).
2. **Props**: An object containing properties to pass to the element.
3. **Children**: Additional elements nested inside the created element.

### Syntax

index.jsx:

```jsx
import { createElement } from "react"
import { createRoot } from "react-dom/client"

const root = createRoot(document.getElementById("root"))
const reactElement = createElement("h1", null, "Hello from createElement!")

console.log(reactElement)

root.render(
    reactElement
)
```

returns:

```shell
{
    type: 'h1', 
    key: null, 
    props: {children: 'Hello from createElement!'}, 
    _owner: null, 
    _store: {}
}
```

## JSX

createElement() is powerful but can be cumbersome. JSX is a syntax extension that simplifies creating React elements by resembling HTML. JSX converts HTML-like code into `React.createElement()` calls behind the scenes.

index.jsx:

```jsx
import { createRoot } from "react-dom/client"

const root = createRoot(document.getElementById("root"))
const reactElement = <h1>Hello from JSX!</h1>

console.log(reactElement)

root.render(
    reactElement
)
```

## Why React

### its Composable

We have the tools to create easily reusable and interchangeable components, that can be combined in various ways to create complex systems.

Custom components can be created and reused across different parts of the application, making it easier to manage and maintain the codebase.

index.jsx:

```jsx
import { createRoot } from "react-dom/client"
const root = createRoot(document.getElementById("root"))

function MainContent() {
    return (
        <h1>"React is great!"</h1>
    )
}

root.render(
    <div>
        <MainContent />
    </div>
)
```

### its Declarative

React allows developers to describe the desired outcome without specifying the exact steps to achieve it. This declarative approach makes code more readable and easier to maintain.

imperative index.jsx:

```js
// using Vanilla JS to create h1 and attching it to dic#root
// Without using innerHTML

// Select the div with id "root"
const root = document.getElementById("root");

// Create a new h1 element
const h1Tag = document.createElement("h1");

// Set the text content
h1Tag.textContent = "This is some text";

// Add the class name
h1Tag.classList.add("header");

// Append the h1 to the div#root
root.appendChild(h1Tag);
```

declarative index.jsx:

```jsx
import { createRoot } from "react-dom/client"
const root = createRoot(document.getElementById("root"))

root.render(
    <h1 className="header">This is some text</h1>
)
```

## Random Housekeeping

## ReactFacts Project - Markup

To test this out, go to the [02-ReactFacts](src\projects\02-ReactFacts\README.md).

## Pop Quiz

1. Where does React put all of the elements I create in JSX when I call `root.render()`?

   All the elements I render get put inside the div with the id of "root"
   (or whatever other element I might select when calling createRoot)

2. What would show up in my console if I were to run this line of code: `console.log(<h1>Hello world!</h1>)`

   An object! Unlike creating an HTML element in vanilla DOM JS, what gets created from the JSX we have in our React code is a plain JS object that React will use to fill in the view.

3. What's wrong with this code:

   ```jsx
   root.render(
        <h1>Hi there</h1>
        <p>This is my website!</p>
   )
   ```

   You can only render 1 parent element at a time. That parent element can have as many children elements as you want.

4. What does it mean for something to be "declarative" instead of "imperative"?

   *Imperative* means we need to give specific step-by-step instructions on how to accomplish a task.

   *Declarative* means we can write our code to simply "describe" *what* should show up on the page and allow the rool (React, e.g.) to handle the details on *how* to put those things on the page.

5. What does it mean for something to be "composable"?

   We have small pieces that we can put together to make something
   larger or greater than the individual pieces themselves.

## Custom Components

index.jsx:

```jsx
import { createRoot } from "react-dom/client"
const root = createRoot(document.getElementById("root"))

function Page() {
    return (
        <ol>
            <li>React is a popular library, so I will be able to
            fit in with all the coolest devs out there! 😎</li>
            <li>I am more likely to get a job as a front end developer
            if I know React</li>
        </ol>
    )
}

root.render(
    <Page />
)
```

## Custom Components Challenge Part 2

index.jsx:

```jsx
import { createRoot } from "react-dom/client"
const root = createRoot(document.getElementById("root"))

function Page() {
    return (
        <div>
            <header>
                <img src="react-logo.png" width="40px" alt="React logo" />
            </header>
            <main>
                <h1>Reason I am excited to learn React</h1>
                <ol>
                    <li>React is a popular library, so I will be able to fit in with all the coolest devs out there! 😎</li>
                    <li>I am more likely to get a job as a front end developer if I know React</li>
                </ol>
            </main>
            <footer>
                <small>© 2024 Ziroll development. All rights reserved.</small>
            </footer>
        </div>
    )
}

root.render(
    <Page />
)
```

## Custom Components Quiz

1. What is a React component?

   A function that returns React elements.

2. What's wrong with this code?

   ```jsx
   function myComponent() {
       return (
           <small>I'm tiny text!</small>
       )
   }
   ```

   We need to use pascal case for the function name. It should be `MyComponent`.

3. What's wrong with this code?

   ```jsx
   function Header() {
       return (
           <header>
               <img src="./react-logo.png" width="40px" alt="React logo" />
           </header>
       )
   }

   root.render(Header())
   ```

   We need to pass the component as JSX, not as a function call. It should be `root.render(<Header />)`.

## Fragments

When we want to return multiple elements from a component, we need to wrap them in a single parent element. However, sometimes we don't want to add an extra `<div>` or other element just to wrap everything.

React provides a solution called **fragments**. Fragments allow us to return multiple elements without adding an extra parent element.

index.jsx:

```jsx
import { createRoot } from "react-dom/client"
import { Fragment } from "react"

const root = createRoot(document.getElementById("root"))

function Page() {
    return (
        <Fragment>
            // Multiple elements here
        </Fragment>
    )
}

root.render(<Page />)
```

or using the shorthand syntax:

index.jsx:

```jsx
import { createRoot } from "react-dom/client"

const root = createRoot(document.getElementById("root"))

function Page() {
    return (
        <>
            // Multiple elements here
        </>
    )
}

root.render(<Page />)
```

## Custom Components - Parent/Child Components

Creating larger components by combining smaller components is a common practice in React. This approach helps keep the codebase organized and makes it easier to manage complex UIs.

index.jsx:

```jsx
import { createRoot } from "react-dom/client"
const root = createRoot(document.getElementById("root"))

function Header() {
    return (
        <header>
            <img src="react-logo.png" width="40px" alt="React logo" />
        </header>
    )
}

function MainContent() {
    return (
        <main>
            <h1>Reason I am excited to learn React</h1>
            <ol>
                <li>React is a popular library, so I will be able to fit in with all the coolest devs out there! 😎</li>
                <li>I am more likely to get a job as a front end developer if I know React</li>
            </ol>
        </main>
    )
}

function Footer() {
    return (
        <footer>
            <small>© 2024 Ziroll development. All rights reserved.</small>
        </footer>
    )
}

function Page() {
    return (
        <>
            <Header />
            <MainContent />
            <Footer />
        </>
    )
}

root.render(
    <Page />
)
```

## Styling with Classes

## Organizing Components

## Mental outline of the project

## Initial Project Setup

## ReactFacts Project - NavBars & Styling

## ReactFacts Project - Main Content Section

## ReactFacts Project - Coloring the Bullet Points

## ReactFacts Project - Background Image

## Section 1 Recap
