# Section 1: Getting Started

## 1. Welcome to the Course

- **Instructor:** Maximilian Schwarzmüller
- **Course Goal:** Teach you React from the ground up—step by step—by building multiple realistic demo projects.
- **Approach:**
  - Hands‑on practice over theory
  - Fun, project‑driven learning
  - Gradually dive deeper into fundamentals and advanced concepts
- **Outcome:**
  - By course end you can call yourself a React developer
  - You’ll master crucial fundamentals and advanced React features
- **Next Up:** What exactly is React, and why use it?

## 2. What is React.js? And Why Would You Use It?

- **Definition (react.dev):**
  - A JavaScript library for building web and native user interfaces
- **Key Idea:**
  - React runs in the browser to update the UI without full page reloads
- **User Experience Example:**
  - Netflix‑style smooth, near‑instant transitions
  - Feels like a mobile app: instant feedback and seamless navigation
- **How It Works:**
  - JavaScript fetches data behind the scenes (e.g., clicking “Movies” tab)
  - Dynamically updates DOM instead of reloading the page
- **Why Not Plain JavaScript?**
  - Vanilla JS for complex UIs is:
    - Cumbersome to write and maintain
    - More error‑prone
    - A poor fit for large, dynamic applications

## 3. ReactJS vs “Vanilla JavaScript”: Why Use React?

- **Demonstration Setup:**
  - Two nearly identical demo apps (tabs + content)
    - One built with plain JS
    - One built with React (both hosted on CodeSandbox)
- **Vanilla JS Version:**
  - `index.html`: Static buttons & container
  - `index.js`:
    - Queries buttons, adds click listeners
    - Clears/sets active CSS class
    - Builds `<ul>` via string concatenation and `innerHTML`
  - **Drawbacks:**
    - Lots of imperative DOM‑manipulation code
    - Manual state management (which button is active)
    - Verbose, easy to introduce bugs
- **React Version:**
  - **Structure:**
    - `public/index.html` contains only `<div id="root">`
    - `src/index.js` mounts the React app to that root div
    - `src/App.js` contains all UI markup + logic
  - **JSX:**
    - Blend of HTML and JS in one file
    - Dynamic expressions (e.g., conditional `className`)
    - Array mapping to `<li>` elements
  - **State Management:**
    - `useState` hook holds `activeContentIndex`
    - Clicking a button calls the state setter (`setActiveContentIndex`)
    - React “re‑renders” UI declaratively based on state
  - **Benefits:**
    - Declarative code: describe *what* the UI should look like, not *how* to update it
    - Less boilerplate, fewer manual DOM steps
    - Easier to extend (e.g., add a fourth button)

## 4. Editing Our First React App

- **Exercise Setup:**
  - Updated demo on CodeSandbox with four nested arrays in `content`
  - Goal: Add a **fourth button** that displays new content
- **Steps Taken:**
  1. **Add Button Markup**
     - Copy/paste an existing `<button>` in `App.js`
     - Rename text (e.g., “React vs JS”)
  2. **Adjust Logic**
     - In the button’s `onClick`, call `setActiveContentIndex(3)`
     - In `className` condition, check `activeContentIndex === 3`
  3. **Verify**
     - Save and (if needed) refresh preview
     - Click new button → only that button is active & its list displays
- **Key Takeaway:**
  - Even without deep React knowledge, you can manipulate state and markup
  - React’s declarative model makes adding features straightforward

## 5. About This Course & Course Outline

- **Modular Structure:**
  1. **Getting Started** (current section)
  2. **Optional JavaScript Refresher** (skip if confident in JS)
  3. **React Essentials**
     - Base Essentials
     - Deep Dive
     - Practice Projects
  4. **Advanced Topics** (each in its own section)
- **Flexibility:**
  - **Sequential Path:** Complete lecture‑by‑lecture for full depth
  - **Pick‑and‑Choose:** Jump to sections of interest if you have prior React experience
- **Outcome:**
  - Whether beginner or experienced, you’ll end up a confident React developer

## 6. The Two Ways (Paths) Of Taking This Course

1. **Standard Path (Recommended):**
   - Follow curriculum in order, lecture by lecture
   - Ensures a thorough, ground‑up understanding
2. **Summary Path (Quick Overview):**
   - Jump to dedicated summary section (few hours)
   - Covers key basic & advanced concepts without deep dives
   - Great for a quick refresher or initial survey

- **Best Practice:**
  - Beginners: Standard Path
  - Fast learners or refreshers: Summary Path, then revisit full sections

## 7. Getting The Most Out Of This Course

- **Prerequisites:**
  - Basic web development & JavaScript knowledge required
  - Optional JS refresher available—but not a full JS course
- **Video Learning Tips:**
  - Adjust playback speed as needed
  - Pause or rewatch unclear explanations
  - Repeat entire sections if helpful
- **Practice & Application:**
  - Complete built‑in coding exercises & demo projects
  - Pause videos to try next steps on your own
  - Build your own mini‑projects inspired by course examples
- **Community & Support:**
  - Use provided GitHub code snapshots to compare solutions
  - Ask and answer questions in the Q&A section
  - Join Discord (next lecture) to collaborate and get help

## 8. Join Our Online Learning Community

- **Academind Community on Discord:**
  - Free, optional access: <https://academind.com/community/>
  - Connect with fellow learners, share progress, ask questions
  - Collaborate, troubleshoot, and celebrate wins together
- **Why Join:**
  - Learning is more effective with peers
  - Code snapshots + community = best complementary resources

## 9. Creating React Projects

- **Quick Start with CodeSandbox:**
  - Go to `react.new` in browser → instant React workspace
  - No local setup required; in‑browser editor + live preview
- **Local Setup (Optional):**
  - **Editor:** Visual Studio Code (free, cross‑platform)
  - **Node.js:** Install from nodejs.org (latest or LTS)
  - **Scaffolding Tools:**
    - **Vite:** `npm create vite@latest` → select React template
    - **Create React App:** alternative CLI tool
  - **Commands:**
    1. `npm install` (once, to fetch dependencies)
    2. `npm run dev` (in Vite; starts development server with live reload)
- **Project Options:**
  - **CodeSandbox:** No installs, instant previews
  - **Local:** Full control, favorite editor, custom extensions
  - **Course Resources:** Both CodeSandbox links and local zip snapshots provided

## 10. Why Do You Need A Special Project Setup?

- **JSX Syntax:**
  - React uses JSX (HTML‑in‑JS) which browsers don’t understand natively
- **Build & Transform:**
  - Tools like Vite or Create React App compile JSX → valid JavaScript
  - Minify, tree‑shake, and optimize code for production
- **Developer Experience:**
  - Live‑reload, error overlays, source maps, and fast refresh
- **Conclusion:**
  - Without these tools, you cannot write modern React code in the browser
  - Course provides preconfigured setups so you can focus on React

## 11. Course Setup

- **IDE Recommendations:**
  - **VS Code:** Free, extensible, cross‑platform (recommended)
  - **JetBrains WebStorm:** 6‑month free license with coupon `ACAD_JETBRAINS`
- **JetBrains Offer:**
  - Select your IDE, enter code `ACAD_JETBRAINS` at checkout
  - Follow instructions on the JetBrains site
  - **Note:** IDE choice is optional; VS Code works perfectly well
