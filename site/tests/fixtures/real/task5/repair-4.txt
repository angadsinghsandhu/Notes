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

Before we jump into our React Facts project, there are a few important housekeeping points to ensure everything runs smoothly.

### `.jsx` File Extension

When using React with JSX and Vite, always name your files with the `.jsx` extension.

**Reasoning:** Vite recommends `.jsx` instead of `.js` for any file that includes JSX syntax. It helps Vite efficiently bundle and optimize your project. **Example:**
  
```jsx
// Correct filename:
index.jsx

// Incorrect (though it may technically work, it's not recommended):
index.js
```

### Handling Static Images

Static images in React projects with Vite require careful handling:

- **Issue:** Relative paths (e.g., `"react-logo.png"`) work fine in Scrimba but may fail in local Vite setups.

- **Temporary Solution:** Use an absolute path from the root of your project:

  ```jsx
  <img src="/src/assets/react-logo.png" alt="React logo" />
  ```

- **Better Approach (covered later):** in Vite, the path is relative to the root of the project (i.e. from index.html), not the file itself.

### Rendering Multiple JSX Elements

JSX requires exactly one parent element when rendering multiple elements:

- **Incorrect:**

  ```jsx
  root.render(
      <img src="/src/assets/react-logo.png" alt="React logo" />
      <h1>This will throw an error</h1>
  )
  ```

- **Correct:**

  ```jsx
  root.render(
      <div>
          <img src="/src/assets/react-logo.png" alt="React logo" />
          <h1>This is React.</h1>
      </div>
  )
  ```

- **Better Practice:**
  Use semantically meaningful containers like `<main>`, `<section>`, or `<article>` instead of a generic `<div>`:

  ```jsx
  root.render(
      <main>
          <img src="/src/assets/react-logo.png" alt="React logo" />
          <h1>This is React.</h1>
      </main>
  )
  ```

  - For guidance on semantic elements, visit [MDN Documentation](https://developer.mozilla.org/en-US/docs/Web/HTML/Element).

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

Custom components in React allow us to encapsulate and reuse logic and markup, essentially letting us create our own custom HTML-like elements. Components significantly enhance flexibility, reusability, and composability in our user interfaces.

### Why Custom Components?

- **Reusability**: Write components once, reuse them everywhere.
- **Maintainability**: Change code in one place, reflecting everywhere it's used.
- **Composability**: Easily combine and organize UI elements.

So far, we've placed everything directly inside `root.render`. Now, we’ll move towards creating our own custom components.

### Creating Your First Custom Component

Creating custom components in React involves defining a JavaScript function that returns JSX:

**Basic Structure:**

```jsx
function ComponentName() {
    return (
        <div>
            {/* JSX markup here */}
        </div>
    )
}
```

**Important Conventions:**

- **PascalCase**: Custom component names should always start with a capital letter.
- **JSX Syntax**: Components are rendered with angle brackets, similar to HTML tags.

**Example:**

```jsx
function TemporaryName() {
    return (
        <div>
            <h1>This is my custom component!</h1>
        </div>
    )
}

// Rendering the component:
root.render(<TemporaryName />)
```

### Custom Components Challenge (Part 1)

**Objective:**

- Define a new custom component named `Page`.
- Return an ordered list (`<ol>`) listing reasons you're excited to learn React.
- Render this component to appear on the page.

**Code Example:**
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

**Breakdown:**

- Defined the `Page` function as a component.
- Used PascalCase naming convention.
- Returned JSX wrapped in parentheses.
- Rendered the component using angle brackets (`<Page />`).

### Common Mistakes & Best Practices

- **Mistake:** Defining but not rendering the component.

  ```jsx
  // Defined but NOT rendered—won't show up:
  function Page() {
      return (
          <ol>
              <li>Reason 1</li>
          </ol>
      )
  }
  ```

- **Correct Practice:** Always render the component explicitly.

  ```jsx
  root.render(<Page />)
  ```

- Components can be rendered as:
  - **Self-closing** (`<Component />`)
  - **Opening/closing tags** (`<Component></Component>`)

### Custom Components Challenge (Part 2)

In this second part of the challenge, we'll extend our custom `Page` component by structuring our page to resemble the React Facts project we'll build later. The goal is to organize the page into three semantic sections: **header**, **main**, and **footer**.

#### Challenge Steps

##### Step 1: Header

- Add a `<header>` element at the top of your `Page` component.
- Include an `<img>` tag inside the header.
- Provide the following attributes for the image:
  - `src` (image source path)
  - `width` (optional, but recommended)
  - `alt` (accessibility description)

##### Step 2: Main Content**

- Wrap your existing ordered list (`<ol>`) within a `<main>` tag.
- Add an `<h1>` element above the list, stating something like:  
  **"Reasons I'm excited to learn React"**

##### Step 3: Footer

- Add a `<footer>` element at the bottom of your `Page` component.
- Include simple footer text wrapped in a `<small>` tag for reduced emphasis.

#### Handling JSX Parent Elements

When adding multiple sibling elements in JSX, React requires exactly **one parent element**:

- **Incorrect (multiple siblings):**

  ```jsx
  return (
      <header>...</header>
      <main>...</main>
  )
  ```

- **Correct (wrapped in a parent element, e.g., `<div>`):**

  ```jsx
  return (
      <div>
          <header>...</header>
          <main>...</main>
          <footer>...</footer>
      </div>
  )
  ```

- A simple `<div>` is acceptable for now; we'll learn cleaner solutions later.

#### Completed Challenge Example

Here's how your final `Page` component might look:

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

**Breakdown:**

- Added a `<header>` with an image.
- Used `<main>` to semantically group the main content.
- Included an `<h1>` heading for clarity.
- Wrapped footer text in a `<small>` tag for subtle styling.

### Notes on Composability

Currently, our entire page layout is contained within a single `Page` component. You might wonder if this contradicts the composability principle in React—breaking things into smaller, reusable components.

- **You're right!** While a large single component is acceptable for initial learning, breaking the page into smaller components improves readability, maintainability, and modularity.
- We'll explore component composition and parent-child relationships shortly.

### Custom Components Quiz

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

### Fragments

When we want to return multiple elements from a component, we need to wrap them in a single parent element. However, sometimes we don't want to add an extra `<div>` or other element just to wrap everything.

React provides a solution called **fragments**. Fragments allow us to return multiple elements without adding an extra parent element. A **Fragment** is a special React component that allows us to group multiple elements without adding extra DOM nodes.

When rendering multiple sibling JSX elements, React requires a single parent element. Previously, we wrapped everything inside a `<div>`, which solved the problem but introduced unnecessary HTML elements into the DOM.

#### Why Use Fragments?

- **Avoid extra DOM elements**: Keeps HTML cleaner by removing unnecessary wrapper elements.
- **Cleaner layouts**: Useful in styling scenarios (e.g., Flexbox, Grid) where extra elements might complicate styling.

#### Using Fragments (Long Syntax)

First, import `Fragment` from React:

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

**Effect**: Renders without creating an extra DOM element (`<div>`).

#### Using Fragments (Short Syntax)

React provides a shorthand syntax for fragments using empty angle brackets (`<>...</>`):

- No imports required.
- Commonly used and recommended for brevity.

**Example (shorthand):**

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

#### Fragment vs. Div

| `<div>` Wrapper                           | React Fragment                           |
| ----------------------------------------- | ---------------------------------------- |
| Adds extra DOM element                    | Does NOT add extra DOM element           |
| Can complicate CSS/layout                 | Cleaner for layout and styling           |
| Can affect styling (Flexbox, Grid, etc.)  | Doesn't interfere with styling/layout    |

### Parent/Child Components

Creating larger components by combining smaller components is a common practice in React. This approach helps keep the codebase organized and makes it easier to manage complex UIs.

In React, creating large components with all the markup stuffed into a single component isn't always ideal, especially as the application grows. It’s often better to **break down components** into smaller, reusable pieces, making your app easier to manage, maintain, and scale.

#### Challenge: MainContent and Footer Components

**Objective:**

Further modularize your app by moving the `<main>` and `<footer>` elements into their own components:

- `MainContent`
- `Footer`

**Solution:**

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

**Breakdown:**

- Each major section of the UI (`header`, `main`, and `footer`) is moved to a separate component.
- The main `Page` component now acts primarily as a parent, rendering these child components.

#### Why Break Components into Smaller Pieces?

- **Maintainability:** Easier to manage, debug, and update individual components.
- **Readability:** Smaller components are easier to understand at a glance.
- **Reusability:** Components can be reused across different parts of the app or even in other projects.

**Note:** While breaking down a small app into multiple components might seem like premature optimization, it’s a best practice that scales well for larger, more complex applications.

#### Parent and Child Components

React organizes UI into a **component hierarchy**—much like a tree structure:

- **Parent Component:** Renders other components inside it.
- **Child Component:** Rendered inside another component.

For instance, in our example:

- `Page` is the **parent** component.
- `Header`, `MainContent`, and `Footer` are **child** components of `Page`.

**Component Hierarchy Example:**

```js
Page (Parent)
├── Header (Child)
├── MainContent (Child)
│   └── (Possible grandchild components)
└── Footer (Child)
```

This structure can extend even deeper, creating "grandparent," "grandchild," and even deeper nested components.

## Styling with Classes

Styling components in React is very similar to styling regular HTML and CSS, with just a few minor differences. Let's explore how we can add CSS styles effectively to React components.

### Mini-Challenge: Add a Navigation Bar

**Objective:**

- Inside the existing `<header>` component, add a `<nav>` element.
- Inside the `<nav>`, create an unordered list (`<ul>`) with three list items (`<li>`):
  - Pricing
  - About
  - Contact

**Example Solution:**

```jsx
function Header() {
    return (
        <header>
            <img src="react-logo.png" width="40px" alt="React logo" />
            <nav>
                <ul>
                    <li>Pricing</li>
                    <li>About</li>
                    <li>Contact</li>
                </ul>
            </nav>
        </header>
    )
}
```

This initial setup works but is visually unappealing without CSS styling.

### Adding CSS Classes in React

- Just like traditional HTML, React uses CSS classes for styling.  
- However, React uses the `className` attribute instead of the traditional `class`.

**Why `className` instead of `class`?**

- React's JSX attributes correspond to JavaScript DOM properties, and in JavaScript DOM manipulation, the property to set an element's class is `className`.

**Example:**

```jsx
<ul className="nav-list">
    <li className="nav-list-item">Pricing</li>
    <li className="nav-list-item">About</li>
    <li className="nav-list-item">Contact</li>
</ul>
```

### Using CSS with React

Because your HTML file links to a stylesheet, you can reference your CSS classes directly:

```css
.nav-list {
    list-style: none;
    display: flex;
}

.nav-list-item {
    margin-left: 10px;
    font-size: 1.1rem;
}
```

**Styling Results:**

- Removes default bullet points from the list items.
- Uses Flexbox to align list items horizontally.

### Challenge: Using Flexbox

**Objective:**

- Style the navigation bar so that the list items align horizontally.
- Align the React logo and the navigation horizontally within the header.
- Use only class selectors in CSS for best practices.

**CSS Solution Example:**

```jsx
<header className="header">
    <img src="react-logo.png" width="40px" alt="React logo" />
    <nav>
        <ul className="nav-list">
            <li className="nav-list-item">Pricing</li>
            <li className="nav-list-item">About</li>
            <li className="nav-list-item">Contact</li>
        </ul>
    </nav>
</header>
```

**Corresponding CSS:**

```css
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nav-list {
    list-style: none;
    display: flex;
}

.nav-list-item {
    margin-left: 10px;
    font-size: 1.1rem;
}
```

- `display: flex` aligns header elements horizontally.
- `justify-content: space-between` separates logo and navigation.
- `align-items: center` fixes vertical stretching of the image.

### Final Mini-Challenge: Move Inline Styles to CSS

**Objective:**

- Move the inline `width` styling from the JSX `<img>` tag into a dedicated CSS class.
- Set the logo width to `55px`.

**Updated JSX:**

```jsx
<img className="nav-logo" src="react-logo.png" alt="React logo" />
```

**CSS:**

```css
.nav-logo {
    width: 55px;
}
```

## Organizing Components

As components get larger and more complex, it's essential to organize them effectively. React components can be organized in various ways, such as:

- **File structure**: Grouping components by feature or functionality.
- **Component hierarchy**: Breaking down components into smaller, reusable parts.
- **Component composition**: Combining smaller components to create larger ones.
- **Naming conventions**: Using consistent naming for components and files.

By organizing components effectively, developers can maintain a clean and scalable codebase, making it easier to manage and extend the application.

We seperate our component into their own files called `Header.tsx`, `MainContent.tsx` and `Footer.tsx`. We export the components from their respective files and import them into the `App.tsx` file.

As your React project grows, keeping all components in a single file (`index.jsx`) quickly becomes unsustainable. A common best practice is to move components into their own separate files, which keeps your codebase organized, maintainable, and scalable.

### Moving Components into Separate Files

To keep things organized, each React component typically gets its own file named after the component.

**Example:** Moving `Header` into `Header.jsx`

- Create a new file: `Header.jsx`  
  *(Use the `.jsx` extension because the file contains JSX.)*
- Cut the `Header` component from your `index.jsx` file and paste it into `Header.jsx`.

Initially, you'll see errors because the component is no longer available in `index.jsx`.

### Exporting and Importing Components

#### Step 1: Export the Component

To make the component usable in other files, we must **export** it:

```jsx
// Header.jsx
export default function Header() {
    return (
        <header>
            <img src="react-logo.png" width="40px" alt="React logo" />
        </header>
    )
}
```

#### Step 2: Import the Component

In `index.jsx`, we **import** the component:

```jsx
// index.jsx
import Header from './Header'
```

- No curly braces needed because it’s a **default export**.
- Using `./` indicates importing from your own file (not from `node_modules`).

**Note:**  
With default exports, the name you import with doesn’t have to match the exported component exactly, but it’s best practice to keep it consistent:

```jsx
// Valid but not recommended
import WhateverComponent from './Header'
```

Then you'd render it as `<WhateverComponent />`.  
However, consistency in naming is preferred for readability and debugging.

### Quick Challenge: Moving Other Components

**Objective:**  
Move the `MainContent` and `Footer` components into their own files (`MainContent.jsx`, `Footer.jsx`) and adjust imports/exports to keep the app working.

**Solution Steps:**

1. Create new files:
    - `MainContent.jsx`
    - `Footer.jsx`
2. Move components into their respective files and add exports:

   ```jsx
   // MainContent.jsx
   export default function MainContent() {
       return (
           <main>
               <h1>Reasons I'm excited to learn React</h1>
               <ol>
                   <li>React is popular!</li>
                   <li>It boosts job opportunities.</li>
               </ol>
           </main>
       )
   }
   ```

   ```jsx
   // Footer.jsx
   export default function Footer() {
       return (
           <footer>
               <small>© 2024 Ziroll development. All rights reserved.</small>
           </footer>
       )
   }
   ```

3. Import these components back into your `index.jsx`:

   ```jsx
   // index.jsx
   import Header from './Header'
   import MainContent from './MainContent'
   import Footer from './Footer'

   function Page() {
       return (
           <>
               <Header />
               <MainContent />
               <Footer />
           </>
       )
   }

   root.render(<Page />)
   ```

After these changes, the `index.jsx` file becomes cleaner, more manageable, and easy to read.

### Organizing Components into Folders

In real-world projects, it’s common practice to place components into a dedicated `components` folder:

```txt
project-root/
├── components/
│   ├── Header.jsx
│   ├── MainContent.jsx
│   └── Footer.jsx
└── index.jsx
```

Then, adjust your imports accordingly:

```jsx
import Header from './components/Header'
import MainContent from './components/MainContent'
import Footer from './components/Footer'
```

## Mental outline of the project

Before starting a new project, it helps to form a clear mental model of what needs to be built. At this stage, the goal isn’t detailed code, but understanding the overall layout, components, and structure. This helps identify any potentially tricky areas upfront.

### 🧠 **Challenge**

Take a moment to mentally outline how you might:

- Separate the page into different sections/components.
- Choose appropriate HTML elements.
- Plan your CSS styling and layout approach.

### General Approach

In web development, there’s always more than one correct way to structure a project. Here’s one possible approach:

### Identifying Main Components

Two main parent components stand out:

1. Header - with the React logo and text
2. MainContent - Heading with the list of reasons to learn React and a background image

### Component Breakdown

#### Header Component

The header is simple and might include:

- A logo image (`<img>` element).
- Brand name text (`<span>` element).

Both elements can be inline and easily aligned.

**Potential CSS Layout Technique:**

- Use **Flexbox** for clean, simple alignment.

```jsx
<header>
  <nav>
    <img src="logo.png" alt="Logo" />
    <span>ReactFacts</span>
  </nav>
</header>
```

*(Wrapping these elements inside a `<nav>` is logical, as clicking the logo typically returns users to the homepage.)*

#### MainContent Component

The main content area might consist of:

- An `<h1>` heading.
- An unordered list (`<ul>`) with multiple list items (`<li>`).
- Background styling (possibly a partial background image).

```jsx
<main>
  <h1>Reasons I'm excited to learn React</h1>
  <ul>
    <li>Reason 1</li>
    <li>Reason 2</li>
    <li>Reason 3</li>
  </ul>
</main>
```

### 🧱 Layout Structure

A good practice is to wrap major sections in a single **container div** for styling purposes:

```html
<div class="container">
  <header>...</header>
  <main>...</main>
</div>
```

This structure makes applying layout and styling easier.

### 🧭 Project Structure (React Components)

The project's structure could look like this:

- **`App` Component** (root component)
  - Renders **`Header` Component**
  - Renders **`MainContent` Component**

This modular structure aligns with best practices for scalability and readability.

```jsx
// App.jsx
function App() {
  return (
    <div className="container">
      <Header />
      <MainContent />
    </div>
  )
}

export default App
```

### Why Use a Mental Outline?

- Clarifies the overall design and layout.
- Helps identify potential issues early.
- Simplifies the development process by providing clear direction.

## Initial Project Setup

We use `main.jsx` as the entry point for our React project. It creates the `root` container and renders the `App` component and add project configurations. The main parts of the project are stored in the `App` component.

We'll start by setting up the basic structure of our React project. At this stage, our goal is to establish a clean foundation by separating configuration and rendering logic from our actual app components.

### Step-by-Step Setup

Follow these steps to initialize your project clearly and efficiently:

#### 1. Create an `App.jsx` file

- Place it at the same level as your existing `index.jsx`.
- This `App.jsx` will serve as the main "parent component" aggregating all other components.

**Structure of `App.jsx`:**

```jsx
export default function App() {
    return (
        <h1>App component here</h1>
    )
}
```

#### 2. Update `index.jsx` to Render `<App />`

Modify your existing `index.jsx` to import and render the new `App` component:

```jsx
import { createRoot } from "react-dom/client"
import App from "./App"

const root = createRoot(document.getElementById("root"))
root.render(<App />)
```

Check your app to ensure it displays correctly.

### Creating Component Structure

To organize our components, we'll create a dedicated `components` folder.

#### 3. Set Up Component Folder

Create a new folder named `components` containing two files:

- `Navbar.jsx`
- `Main.jsx`

**Inside each component file, initially render simple placeholders:**

`components/Navbar.jsx`

```jsx
export default function Navbar() {
    return (
        <h1>Navbar component here</h1>
    )
}
```

`components/Main.jsx`

```jsx
export default function Main() {
    return (
        <h1>Main component here</h1>
    )
}
```

**4. Import and Render Components in `App.jsx`**

Replace the placeholder markup in `App.jsx` by importing and rendering the new components:

```jsx
import Navbar from "./components/Navbar"
import Main from "./components/Main"

export default function App() {
    return (
        <>
            <Navbar />
            <Main />
        </>
    )
}
```

Make sure to wrap components with a React Fragment (`<>...</>`), as JSX requires a single parent element.

### Adding Google Fonts (Inter)

To enhance the project's typography, we'll add the **Inter** font from [Google Fonts](https://fonts.google.com/):

**5. Add Inter Font to `index.html`**

- Choose the **Inter** font with weights **400, 600, and 700** (or the Variable Font variant).
- Paste the provided `<link>` elements into the `<head>` section of your `index.html`, above other stylesheet links:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
    <!-- Google Fonts: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="/index.css" />
    <title>React App</title>
  </head>
  <body>
    <div id="root"></div>
    <script src="/index.jsx" type="module"></script>
  </body>
</html>
```

(Note: You can choose either individual font weights or the newer Variable Font option.)

### ✅ **Checkpoint**

After completing these steps, your project structure should look like:

```txt
project-root/
├── index.html
├── index.jsx
├── App.jsx
├── components/
│   ├── Navbar.jsx
│   └── Main.jsx
└── index.css
```

Your page should correctly display the Navbar and Main placeholder components.

## ReactFacts Project

### NavBars & Styling

Go to the [02-ReactFacts](src\projects\03-ReactFacts\src\assets\components\Navbar\Navbar.tsx) to see this implementation.

Throughout the upcoming challenges, we'll primarily focus on CSS styling. Styling is a fundamental part of frontend development, making these exercises particularly valuable. If you're already comfortable with CSS, feel free to skip ahead. However, if you're less confident or unfamiliar with closely following a Figma design, it's strongly recommended to complete these styling challenges for good practice.

#### 📌 **Implementing Navbar HTML**

Replace any placeholder markup in your Navbar component with the following semantic structure:

**`components/Navbar.jsx`:**

```jsx
export default function Navbar() {
    return (
        <header>
            <nav>
                <img src="../imgs/react-logo.png" alt="React logo" />
                <span>React Facts</span>
            </nav>
        </header>
    )
}
```

- Ensure the image path (`src`) is correctly set according to your project structure.
- Use a descriptive `alt` attribute for accessibility.

#### **Navbar CSS Styling**

Follow these styling instructions carefully, referencing the provided Figma design for precise colors, spacing, and typography details:

- **Header Styles:**

  ```css
  header {
      height: 90px;
      padding: 30px 25px;
      background-color: /* use color from Figma */;
  }
  ```

- **Navigation Flexbox Layout:**

  ```css
  header nav {
      display: flex;
      align-items: center;
  }
  ```

- **Logo Image Styles:**

  ```css
  header nav img {
      width: 40px;
      margin-right: 7px; /* Spacing between logo and text */
  }
  ```

- **Navbar Text Styles:**

  ```css
  header nav span {
      font-size: 1.4rem; /* Approximately 22.25px */
      font-family: 'Inter', sans-serif;
      font-weight: 700; /* Bold weight from Figma */
      color: /* use color from Figma */;
  }
  ```

- Remember: In JSX, use `className` instead of `class` if adding CSS classes.

#### **Final Checkpoint**

At this stage, your Navbar should visually match the design closely, with:

- Proper vertical alignment of the logo and text.
- Correct spacing, colors, and font properties.
- Semantic HTML markup enhancing accessibility and SEO.

### Main Content Section

Similar to the navbar challenge, this section primarily focuses on styling and markup, matching our provided Figma design. We'll handle two specific design aspects separately in later challenges:

- **Custom-colored list bullets**
- **Side-positioned React logo image**

For now, focus only on matching the general layout, typography, spacing, and colors of the main content.

#### Main Content HTML

Create semantic HTML markup within your **`Main.jsx`** component:

```jsx
export default function Main() {
    return (
        <main>
            <h1>Fun facts about React</h1>
            <ul className="facts-list">
                <li>Was first released in 2013</li>
                <li>Was originally created by Jordan Walke</li>
                <li>Has well over 100K stars on GitHub</li>
                <li>Is maintained by Facebook</li>
                <li>Powers thousands of enterprise apps, including mobile apps</li>
            </ul>
        </main>
    )
}
```

- Using the `<main>` element helps semantically indicate primary page content.
- Adding a `className` to the `<ul>` aids targeted styling.

#### Main Content CSS Styling

Apply the following CSS to match the design closely:

**Base Styles (`index.css`):**

```css
body {
    background-color: /* dark background color from Figma */;
    color: white; /* Ensures readability of all text */
    font-family: 'Inter', sans-serif;
    margin: 0;
}
```

**Main Content Styles:**

```css
main {
    padding: 57px 27px;
}

/* Remove default margin from <h1> */
main h1 {
    margin: 0;
    font-size: 2.4rem; /* ~39px from Figma */
}

/* Style list */
.facts-list {
    margin-top: 46px; /* Space between h1 and list */
    max-width: 400px; /* Prevent overly wide lists */
    padding-left: 20px; /* Default list indent */
}

/* List item spacing */
.facts-list li {
    padding-block: 10px; /* 20px spacing between items without collapsing */
    line-height: 19px; /* From Figma design */
}
```

**Note:**

- Use `padding-block` for consistent vertical spacing (avoiding margin collapse issues).
- Background color applied to `<body>` ensures consistent coloring throughout the entire page.

#### Skipped Elements

These will be handled separately in upcoming challenges:

- Custom bullet colors/sizes
- Side React logo positioning

#### Checkpoint

Your main content should now have:

- A clearly visible heading and list.
- Correct typography and colors as per Figma.
- Consistent vertical spacing between list items and other elements.
- A solid semantic HTML structure.

Remove any temporary challenge text, and prepare for styling the remaining design elements in the next challenges.

### Coloring the Bullet Points

We originally planned a CSS challenge to make the bullets larger and colored blue to match the design. You're still welcome to try this yourself as extra practice!

#### Common Approach (Advanced)

Typically, custom bullet points are styled by:

- Removing default list styling (`list-style: none`).
- Using the `::before` pseudo-element to create custom bullet shapes.

However, this approach can feel overly detailed for our React-focused course.

#### Simpler Approach: Using `::marker`

A simpler alternative is the built-in CSS pseudo-selector **`::marker`**, which lets you style bullet points directly without extra elements or complicated markup:

```css
.facts-list li::marker {
    color: /* Blue color from "React Facts" text */;
    font-size: 1.5rem; /* Balanced size to avoid alignment issues */
}
```

- This approach colors bullets easily to match the design.
- A font size around `1.5rem` helps maintain visual alignment.

#### Alignment Issue (Heads-Up!)

Increasing the bullet size too much can cause misalignment. For instance:

- `font-size: 4rem` clearly misaligns the bullets.
- After experimentation, approximately `1.5rem` is recommended.

Feel free to reach out on the Scrimba Discord if you discover a better solution!

#### Final Decision & Recommendation

We'll use:

- Bullet color matching the blue from the design.
- Bullet size at approximately `1.5rem` for best visual balance.

This solution deviates slightly from the Figma mockup (approximately `2rem`) but maintains better alignment.

### Background Image

The final design touch for our React Facts project is to add the React logo image, positioned as a background element within our `<main>` section.

Since this image isn't semantically important (i.e., it doesn't need to be accessible by screen readers or keyboard users), we'll use the CSS `background-image` property instead of a regular `<img>` element.

#### Setup and Housekeeping

- A new image file (`react-logo-half.png`) has been provided.
- For better organization, create an `images` folder (if not already created) and place your logo images there.
- Update any existing image references, such as in the navbar:

  ```jsx
  <img src="/images/react-logo.png" alt="React logo" />
  ```

#### Implementing the Background Image

Use the following CSS directly on the `<main>` element:

```css
main {
    background-image: url(/images/react-logo-half.png);
    background-repeat: no-repeat;
    background-position: right 70%;
}
```

**Explanation:**

- `background-image`: Sets the image as the background.
- `background-repeat`: Prevents the image from repeating.
- `background-position`: Positions the image to the right horizontally, and vertically slightly below center (`70%`) to match the Figma design.

#### ⚙️ **CSS Shorthand (Optional)**

If you prefer shorthand, all properties can be combined into a single line:

```css
main {
    background: url(/images/react-logo-half.png) no-repeat right 70%;
}
```

(Note: Shorthand order can sometimes be confusing; using separate properties is fine if preferred.)

#### Design Considerations

Currently, the layout isn't optimized for mobile or larger screens. The image positioning might visually break if the viewport is significantly resized. However, that's beyond the scope of this React-focused course.

#### Final Checkpoint

At this point, your React Facts project should:

- Closely match the provided Figma design.
- Have semantic HTML structure.
- Use CSS effectively for styling and layout.

## Section 1 Recap

It might seem small right now, but these initial steps—building a static page with React—are crucial milestones on your React learning journey.

### Here's What We've Covered

- **Why React?**  
  We explored why React matters and why it's a powerful tool to add to your skillset.

- **Composability and Declarative UI**  
  We discussed React's composability, allowing you to build modular, maintainable applications. We also explored React's declarative approach, significantly improving the developer experience.

- **Project Setup with React and Vite**  
  We practiced setting up React projects multiple times (maybe more than you'd like!) and introduced local setup with **Vite**. While Scrimba is great for learning interactively, we also emphasized the importance of knowing how to build projects locally on your own machine.

- **JSX and `React.createElement`**  
  We discussed how JSX is syntactic sugar for `React.createElement`, ultimately generating JavaScript objects that describe your UI. JSX provides a clean, familiar syntax that makes building React components intuitive.

- **Custom Components**  
  We built our own custom components, diving into React's core strength—component composability. We've only scratched the surface here, but this foundational understanding will be crucial as you move forward.

- **CSS Styling**  
  We spent significant time styling our app to ensure it's visually appealing, reinforcing the importance of CSS in frontend development.

### 🎉 **Celebrate Your Success**

If you haven't already, **join the Scrimba Discord community!**  
Share your accomplishment in the **#today-i-did** channel:

- Connect with others learning React.
- Celebrate your progress and get feedback.
- Stay motivated for the next sections of the course.
