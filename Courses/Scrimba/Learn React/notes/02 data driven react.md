# Data-Driven React

Understanding how to pass and manage data in React components is crucial for building dynamic applications. In this section, we will explore props, reusable components, passing data, and rendering arrays in React.

We will achieve this by working on a **Travel Journal** project, where we will learn how to manage and pass data effectively between components.

## Section 2 Intro

With the foundational concepts and syntax for creating static pages in React under our belt, we're now ready to advance and begin developing **data-driven React applications**.

In our previous project, all the content displayed on the page was **hard-coded** directly into the markup. While hard-coded text still has its place—especially for content that rarely changes—the real power of React emerges when we move beyond static content.

React's strength isn't just in its **composability** and **declarative nature**, but also in its capability to **handle dynamic data**, enabling us to create **reusable components**.

In this section, we'll work on building a **Travel Journal** project. Unlike the previous static page, the information in this project will be dynamically rendered from regular JavaScript files containing data structured as **objects and arrays**.

In the completed project example, you'll find a dedicated `data.js` file where all the necessary information is stored. Our React application will access this array of data, iterate over it, and dynamically generate React components, seamlessly inserting the data into appropriate locations.

Take a moment to explore the provided codebase to gain a better understanding of its structure. Remember, you can also click on the project's screenshot to open the corresponding **Figma design**, ensuring you utilize the precise colors and spacing provided.

Throughout this section, we'll first discuss **why reusability matters**, recognizing it as a fundamental design pattern you'll encounter on nearly every modern website.

Next, we'll explore React’s primary feature that facilitates component reusability and dynamic rendering: **props**. By thoroughly understanding props, we'll learn how to convert arrays of data into dynamically generated React components.

And naturally, as with every Scrimba course, expect plenty of **hands-on challenges** to reinforce your learning along the way.

## Travel Journal - Header

We'll kick off our Travel Journal project with an easy, straightforward challenge to warm up—mostly reviewing concepts you've already learned.

Your goal is simple: **build the header section** for the Travel Journal project.

Start by clicking on the provided screenshot to open the design in **Figma**. This gives you clear visuals and specific details about what's required. The instructions below will guide you step-by-step.

### 🛠️ Already Set Up for You

To simplify things, a few resources have already been prepared:

- **Inter Google Font** is imported in `index.html`.
- **Globe image** (`globe.png`) is provided and ready for you to use.

You're free to style this header however you prefer. Given the project's small size, you can choose either class names or element selectors. Just remember to use **semantic HTML** to enhance readability and accessibility.

If it's been a while since you completed section one, use this as a refresher to regain confidence!

### Step-by-Step Walkthrough

1. **Create the App component**:
   - Make a new file called `App.jsx`.
   - Import and render `<App />` into your main entry file (`index.js` or `main.jsx`).

      ```jsx
      export default function App() {
          return <h1>I’m the App component</h1>;
      }
      ```

   Save and verify everything runs smoothly.

2. **Create the Header component**:
   - In your project directory, create a `components/` folder.
   - Inside `components/`, create a new file: `Header.jsx`.

   ```jsx
   export default function Header() {
       return <h1>I’m the Header component</h1>;
   }
   ```

   Import and render `<Header />` inside `App.jsx`.

### Making It Semantic & Styled

Let’s enhance the `Header.jsx` file further:

- Replace the basic `<h1>` with a semantic `<header>` element.
- Inside `<header>`:
  - Add an `<img>` tag pointing to `"../globe.png"`.
  - Include an `<h1>` with the text `"my travel journal."`

Initially, your globe icon might blend into a white background, making it invisible. Temporarily set a red background on the header to verify its placement.

Use CSS **Flexbox** for clean alignment and centering. Add spacing, adjust font size (`0.9rem`), font weight (`500`), and font family (`Inter`).

Key styling points:

- Image: Add `alt="globe icon"`, width: `24px`, margin-right: `7px`.
- Header height: `55px` to match the Figma design.

### Finishing Touches & Additional Practice

If you're already confident with your CSS skills, you might skip further styling instructions. However, if you'd like extra practice—or insights into other styling approaches—follow along to refine:

- Precise header height (`55px`).
- Accurate image and text styling.
- Flexbox layout for a polished look.
- Matching colors, fonts, and spacing exactly as specified in Figma.

After completing and polishing your header, **check off this challenge ✅**.

## Travel Journal - Entry Component

The primary goal of this exercise is to demonstrate that, with our current knowledge, we're not quite ready to fully harness React's true potential. Right now, we'll focus on creating a **hardcoded instance** of an `Entry` component, highlighting where we currently stand and where we'll soon go.

### Project Setup (Already Done for You)

To simplify your workflow, the following preparations have been completed:

- **`Entry.jsx` file** is already created.
- **Marker icon** (`marker.png`) is included in a new `images` folder.
- **Globe image** (`globe.png`) was moved to the `images` folder and references updated.
- A `japan.md` file is provided temporarily to reduce tedious copying and pasting. It contains the initial content you'll need.

### Your Task

Render **one instance** of the `Entry` component right below the existing `Header` component in your `App.jsx`. Figuring out the exact placement will be a small but manageable challenge.

For now, it's fine to hardcode the data into the component. The intention here is simply to expose the limitations of this approach—setting the stage for the next lessons.

### Step-by-Step Guide

#### 1. **Create Your Entry Component Structure:**

- Export a default function named `Entry` from `Entry.jsx`.
- Wrap the component in an `<article>` tag for semantic clarity.

    ```jsx
    export default function Entry() {
        return (
            <article>
                {/* content will go here */}
            </article>
        );
    }
    ```

#### 2. **Add Main Image (Mount Fuji):**

- Wrap the image in a container `div` (e.g., `className="main-image-container"`).
- Set fixed dimensions (`width: 125px`, `height: 168px`) on the container.
- Use `object-fit: cover` on the image to handle sizing issues.
- Add `overflow: hidden` and `border-radius: 5px` to the container.

```jsx
<div className="main-image-container">
    <img src="your-image-source" alt="Mount Fuji" />
</div>
```

#### 3. **Build the Top-Row Content:**

- Include the **map marker icon**, **location name (Japan)**, and a link labeled **"View on Google Maps"**.
- Use Flexbox for alignment and spacing.

```jsx
<div className="entry-header">
    <img src="../images/marker.png" alt="map marker icon" />
    <span>Japan</span>
    <a href="#">View on Google Maps</a>
</div>
```

#### 4. **Add Title, Date, and Journal Text:**

- Insert the title (e.g., "Mount Fuji") as an `<h2>`.
- Include the date (e.g., "12 Jan 2021") and journal description within `<p>` tags.

```jsx
<h2>Mount Fuji</h2>
<p className="entry-date">12 Jan 2021</p>
<p className="entry-description">Your journal content here...</p>
```

#### 5. **Resolve Flexbox Issues:**

- Apply `flex-shrink: 0` to the image container to prevent layout breaking.

### Rendering in App Component

Now, import and render your `Entry` component within `App.jsx`, directly below the `Header` component. Since React components can't directly return multiple sibling elements, wrap them in a React fragment (`<>...</>`):

```jsx
import Header from './components/Header';
import Entry from './components/Entry';

export default function App() {
    return (
        <>
            <Header />
            <Entry />
        </>
    );
}
```

### Wrapping Up & Reflecting on Hardcoding

By this stage, your journal entry component should render nicely, aligning closely with the provided design. It doesn't need to be pixel-perfect yet, as styling refinements will follow.

This exercise intentionally highlights the **limitation** of manually hardcoding data within components. If we wanted additional entries, we'd have to repeatedly copy and paste—obviously not an efficient approach.

## Problem - Not Reusable

Right now, our `Entry` component isn't reusable. If we wanted to add another journal entry by placing a new instance of the `Entry` component in our `App.jsx`, we'd end up seeing another identical trip to Mount Fuji. This is because all our information is currently **hardcoded** directly into the component.

This clearly isn’t ideal. We want our Travel Journal to feature **multiple destinations**, not just repetitions of the same trip. This highlights the need for creating **reusable components**.

### The Importance of Reusable Components

Reusable components are foundational to modern web applications and appear across the internet. Consider these familiar examples:

- **Amazon.com**: New products are displayed using a consistent structure—badge icon, image, product name, rating, and price—though the data varies for each item.
- **IMDb**: Movies appear as consistent cards. The structure remains unchanged, even as the data (movie title, rating, poster image) changes.
- **Apple's Website**: Categories consistently reuse the same format (image, title, repeat), despite the data differing each time.

This is the core of reusability—same structure, different data.

When IMDb adds a new movie, developers don't manually rewrite HTML for each new release. Instead, the content is **data-driven**. The UI updates automatically as new data enters the database, leveraging reusable structures.

### Current Limitations in Our Entry Component

Our current `Entry` component demonstrates exactly why hardcoding data is limiting:

- It's impossible to represent different data without manual duplication and modification.
- Each additional destination would require copying and editing the same component repeatedly, which is inefficient and error-prone.

Clearly, this isn't scalable.

### Introducing Props

To overcome these limitations, React offers a powerful concept called **props**.

From my experience teaching React, I've noticed that understanding props is often the first significant challenge for beginners. For that reason, we’ll approach props carefully and methodically—breaking down the concept into manageable steps, reinforced with practical coding exercises.

By the end of this section, you'll clearly understand:

- How **props** function.
- How they facilitate creating flexible, reusable components.
- How to efficiently manage data-driven UIs in React.

## Props Part 1: Understanding the Concept

Let’s begin by grasping the foundational concept of **props** in React.

Imagine a simple `index.html` file that doesn't yet involve React. Take a closer look at these plain HTML elements, and see if you can spot what's missing:

- **Anchor (`<a>`) tag**:
  - Currently, the `<a>` tag lacks an `href` attribute. Without it, the anchor is essentially useless since it can't direct users to another page (e.g., `https://google.com`).

- **Image (`<img>`) tag**:
  - Without specifying the `src` attribute, the browser doesn't know which image to render. The `src` attribute must provide either a local path or a link to an image online.

- **Input (`<input>`) element**:
  - Alone, an input element defaults to a simple text box. This is already functional, but we can greatly enhance it by adding attributes like:
    - `placeholder`: Shows guiding text inside the input box (e.g., `placeholder="First Name"`).
    - `type`: Changing this attribute dramatically changes the element’s purpose and appearance:
      - `type="submit"` turns it into a button.
      - `type="radio"` makes it a radio button.

Each of these examples shows that adding attributes to HTML elements significantly enhances their functionality and flexibility.

### Parallel with JavaScript Functions

Consider a JavaScript function named `addTwoNumbersTogether`. Suppose it looks like this:

```js
function addTwoNumbersTogether() {
  return 1 + 2;
}
```

While this function works syntactically, it always returns `3` and thus isn't very useful. It has no flexibility or reusability.

If we modify the function to accept parameters, it becomes much more powerful:

```js
function addTwoNumbersTogether(a, b) {
  return a + b;
}
```

Now, the function can dynamically add **any two numbers** provided. Just by introducing parameters, we've dramatically increased its versatility.

### 🚀 Introducing React Props

In React, **props** serve a similar purpose—they are like the attributes we add to HTML elements or the parameters we pass into JavaScript functions.

- **Props** are how we pass data into components, making those components **dynamic and reusable**.
- Components without props (just like HTML elements without attributes or JS functions without parameters) are limited and inflexible.

With this foundational understanding, we can dive deeper into React props and fully grasp how they empower React components.

Before moving forward, let’s explore one more visual analogy to further solidify our understanding of props.

## Props Part 2: Reusable Components

Let’s deepen our understanding of **props** by visualizing them in action.

Imagine looking at a screenshot from an older version of **YouTube**. As you glance around YouTube—or virtually any modern web application—you'll start noticing repeated patterns. The page often consists of the same structure, displayed multiple times, each with different data.

Take, for example, the **top playlist** section on YouTube. Each video listed there follows the same consistent structure:

- An **image** thumbnail at the top.
- Bold **title text** beneath the thumbnail.
- A **view count** displayed prominently.
- Possibly a small **timestamp** in the bottom-right corner.

Each of these repeated blocks can be viewed as a distinct, reusable component—a **video tile**.

### How Reusable Components Work

When a new video is uploaded to YouTube, developers aren't manually writing HTML for each entry. Instead:

- All video information (**thumbnail, title, views, timestamp**) is stored in a **database**.
- A single, **flexible, reusable component** is utilized to dynamically fetch and render this data for each video tile.

This approach allows each video tile to appear unique, despite using the same underlying component.

### Nested Reusable Components

Reusable components often aren't isolated; they're frequently **nested** within other components.

Continuing our YouTube example:

- Multiple **Video Tiles** are grouped together into playlists or categories.
- Each playlist or category can itself be another reusable component—like a `VideoList` component—that contains multiple `VideoTile` components.

You'll notice this nested, reusable structure across numerous popular websites:

- **Apple’s website**, for instance, displays vertical menu sections with icons and titles—each section likely uses a reusable component.

### Why This Matters

Reusable components allow us to:

- **Avoid repetitive code**.
- Create **dynamic, data-driven UIs**.
- Build **scalable applications** that easily handle new data.

## Aside: JS inside JSX

Before diving into using **props**, there’s one more important concept we need to cover: how to effectively use JavaScript inside JSX.

We've already learned that JSX syntax closely resembles HTML and allows us to easily create elements. Anything we put between the opening and closing JSX tags—whether plain text or nested elements—will be rendered directly on our web page.

However, often you'll need to display dynamic JavaScript values or variables within your JSX. For example, suppose you have two variables:

```jsx
const firstName = "Joe"
const lastName = "Shmo"
```

Instead of displaying a static message like `"Hello World"`, you'd prefer a dynamic greeting like `"Hello Joe Shmo"`.

### How to Use JavaScript Inside JSX

Initially, you might attempt something like plain string concatenation (`firstName + " " + lastName`), just as you'd do in vanilla JavaScript. But React won't interpret that correctly—it'll treat it as literal text.

Fortunately, React makes embedding JavaScript easy. Simply wrap your JavaScript expression in **curly braces `{}`**:

```jsx
<h1>Hello {firstName} {lastName}</h1>
```

When saved, this renders exactly as desired:

```txt
Hello Joe Shmo
```

### Quick Challenge

Update this JSX snippet to dynamically display `"Hello Joe Schmo"` without any plain text or extra characters:

```jsx
<h1>Hello {firstName} {lastName}</h1>
```

### What’s Actually Happening Here?

When JSX gets transpiled to regular JavaScript, it recognizes curly braces `{}` as signals to interpret what's inside as JavaScript.

For example:

```jsx
<h1>Hello {firstName} {lastName}</h1>
```

React sees the `<h1>` as JSX ("JSX land"), and when it encounters `{firstName}`, it briefly switches context into pure JavaScript ("JavaScript land") to interpret that expression before returning to JSX.

You can even run more dynamic code inside curly braces, provided it returns a valid value.

### Example: Displaying Current Time

Suppose you want a greeting displaying the current hour, such as:

```txt
It is currently 3 PM
```

You can achieve this by using JavaScript directly inside JSX:

```jsx
const date = new Date()
const hours = date.getHours() % 12

<h1>It is currently {hours}</h1>
```

However, to improve readability and maintain a clear separation of concerns, it's often best practice to place computations **above the return statement**:

```jsx
const date = new Date()
const hours = date.getHours()

const timeOfDay = hours < 12 ? "morning" :
                  hours < 17 ? "afternoon" :
                  hours < 21 ? "evening" : "night"

<h1>Good {timeOfDay}</h1>
```

This prevents overly complicated logic from cluttering your JSX.

### Final Challenge

Modify your JSX code to use the dynamically calculated `timeOfDay` instead of hard-coding a greeting:

```jsx
<h1>Good {timeOfDay}</h1>
```

## Props Part 3: Create a Contact Component

To learn the syntax of using **props** in React, we'll use a small **contact book** example.

Currently, the contacts are all hardcoded directly inside `App.jsx`, each wrapped in an `article` element. Each article represents a single contact card. While this approach is acceptable for a small-scale app, it's certainly not practical if we intend to scale up beyond just a few contacts.

### Your Challenge

To get comfortable with props, let's start with a straightforward challenge:

1. **Create** a new component named `Contact` in a separate file (`Contact.jsx`).
2. **Move** the structure from one of the existing contact articles into this new `Contact` component.
3. **Import** the `Contact` component back into `App.jsx` and **render four instances** of it.
4. Once moved, you can **delete** the original four hardcoded articles.

Don’t worry about the contact data itself for now—we’ll fix that shortly.

While rendering these four instances, think ahead: there won’t be any syntax errors, but there will be an obvious bug. Can you anticipate it?

### 🛠️ Step-by-Step Solution

**Step 1: Create `Contact.jsx`**

Create a new file named `Contact.jsx`. Inside, export a simple functional component:

```jsx
export default function Contact() {
  return (
    <article>
      {/* Paste your chosen contact card's JSX here */}
    </article>
  )
}
```

**Step 2: Modify `App.jsx`**

- Import the `Contact` component at the top of `App.jsx`:

```jsx
import Contact from "./Contact"
```

- Replace your four hardcoded articles with four instances of the `<Contact />` component:

```jsx
export default function App() {
  return (
    <div>
      <Contact />
      <Contact />
      <Contact />
      <Contact />
    </div>
  )
}
```

### Anticipating the Bug

Before saving your changes, consider: what will you now see on the screen?

After saving, you'll notice the issue clearly: you'll have **four identical contacts (e.g., four Mr. Whiskersons)**.

As adorable as Mr. Whiskerson might be, we certainly want variety in our contacts—not the same contact repeated four times!

### Why This Happens

This issue arises because we moved the hardcoded contact data directly into the `Contact` component. Each instance of the component now renders the same fixed data.

This situation is analogous to creating a JavaScript function that always returns the same result, such as:

```js
function addTwoNumbers() {
  return 1 + 2
}
```

The function isn't flexible because the values are hardcoded.

To fix this, we’d make the function reusable by adding **parameters**:

```js
function addTwoNumbers(a, b) {
  return a + b
}
```

Similarly, our React `Contact` component needs to accept **props**—allowing each instance to render **unique data**.

### 🚀 Next Steps

Now that we've set up our contact card, in the next lesson, we’ll learn how to **pass data into our `Contact` component using props**.

Afterward, we'll explore how to **receive and use that data** inside the component.

## Props Part 4: Passing Data into a Component

We need a method to pass **data** into our `Contact` component. Without this ability, we’d be forced to hard-code everything directly inside the component—defeating the purpose of reusable components.

Fortunately, React provides an intuitive mechanism for this, especially familiar if you've used HTML.

### Props

In HTML, elements like `<link>` can accept **attributes** (e.g., `href`) that change their behavior or content. React has a similar concept called **props** (short for properties).

However, unlike HTML—which restricts you to attributes defined by the spec—React allows you to pass any **custom props** you want to your components, named freely and assigned with any value.

### What Data Should We Pass?

Pass in whatever data your `Contact` component needs to render dynamically:

- **Image** (profile picture)
- **Name**
- **Phone number**
- **Email**

This data should never be hard-coded if your goal is reusability.

### Example: Passing an Image Prop

Instead of generic or arbitrary props like this:

```jsx
<Contact whateverIwant="..." />
```

Use descriptive, meaningful props:

```jsx
<Contact img="images/mr-whiskerson.png" />
```

At this point, we aren't yet using these props inside the `Contact` component. We'll cover how to do that soon, but right now, our focus is strictly on passing data into components.

### Passing Multiple Props

React components often accept multiple props. For readability and clarity, it's best to format them across multiple lines:

```jsx
<Contact
  img="images/mr-whiskerson.png"
  name="Mr. Whiskerson"
  phone="(212) 555-1234"
  email="mr.whiskerson@example.com"
/>
```

Here, we're using strings as prop values. React supports other data types, but strings work perfectly for this scenario.

### Wrapping Up: Separation of Concerns

Once all the data is added, notice how clear the roles become:

- `App` component: responsible for managing and passing **data**.
- `Contact` component: handles **layout and styling**.

This clear separation helps keep your code organized, scalable, and easy to maintain.

- Want to change the design? Modify the `Contact` component.
- Need to update the data or content? Update props inside the `App` component.

### ⚠️ Final Note

If you hit save and still see four identical cards—like four Mr. Whiskersons—don't worry! We haven't covered how to **use props** within our component yet.

## Props Part 5: Receiving Props in a Component

In the previous lesson, we learned how to pass custom data into React components using **props**—similar to HTML attributes, but with far greater flexibility. Unlike HTML attributes, which must follow a strict specification, React lets us create any custom props we want, naming them clearly and logically.

Now, the important question is: **How do we receive and use these props within our components?**

### Receiving Props in a Component

Just as a JavaScript function can receive parameters, a React component can also receive props by defining a parameter (commonly named `props`) in the component function. The `props` parameter is an object that contains all of the properties passed into the component.

Here's an example of receiving and logging props:

```jsx
export default function Contact(props) {
    console.log(props);
    return (
        <div>
            {/* component JSX here */}
        </div>
    );
}
```

When you run this code, you’ll notice that the log appears multiple times if your component renders multiple instances—each component instance receives its own `props` object.

### Understanding the `props` Object

The `props` object is a simple JavaScript object containing key-value pairs corresponding to each prop passed in. For example, if your component is used as:

```jsx
<Contact
    img="images/cat.png"
    name="Mr. Whiskerson"
    phone="(212) 555-1234"
    email="mr.whiskerson@example.com"
/>
```

Your `props` object inside the component will look like:

```js
{
    img: "images/cat.png",
    name: "Mr. Whiskerson",
    phone: "(212) 555-1234",
    email: "mr.whiskerson@example.com"
}
```

It's important that prop names match exactly across all component instances. Changing a prop name (e.g., from `img` to `image`) must be done consistently to avoid confusion or errors.

### Replacing Hard-Coded Data with Props

Once we receive props, we can replace all hard-coded data with dynamic values from the props object. Here’s how to do it correctly in JSX:

- Replace static names:

  ```jsx
  <h2>{props.name}</h2>
  ```

- Replace image sources:

  ```jsx
  <img src={props.img} alt={props.name} />
  ```

- Replace phone numbers and emails:

  ```jsx
  <p>{props.phone}</p>
  <p>{props.email}</p>
  ```

> ⚠️ **Important:** Remember, whenever embedding JavaScript expressions within JSX, wrap them in curly braces `{}`.

### Common Mistakes & Troubleshooting

If you notice unexpected behavior, such as components rendering incorrectly or data mismatches, it usually comes down to inconsistent prop names. Ensure all component instances use identical prop names.

Once you align your props correctly, your component should render exactly as intended, making your contact book **dynamic and reusable**.

### Benefits of Using Props

By leveraging props, you've successfully separated:

- **Data** (managed by the parent component)
- **Layout and Styling** (managed by the child component)

This separation makes your components:

- **Reusable**: Easily scalable for new data.
- **Maintainable**: Changes in layout or data become straightforward.

### Congratulations

You’ve just mastered one of the most critical and foundational React concepts—**props**! Props are fundamental to building organized, powerful, and scalable React applications.

## Prop Quiz! (Get it?? 😆)

1. What do props help us accomplish?

    Make a component more reusable.

2. How do you pass a prop into a component?

    <MyAwesomeHeader title="???" />

3. Can I pass a custom prop (e.g. `blahblahblah={true}`) to a native DOM element? (e.g. <div blahblahblah={true}>) Why or why not?

   No, because the JSX we use to describe native DOM elements will
   be turned into REAL DOM elements by React. And real DOM elements
   only have the properties/attributes specified in the HTML specification. (Which doesn't include properties like `blahblahblah`)

4. How do I receive props in a component?
function Navbar() {
    return (
        <header>
            ...
        </header>
    )
}

    We can receive props by adding a parameter to the function that represents the component. eg. `function Navbar(props) { ... }`

5. What data type is `props` when the component receives it?

    An object!

## Destructuring Props

By this point in the course, you're probably familiar with **object destructuring**. But let's quickly recap to make sure the concept is clear.

Imagine we have an object called `person`, containing properties like `image`, `name`, `phone`, and `email`. Typically, you'd access these properties using dot notation, like this:

```js
const person = {
    image: "mr-whiskerson.png",
    name: "Mr. Whiskerson",
    phone: "(212) 555-1234",
    email: "mr.whiskerson@example.com"
}

console.log(person.name) // "Mr. Whiskerson"
```

This approach is straightforward, but JavaScript offers a cleaner method called **destructuring**.

### Quick Recap: Object Destructuring

Destructuring allows you to easily extract specific properties from an object into their own variables. For example:

```js
const { image, name } = person;

console.log(name);  // "Mr. Whiskerson"
console.log(image); // "mr-whiskerson.png"
```

This single line:

- Declares two new variables (`image` and `name`).
- Assigns them values from the corresponding properties within the `person` object.

Note: When destructuring, the variable names **must match** the property names exactly, unless you explicitly rename them.

For example, if you wanted to rename `image` to `img`, you'd do:

```js
const { image: img } = person;
console.log(img); // "mr-whiskerson.png"
```

### Destructuring Props in React

Because `props` in React is simply an object, you can use destructuring directly in your component's parameter definition.

Instead of writing:

```jsx
function Contact(props) {
    return (
        <div>
            <img src={props.image} />
            <h2>{props.name}</h2>
        </div>
    );
}
```

You can destructure inline like this:

```jsx
function Contact({ image, name, phone, email }) {
    return (
        <div>
            <img src={image} />
            <h2>{name}</h2>
        </div>
    );
}
```

Notice we've replaced the `props` parameter with `{ image, name, phone, email }`. This creates individual variables from the `props` object properties.

### Quick Challenge: Fix the Bug

After destructuring props inline, your component might initially break because you're no longer using `props.image`, `props.name`, etc.

To fix this:

- Simply remove the `props.` prefix from all your variables inside the component.

After fixing it, your component should render perfectly again.

### Best Practices & Personal Preference

There's no significant functional difference between using `props` directly or destructuring inline. The choice depends largely on:

- **Personal preference**
- **Project/team coding standards**

However, consistency is key. Choose one approach and stick with it for clarity and readability.

For the remainder of this course, we'll typically use the full `props` object:

- It clearly distinguishes variables coming from outside (via `props`) versus variables defined within the component.
- Although slightly more verbose, it helps maintain readability, especially as our components grow more complex.

## Props Practice

In this section, we’re not starting a new React app from scratch—but we’re pretty close! Our goal is to reinforce the concept of **passing and receiving props** by building a simple page to display some of your favorite jokes.

### Challenge Overview

Your task is as follows:

1. Create a new component called `Joke` in its own file (`Joke.jsx`).
2. Import and render **4–5 instances** of the `Joke` component within your main `App` component.
3. Each `Joke` component should accept two props:
    - `setup`
    - `punchline`
4. Render these props to display the jokes clearly on your webpage.

Feel free to use your own jokes or those provided in the `jokes.md` file.

### Extra Credit

There’s an optional **bonus challenge** that involves a concept not yet covered. Completing it will require external research—give it a shot if you feel ready!

### Implementation Walkthrough

Follow these step-by-step instructions for clarity:

#### 1. **Set up `App.jsx`**

- Import the `Joke` component (though not created yet):

    ```jsx
    import Joke from "./Joke";
    ```

- Wrap your jokes within a semantic `<main>` element:

    ```jsx
    export default function App() {
      return (
        <main>
          <Joke />
          <Joke />
          <Joke />
          <Joke />
          <Joke />
        </main>
      );
    }
    ```

#### 2. **Create the `Joke` component**

- In a new file (`Joke.jsx`):

```jsx
export default function Joke() {
  return <h1>Inside the Joke component</h1>;
}
```

- Verify it renders correctly.

#### 3. **Pass Joke Data via Props**

- Update each instance of the `Joke` component in `App.jsx` with real joke content:

```jsx
<Joke setup="Why did the..." punchline="Because..." />
```

- Accept these props in `Joke.jsx` and render them:

```jsx
export default function Joke(props) {
  return (
    <>
      <p>{props.setup}</p>
      <p>{props.punchline}</p>
      <hr />
    </>
  );
}
```

### Conditional Rendering

Not every joke has a setup. For instance, one-liner jokes only have punchlines:

> _"It’s hard to explain puns to kleptomaniacs because they take things literally."_

We should omit the `setup` prop in such cases.

Here's how to handle this gracefully with React’s conditional rendering:

```jsx
export default function Joke(props) {
  return (
    <>
      {props.setup && <p>{props.setup}</p>}
      <p>{props.punchline}</p>
      <hr />
    </>
  );
}
```

This ensures the setup paragraph **only renders if the `setup` prop exists**.

#### Alternative Method (Less Common)

You could also use the ternary operator to conditionally show or hide via CSS:

```jsx
<p style={{ display: props.setup ? "block" : "none" }}>{props.setup}</p>
```

But the double ampersand method (`&&`) is simpler, clearer, and widely preferred in React.

### Basic Styling

For improved readability, we introduced basic styling:

- Added some margin to the body element.
- Used `className="setup"` to bold the setup text.
- Assigned an unused `className="punchline"` to the punchline (for potential future styling).

### Summary

Through this practice, we've successfully:

- Passed props from the parent `App` component down to multiple child `Joke` components.
- Used conditional rendering (`&&`) to handle optional data gracefully.

## Non-String Props

We have one more important topic to cover regarding passing data through props before returning to our **Travel Journal** project.

Up to this point, we've only passed **strings** through props, similar to HTML attributes. In HTML, attributes typically must be strings—even if they represent numbers or other data types, they're still treated as strings.

However, React allows us to leverage JavaScript’s flexibility, meaning we can pass various data types beyond just strings.

### Challenge

Consider how you might pass non-string props. For example:

- Passing a **number** (`upvotes`, `downvotes`)
- Passing a **boolean** (`isPun`)
- Passing an **array** of comments or objects

You can experiment by pausing here to try passing different prop types in React.

### How to Pass Non-String Props

To pass JavaScript values as props, simply use curly braces `{}`:

**Numbers:**

```jsx
<Joke upvotes={10} />
```

You can now perform math operations:

```js
console.log(props.upvotes + 1); // Outputs 11
```

**Booleans:**

```jsx
<Joke isPun={true} />
```

You can directly use or invert the value:

```js
console.log(!props.isPun); // Flips the boolean
```

**Arrays and Objects:**

```jsx
<Joke comments={[
  { author: "user123", text: "Great joke!" },
  { author: "user456", text: "Haha!" }
]} />
```

Inside your component, access it normally:

```js
console.log(props.comments); // Outputs the array of objects
```

### Notes

- Wrapping strings in curly braces `{}` (e.g., `title={"My Joke"}`) is valid but unnecessary.
- For **non-string values**, using curly braces `{}` is **required**.
  - For example, `isPun=true` will produce a syntax error. Correct usage is `isPun={true}`.

### Props Summary

You can now confidently pass various types of data as props in React:

- Strings  
- Numbers  
- Booleans  
- Arrays  
- Objects  

This ability makes your components highly flexible and powerful.

## Importing Static Assets

Let's briefly discuss how to handle static assets, like images, when working outside of Scrimba, particularly in a local development environment.

### Why

While Scrimba handles static assets seamlessly, coding locally introduces potential issues:

- Relative paths to static assets (e.g., images) may not work as expected.
- Build tools like **Vite** restructure your project's files for optimization, affecting how assets are referenced.

### Problem with Relative Paths

Using a build tool such as **Vite** affects your project by:

- Relocating and optimizing static assets during the build.
- Potentially breaking hardcoded relative paths after deployment.

This means referencing an image with a relative path like `./images/photo.png` might work in development but fail after building and deploying.

### The Solution: Import Your Assets

To avoid broken paths, follow these two steps:

1. **Import the asset** at the top of your component file:

      ```js
      import mrWhiskerson from './images/mr-whiskerson.png';
      ```

2. **Use the imported variable** within your JSX:

      ```jsx
      <img src={mrWhiskerson} />
      ```

This approach allows JavaScript and your build tool (like Vite) to track and manage the asset correctly during bundling and deployment.

### Why Importing Works

When using a bundler like Vite, it automatically:

- Moves and optimizes assets to different folders during build.
- Rewrites asset paths appropriately in your final build output.

By importing your assets directly into JavaScript, you give Vite explicit instructions to handle and rewrite paths properly, ensuring your images load correctly in the production build.

### Important Note

- In a **local environment**, always import static assets explicitly.
- Replace hardcoded paths (e.g., `./images/image.png`) with imported asset variables.
- In **Scrimba**, this issue is typically handled automatically, allowing direct relative paths without problems.

### Recap

- Use explicit `import` statements for static assets in local projects.
- Replace relative paths in JSX with imported variables.
- Trust build tools like Vite to handle bundling and path adjustments.

By following this approach, you'll ensure your assets load reliably in both development and production environments.

## Pass Props to Entry Component

We're back at the Travel Journal project. Up until now, we've gained substantial knowledge about using props in React. Yet, if you look closely at our `Entry` component, you'll see everything is still hardcoded. It's time to fix this.

### A Tricky Detail: The Image Prop

The image prop isn't just a string—it's an object. Make sure you pass it correctly:

```jsx
img={{ src: "path/to/image.png", alt: "Mount Fuji" }}
```

Then, in your `Entry.jsx`, access it like this:

```jsx
<img src={props.img.src} alt={props.img.alt} />
```

---

### Refactoring Hardcoded Data

Replace all hardcoded data in your `Entry` component with dynamic props. To confirm your props are passing correctly, you can log them:

```jsx
console.log(props);
```

This change might seem subtle visually, but behind the scenes, your component is now dynamic.

### Implementing Props in JSX

For clarity, it's best to break the props onto separate lines:

```jsx
<Entry
  img={{ src: "...", alt: "..." }}
  title="Mount Fuji"
  country="Japan"
  googleMapsUrl="https://..."
  dates="12 Jan, 2021 - 24 Jan, 2021"
  text="Mount Fuji is the tallest mountain in Japan..."
/>
```

Then, in `Entry.jsx`, replace static content with props:

```jsx
<h1>{props.title}</h1>
<p>{props.dates}</p>
<a href={props.googleMapsUrl}>View on Google Maps</a>
```

### Test & Verify

- After making these changes, save your file.
- Visually, nothing changes—but under the hood, your `Entry` component is now reusable and dynamic.

### Why Pass Objects as Props?

Although it seems like a minor update, this marks an important milestone in your React journey:

You're no longer hardcoding data; instead, you're passing it dynamically, making components reusable. Now, creating multiple entries with different data is easy and efficient.

### Props Are Initially Challenging

It's common to find props challenging at first, especially when dealing with non-string values such as:

- Objects
- Arrays
- Booleans

## Review - array .map()

Before moving forward, let's review the `.map()` method, a powerful tool in JavaScript that you'll use frequently in React.

### `.map()` Challenge

```js
/* Challenge 1:
Given an array of numbers, return an array of each number, squared */
const nums = [1, 2, 3, 4, 5]
// -->       [1, 4, 9, 16, 25]
// Your code here
const squares = nums.map(function(num) {
    return num * num
})

console.log(squares)

/* Challenge 2:
Given an array of strings, return an array where 
the first letter of each string is capitalized */

const names = ["alice", "bob", "charlie", "danielle"]
// -->        ["Alice", "Bob", "Charlie", "Danielle"]
// Your code here
const capitalized = names.map(name => (name[0].toUpperCase() + name.slice(1)))

console.log(capitalized)

/* Challenge 3:
Given an array of strings, return an array of strings that wraps each
of the original strings in an HTML-like <p></p> tag.

E.g. given: ["Bulbasaur", "Charmander", "Squirtle"]
return: ["<p>Bulbasaur</p>", "<p>Charmander</p>", "<p>Squirtle</p>"] */

const pokemon = ["Bulbasaur", "Charmander", "Squirtle"]
// -->          ["<p>Bulbasaur</p>", "<p>Charmander</p>", "<p>Squirtle</p>"]
// Your code here

const paragraphs = pokemon.map(mon => `<p>${mon}</p>`)

console.log(paragraphs)
```

## React Can Render Arrays

Previously, we reviewed how to create arrays from existing arrays. Now, let's understand how React handles arrays when rendering.

### Rendering Arrays in React

React is capable of rendering arrays directly. For example, if you have an array of strings—such as the names of the Ninja Turtles—you can render it in JSX. If you simply reference the array in curly braces, React will concatenate and display each element as plain text:

```jsx
const turtles = ["Leonardo", "Raphael", "Donatello", "Michelangelo"];

function App() {
  return <div>{turtles}</div>; // Renders as LeonardoRaphaelDonatelloMichelangelo
}
```

This works whether your array is defined as a variable or written directly inline.

### Arrays of Objects and React

However, React cannot directly render arrays containing plain JavaScript objects. If you attempt to render an array of objects directly, React will throw an error:

> **Objects are not valid as a React child**

This is because React expects valid children, such as strings, numbers, or JSX elements—not plain JavaScript objects.

### Rendering Arrays of JSX Elements

To successfully render arrays in React, convert each item into a JSX element. For example, wrapping each Ninja Turtle's name in an `<h2>` tag:

```jsx
const turtles = ["Leonardo", "Raphael", "Donatello", "Michelangelo"];

function App() {
  const turtleElements = turtles.map(turtle => <h2>{turtle}</h2>);
  return <div>{turtleElements}</div>;
}
```

React renders this correctly as:

```html
<h2>Leonardo</h2>
<h2>Raphael</h2>
<h2>Donatello</h2>
<h2>Michelangelo</h2>
```

### Why Array Matters

This method allows you to dynamically generate UI components based on data. Rather than manually coding repetitive JSX, you can use `Array.map` to create multiple components, making your applications scalable and maintainable.

For example, when creating a list of joke components from a joke array:

```jsx
const jokes = [
  { setup: "Why did the...", punchline: "Because..." },
  { setup: "What do you call...", punchline: "A..." }
];

function App() {
  const jokeElements = jokes.map(joke => (
    <Joke setup={joke.setup} punchline={joke.punchline} />
  ));

  return <div>{jokeElements}</div>;
}
```

This is especially powerful when dealing with dynamic data, such as results fetched from an API.

### Note About Keys

When rendering arrays, you might see a React warning about missing `key` props. Don’t worry about this right now—we’ll address it in detail shortly.

### React Arrays: Recap

- React can render arrays directly, but arrays of plain objects will cause errors.
- Convert array items into JSX elements using `Array.map` for dynamic rendering.
- This approach is fundamental to building scalable React applications.

Let's practice this concept in the next lesson.

## Mapping Components

Before applying our new knowledge to React, let's briefly recap a few setup changes made to our project:

- All hardcoded instances of the `Joke` components have been removed and commented out.
- Instead of using a markdown (`.md`) file for jokes, we've introduced a new file, `jokesData.js`. This file mimics pulling data from an API and exports an array of joke objects.

### Using `.map()` to Render Components Dynamically

In the `App` component, we now import the `jokesData` array:

```js
import jokesData from "./jokesData.js";
```

By logging this data, we verify it's correctly imported:

```js
console.log(jokesData);
```

Next, we dynamically create an array of React components named `jokeElements` by mapping over the `jokesData` array. Each item from this array is converted into a `Joke` component, with data passed as props:

App.jsx:

```jsx
import Joke from "./Joke"
import jokesData from "./jokesData"

export default function App() {
    const jokeElements = jokesData.map((joke) => {
        return <Joke setup={joke.setup} punchline={joke.punchline} />
    })
    return (
        <main>
            {jokeElements}
        </main>
    )
}
```

### Cleaning Up the Codebase

Once verified, you can safely remove any old challenge text and commented-out components. Notice how much simpler and scalable your code becomes when using `.map()` instead of manually adding components.

### Benefits of Using `.map()` for Dynamic Rendering

- **Flexibility**: Even if your dataset includes thousands of jokes, your rendering logic won't change.
- **Maintainability**: Changes to your data automatically reflect in your UI without extra effort.
- **Scalability**: Easily supports future enhancements like pagination or filtering.

### What's Next?

Having practiced dynamic rendering with jokes, you're now prepared to apply this approach to the Travel Journal project. Instead of hardcoding a single trip, we'll store our trips externally (e.g., in a JavaScript file), iterate over them using `.map()`, and render each entry dynamically.

Before returning to the Travel Journal, there's a quick quiz to reinforce your understanding of using `.map()` in React.

## Map Quiz

1. What does the `.map()` array method do?
Returns a new array. Whatever gets returned from the callback
function provided is placed at the same index in the new array.
Usually we take the items from the original array and modify them
in some way.

2. What do we usually use `.map()` for in React?
Convert an array of raw data into an array of JSX elements
that can be displayed on the page.

3. Critical thinking: why is using `.map()` better than just
   creating the components manually by typing them out?
    1. We often don't have the data ahead of time when we're building
       the app, so we simply can't manually type them out.
    2. It makes our code more "self-sustaining" - not requiring additional
       changes to the code whenever the data changes.

## Travel Journal

### Map Entry Components

Everything we've learned so far comes together in this exercise. Let's quickly overview the setup:

Instead of using a markdown file for our Travel Journal data, we now have a JavaScript file (`data.js`) exporting an array of journal entry objects. Each object contains details for one entry, including an `id`. Don't worry about the `id` property yet—we'll address it soon.

#### Step-by-Step Implementation

First, **import** the `data` array:

```jsx
import data from './data.js';
```

Next, create an array of JSX elements (`entryElements`) by mapping over the imported data:

```jsx
const entryElements = data.map(entry => (
  <Entry
    img={entry.image}
    title={entry.title}
    country={entry.country}
    googleMapsLink={entry.googleMapsLink}
    dates={entry.dates}
    text={entry.text}
  />
));
```

Finally, replace the single hardcoded `<Entry />` in your JSX with the dynamically generated `entryElements`:

```jsx
export default function App() {
  return (
    <div>
      {entryElements}
    </div>
  );
}
```

When you save, all journal entries should appear correctly on the page with their respective images and details.

#### Why This Matters to our Project

This challenge demonstrates a fundamental pattern in React development:

- Dynamically rendering multiple components from imported data.
- Leveraging JavaScript's `.map()` method to build scalable UIs.

If this exercise feels challenging, that's completely normal. Consider revisiting earlier sections for additional practice or reach out to the community for support.

Completing this milestone means you've successfully built a functional MVP (Minimum Viable Product) of your Travel Journal app.

### Key Prop

One of the powerful aspects of React is that the UI directly reflects the underlying data. For example, if we duplicate some entries in our `data.js` file and save, those new entries instantly appear on the screen. While typically we'd fetch data from an API, this demonstrates React's strength in dynamically rendering data from arrays.

However, you might notice a common warning in the console when mapping arrays to components:

> "Warning: Each child in a list should have a unique `key` prop."

This warning arises because React internally tracks elements using a special prop called `key`. The `key` helps React efficiently determine which elements have changed, been added, or removed.

#### Solving the Key Prop Warning

To resolve this warning, provide a unique `key` prop whenever you map over an array. Important points about keys:

- The prop name **must be** `key`.
- The key's value must be unique across the array.

An incorrect example (all keys identical):

```jsx
data.map(item => <Entry key={1} />);
```

A correct and recommended way, using a unique ID from your data:

```jsx
data.map(entry => (
  <Entry
    key={entry.id}
    img={entry.image}
    title={entry.title}
    country={entry.country}
    googleMapsLink={entry.googleMapsLink}
    dates={entry.dates}
    text={entry.text}
  />
));
```

Most real-world data (especially from databases or APIs) include a unique ID, making it an ideal key.

---

#### Choosing Good Keys

Technically, for smaller datasets, you might consider using other unique fields like:

- `title`
- `dates`
- `text`

However, these can potentially repeat (e.g., visiting the same location multiple times), leading to key duplication. Therefore, using unique IDs remains best practice.

#### Avoid Using Array Index as Key

Although tempting, using the array index provided by `.map()` as the key is generally discouraged:

```jsx
data.map((entry, index) => <Entry key={index} />);
```

While this eliminates the warning temporarily, it can lead to rendering issues if the list dynamically changes—such as adding, removing, or sorting items. React's documentation explains this further if you're curious.

**Rule of thumb:** Avoid using the array index as a key unless you have no better option.

#### Key Prop: Recap

- The `key` prop helps React track elements efficiently.
- Keys must be unique and are typically taken from data IDs.
- Avoid using the array index as a key.

With this resolved, our app is looking clean and ready to move forward. We'll wrap up a few more details about props in the next sections.

### Pass Object as Props

As our `Entry` component grows, you might notice that explicitly passing individual props (like `image={entry.image}`, `title={entry.title}`, etc.) becomes cumbersome, especially if the data objects contain many properties.

Instead of manually passing each property, a more concise approach is to pass the entire data object as a single prop. For example:

```jsx
<Entry key={entry.id} entry={entry} />
```

This approach allows the `Entry` component to access all the properties it needs directly from the passed object.

#### Important Considerations

- You **must still include the `key` prop** separately when mapping components from an array. React uses the `key` prop to uniquely identify components and manage their lifecycle efficiently.

- The name of the prop (`entry` in this case) is arbitrary but choosing clear, descriptive names helps readability.

#### Updating the `Entry` Component

Since we're now passing the entire object as a prop, you'll need to update the `Entry` component accordingly.

Previously, your component might have directly accessed props like:

```jsx
<img src={props.img.src} alt={props.img.alt} />
<h1>{props.title}</h1>
```

Now, you must update it to reflect the new prop structure:

```jsx
<img src={props.entry.image.src} alt={props.entry.image.alt} />
<h1>{props.entry.title}</h1>
```

If your component breaks after making this change, it’s likely due to trying to access props using the old structure (`props.title`, `props.img.src`). A good debugging step is to log props and verify the new structure:

```jsx
console.log(props);
```

#### Debugging Common Errors

A common error you might encounter is something like:

```txt
Cannot read property 'src' of undefined
```

This occurs because the component still expects individual props instead of the nested object (`entry`). Temporarily using optional chaining (`img?.src`) can avoid the error momentarily but isn't a permanent fix.

Properly adjust your code by updating references to the nested structure:

```jsx
props.entry.image.src
props.entry.title
props.entry.country
// and so forth...
```

#### Pros and Cons

**Advantages**:

- Significantly reduces boilerplate and repetition in your JSX.
- Cleaner and more concise component rendering logic.

**Disadvantages**:

- Your component becomes tightly coupled to the exact structure of the data object. Any mismatch or change in naming conventions (like using snake_case instead of camelCase) can break your component.
- It requires consistent property names throughout your data source.

#### Best Practices

- Ensure your data consistently matches your component's expected property names.
- If using external APIs or databases, be mindful of naming conventions and adjust your data or components accordingly.

#### Next Steps

There's one final concise method to pass all properties from an object directly into a component without explicitly stating `entry={entry}`. We'll explore this helpful technique in the next section.

### Spread Object as Props

There's one more concise JavaScript trick for passing an object's properties directly into a React component—known as **object spread syntax**. You might encounter this syntax in real-world React projects, so it's good to understand how it works.

Instead of explicitly writing:

```jsx
<Entry entry={entry} />
```

You can use the spread syntax:

```jsx
<Entry {...entry} />
```

This tells React to spread each individual property from the `entry` object as separate props. For instance, if `entry` looks like this:

```js
const entry = {
  id: 1,
  image: { src: "mount-fuji.jpg", alt: "Mount Fuji" },
  title: "Mount Fuji",
};
```

Using `{...entry}` is equivalent to writing:

```jsx
<Entry
  id={entry.id}
  image={entry.image}
  title={entry.title}
/>
```

React handles nested objects gracefully with this approach.

#### Refactoring the Component

When you switch to this spread syntax, you'll likely encounter a breaking change. If your component was previously structured to accept an `entry` object directly (`props.entry.title`), it will now break, because the props are no longer nested under `entry`.

The solution is straightforward:

- Remove the nested object reference from your component.
- For example, change from:

```jsx
<img src={props.entry.image.src} alt={props.entry.image.alt} />
<h1>{props.entry.title}</h1>
```

- To simply:

```jsx
<img src={props.image.src} alt={props.image.alt} />
<h1>{props.title}</h1>
```

#### Advantages of Using Spread Syntax

- **Conciseness**: Your parent component becomes cleaner, avoiding repetitive prop declarations.
- **Simplified Child Components**: Eliminates deeply nested property references.

#### Considerations and Trade-offs

While concise, the spread syntax has a trade-off:

- **Clarity**: It can be less obvious what props are being passed at a glance.
- **Debugging and maintenance**: You may need additional logging or referencing back to your data structure to remember what props are available.

In some cases, explicitly naming props or passing the entire object as a single prop (like `entry={entry}`) can make your code easier to read and maintain long-term.

#### Completion of the Travel Journal Project

This marks the end of the Travel Journal project! Consider improving the UI or adding your own personal entries by updating the `data.js` file. Share your creations within the Scrimba Discord community to receive feedback and support.

Finally, we'll briefly recap what we've learned before moving forward. If you're a Scrimba Pro member, expect a solo project soon that lets you apply these concepts independently—a great opportunity to solidify your understanding.

Access the project here: [03-TravelJournal](../src/projects/03-TravelJournal/README.md)

## Section 2 Recap

You've completed the Travel Journal project—a major milestone in your React learning journey.

In this section, we've explored key React concepts and used them to build a dynamic, reusable web app.

### What We Learned

We began by discussing why **reusability** is crucial:

- Modern web applications rely heavily on reusable components.
- Instead of manually hardcoding HTML, dynamic data is used to render the UI.

While static HTML still has its place, increasingly you'll use **dynamic data to drive interfaces**, whether it's personal projects, dashboards, or more complex apps like our travel journal.

### Understanding Props

In React, **props** are essential for creating reusable components. They're similar to function parameters, enabling components to render different content based on the data passed in.

We also learned how React can render **arrays of components**:

- Taking raw data (e.g., travel destinations)
- Mapping over that data
- Dynamically rendering each piece of data as a separate component instance

In this project, our data was static and stored locally, but typically you'd fetch it from an external **API** in real-world apps.

### Key Takeaways

This section marks significant progress in your React skills:

- You've learned to build dynamic, data-driven apps.
- You've grasped essential concepts like props and mapping over arrays.
- You're now equipped to create scalable and maintainable React applications.

Take some time to share your achievements on the **Scrimba Discord**, particularly in the `#today-i-did` channel, and celebrate your progress alongside your peers.

### Section 2: What's Next?

After you've taken a well-deserved break, get ready for the next section. It will significantly deepen your React knowledge and empower you to build:

- More interactive applications
- Advanced features
- Dynamic user experiences

Rest up, celebrate your successes, and then dive into the next exciting chapter of your React journey.
