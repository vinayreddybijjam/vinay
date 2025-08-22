# Comprehensive API Documentation

This document provides comprehensive documentation for all public APIs, functions, and components in the codebase.

## Table of Contents

1. [JavaScript Functions](#javascript-functions)
2. [JavaScript Data Structures](#javascript-data-structures)
3. [Java Classes](#java-classes)
4. [HTML Components](#html-components)
5. [CSS Classes and Styles](#css-classes-and-styles)
6. [Usage Examples](#usage-examples)

---

## JavaScript Functions

### Event Handler Functions (`function.js`)

#### `button1()`
**Purpose**: Changes the background color of an element to yellow on mouse over event.

**Parameters**: None

**Returns**: None

**Usage**:
```html
<button id="mouseover1" onmouseover="button1()">Mouse over</button>
```

**Example**:
```javascript
// Function implementation
function button1(){
    var a = document.getElementById("mouseover1");
    a.style = "background-color: Yellow"
}
```

---

#### `button2()`
**Purpose**: Changes the background color of an element to red on mouse out event.

**Parameters**: None

**Returns**: None

**Usage**:
```html
<button id="mouseout1" onmouseout="button2()">Mouse out</button>
```

**Example**:
```javascript
function button2(){
    var b = document.getElementById("mouseout1");
    b.style = "background-color: Red"
}
```

---

#### `button3()`
**Purpose**: Changes the background color of an element to black on click event.

**Parameters**: None

**Returns**: None

**Usage**:
```html
<button id="click1" onclick="button3()">Onclick</button>
```

**Example**:
```javascript
function button3(){
    var c = document.getElementById("click1");
    c.style = "background-color: Black"
}
```

---

#### `button4()`
**Purpose**: Changes the background color of an element to orange on double click event.

**Parameters**: None

**Returns**: None

**Usage**:
```html
<button id="dblclick1" ondblclick="button4()">ondblclick</button>
```

**Example**:
```javascript
function button4(){
    var d = document.getElementById("dblclick1");
    d.style = "background-color: Orange"
}
```

---

#### `button5()`
**Purpose**: Changes the background color of an input element to pink on focus event.

**Parameters**: None

**Returns**: None

**Usage**:
```html
<input id="onfocus1" onfocus="button5()" />
```

**Example**:
```javascript
function button5(){
    var e = document.getElementById("onfocus1");
    e.style = "background-color: Pink"
}
```

---

#### `button6()`
**Purpose**: Converts the input text to uppercase on blur event.

**Parameters**: None

**Returns**: None

**Usage**:
```html
<input type="text" id="onblur1" onblur="button6()" />
```

**Example**:
```javascript
function button6(){
    var f = document.getElementById("onblur1");
    f.value = f.value.toUpperCase();
}
```

---

### Utility Functions (`ass.js`, `ass2.js`, `ass3.js`)

#### Divisibility Check (`ass.js`)
**Purpose**: Checks if a number is divisible by 7.

**Parameters**: None (uses hardcoded variable `a`)

**Returns**: Console output indicating divisibility

**Example**:
```javascript
var a = 36;
if(a % 7 == 0){
    console.log("yes divisible by 7")
} else {
    console.log("no not divisible by 7")
}
```

---

#### Multiple Check (`ass2.js`)
**Purpose**: Checks if a number is a multiple of 3.

**Parameters**: None (uses hardcoded variable `a`)

**Returns**: Console output indicating if it's a multiple

**Example**:
```javascript
var a = 9;
if(a % 3 == 0){
    console.log("yes multiple by 3")
} else {
    console.log("no not multiple by 3")
}
```

---

#### Number Sign Check (`ass3.js`)
**Purpose**: Determines if a number is positive, negative, or neutral (zero).

**Parameters**: None (uses hardcoded variable `a`)

**Returns**: Console output indicating the number's sign

**Example**:
```javascript
var a = 0;
if(a == 0){
    console.log(`Please enter a valid number 0 is neutral`)
} else if(a > 0){
    console.log(`${a} is positive number`)
} else {
    console.log(`${a} is negative number`)
}
```

---

## JavaScript Data Structures

### Employee Array (`j.js`)
**Purpose**: Stores employee information in an array of objects.

**Structure**:
```javascript
let employee = [
    {
        i: "1",
        first_name: "Bernardine",
        last_name: "Banbrook",
        email: "bbanbrook0@shareasale.com",
        gender: "Male",
    },
    // ... more employees
];
```

**Properties**:
- `i`: Employee ID (string)
- `first_name`: Employee's first name (string)
- `last_name`: Employee's last name (string)
- `email`: Employee's email address (string)
- `gender`: Employee's gender (string)

**Usage**:
```javascript
// Access first employee
console.log(employee[0].first_name); // "Bernardine"

// Loop through all employees
employee.forEach(emp => {
    console.log(`${emp.first_name} ${emp.last_name}`);
});
```

---

### Contacts Data (`data.js`)
**Purpose**: Comprehensive contact information storage with detailed user profiles.

**Structure**: Array of contact objects with nested properties for name, location, login credentials, and personal information.

**Key Properties**:
- `gender`: Contact's gender
- `name`: Object containing title, first, and last name
- `location`: Object with street, city, state, country, coordinates, and timezone
- `email`: Contact's email address
- `login`: Object with UUID, username, and password hashes
- `dob`: Date of birth and age
- `phone`: Contact and cell phone numbers
- `picture`: URLs for profile images (large, medium, thumbnail)
- `nat`: Nationality code

**Usage**:
```javascript
// Access contact information
const firstContact = contacts[0];
console.log(firstContact.name.first); // "Kaspian"
console.log(firstContact.location.city); // "Leirvik"

// Filter contacts by gender
const maleContacts = contacts.filter(contact => contact.gender === "male");

// Find contacts by city
const cityContacts = contacts.filter(contact => 
    contact.location.city === "Leirvik"
);
```

---

## Java Classes

### Fibonacci Class (`fabonacci.java`)
**Purpose**: Generates and prints the first 10 numbers in the Fibonacci sequence.

**Public Methods**:
- `main(String args[])`: Entry point that generates Fibonacci sequence

**Algorithm**: Uses iterative approach with three variables to generate sequence

**Usage**:
```bash
javac fabonacci.java
java fabonacci
```

**Output**: `0 1 1 2 3 5 8 13 21 34`

**Code Structure**:
```java
class fabonacci {
    public static void main(String args[]) {
        int n1 = 0, n2 = 1, n3, i, count = 10;
        System.out.print(n1 + " " + n2);
        
        for(i = 2; i < count; i++) {
            n3 = n1 + n2;
            System.out.print(" " + n3);
            n1 = n2;
            n2 = n3;
        }
    }
}
```

---

### FibonacciExample1 Class (`ex.java`)
**Purpose**: Alternative implementation of Fibonacci sequence generation.

**Public Methods**:
- `main(String args[])`: Entry point for Fibonacci sequence generation

**Usage**:
```bash
javac ex.java
java FibonacciExample1
```

**Output**: `0 1 1 2 3 5 8 13 21 34`

**Code Structure**:
```java
class FibonacciExample1 {
    public static void main(String args[]) {
        int n1 = 0, n2 = 1, n3, i, count = 10;
        System.out.print(n1 + " " + n2);
        
        for(i = 2; i < count; ++i) {
            n3 = n1 + n2;
            System.out.print(" " + n3);
            n1 = n2;
            n2 = n3;
        }
    }
}
```

---

## HTML Components

### Event Demonstration Interface (`index.html`)
**Purpose**: Interactive demonstration of various JavaScript events.

**Components**:
- **Mouse Events**: Mouse over, mouse out, click, double click
- **Focus Events**: Focus and blur event handlers
- **Responsive Layout**: Flexbox-based responsive design

**Structure**:
```html
<div class="container">
    <h1>Javascript Events</h1>
    <div class="main">
        <!-- Event demonstration sections -->
    </div>
</div>
```

**Event Bindings**:
- `onmouseover="button1()"`: Triggers on mouse over
- `onmouseout="button2()"`: Triggers on mouse out
- `onclick="button3()"`: Triggers on single click
- `ondblclick="button4()"`: Triggers on double click
- `onfocus="button5()"`: Triggers on input focus
- `onblur="button6()"`: Triggers on input blur

---

### Dropdown Navigation (`h1.html`)
**Purpose**: Collapsible dropdown navigation menu with icons.

**Features**:
- Checkbox-based toggle mechanism
- Font Awesome icon integration
- Smooth CSS transitions

**Structure**:
```html
<div class="container">
    <input type="checkbox" class="btn">
    <div class="list">
        <a href="#"><i class="fas fa-user-alt"></i>&nbspProfile</a>
        <a href="#"><i class="fas fa-envelope"></i>&nbspMessages</a>
        <a href="#"><i class="fas fa-cog"></i>&nbspSettings</a>
        <a href="#"><i class="fas fa-sign-out-alt"></i>&nbspLog Out</a>
    </div>
</div>
```

---

### Basic HTML Templates (`basics/` directory)
**Purpose**: Collection of basic HTML structure examples.

**Files**:
- `employee.html`: Employee information display template
- `form.html`: Basic form structure
- `image.html`: Image display template
- `list.html`: List structure examples
- `table.html`, `table1.html`, `table2.html`: Table structure variations

---

## CSS Classes and Styles

### Main Layout Classes (`style.css`)

#### `.container`
**Purpose**: Main wrapper for the entire application.

**Properties**:
```css
.container {
    /* Grid layout commented out */
    /* display: grid; */
    /* border: 2px solid black; */
}
```

---

#### `.main`
**Purpose**: Flexbox container for organizing content sections.

**Properties**:
```css
.main {
    display: flex;
    overflow: hidden;
    padding: 51px;
    margin: 56px;
}
```

---

#### `.one-class`
**Purpose**: Individual content section styling.

**Properties**:
```css
.one-class {
    display: inline-flex;
    justify-content: center;
    flex-direction: column;
    margin: 0 15px;
}
```

---

### Button Styling

#### `#mouseover1`
**Purpose**: Mouse over button styling.

**Properties**:
```css
#mouseover1 {
    background-color: blue;
    color: white;
    width: 213px;
    height: 36px;
}
```

#### `#mouseout1`
**Purpose**: Mouse out button styling.

**Properties**:
```css
#mouseout1 {
    background-color: green;
    color: white;
    width: 213px;
    height: 36px;
}
```

#### `#click1`
**Purpose**: Click button styling.

**Properties**:
```css
#click1 {
    background-color: red;
    color: white;
    width: 213px;
    height: 36px;
}
```

#### `#dblclick1`
**Purpose**: Double click button styling.

**Properties**:
```css
#dblclick1 {
    background-color: rgb(247, 0, 255);
    color: white;
    width: 213px;
    height: 36px;
}
```

---

### Input Styling

#### `#onfocus1`, `#onblur1`
**Purpose**: Input field styling for focus and blur events.

**Properties**:
```css
#onfocus1, #onblur1 {
    color: black;
    width: 213px;
    height: 26px;
}
```

---

### Typography

#### `h1`
**Purpose**: Main heading styling.

**Properties**:
```css
h1 {
    justify-content: center;
    text-align: center;
    font-family: 'Qahiri', sans-serif;
    font-family: 'Rampart One', cursive;
}
```

---

## Usage Examples

### Complete Event Handler Setup

1. **Include the JavaScript file**:
```html
<script src="./function.js"></script>
```

2. **Create HTML elements with event bindings**:
```html
<button id="mouseover1" onmouseover="button1()">Mouse over</button>
<button id="click1" onclick="button3()">Click me</button>
<input id="onfocus1" onfocus="button5()" placeholder="Focus me" />
```

3. **Add corresponding CSS styling**:
```css
#mouseover1 {
    background-color: blue;
    color: white;
    width: 213px;
    height: 36px;
}
```

### Working with Data Structures

1. **Accessing Employee Data**:
```javascript
// Get first employee
const firstEmployee = employee[0];
console.log(firstEmployee.first_name); // "Bernardine"

// Filter by gender
const maleEmployees = employee.filter(emp => emp.gender === "Male");
```

2. **Working with Contact Data**:
```javascript
// Find contacts by country
const norwegianContacts = contacts.filter(contact => 
    contact.location.country === "Norway"
);

// Get contact's full name
const fullName = `${contact.name.title} ${contact.name.first} ${contact.name.last}`;
```

### Running Java Programs

1. **Compile the Java file**:
```bash
javac fabonacci.java
```

2. **Run the compiled class**:
```bash
java fabonacci
```

### Responsive Layout Implementation

1. **HTML Structure**:
```html
<div class="container">
    <h1>Your Title</h1>
    <div class="main">
        <div class="one-class">
            <!-- Content here -->
        </div>
    </div>
</div>
```

2. **CSS Flexbox Layout**:
```css
.main {
    display: flex;
    overflow: hidden;
    padding: 51px;
    margin: 56px;
}

.one-class {
    display: inline-flex;
    justify-content: center;
    flex-direction: column;
    margin: 0 15px;
}
```

---

## Best Practices

### JavaScript
- Use meaningful function names that describe the action
- Implement proper error handling for DOM element selection
- Consider using event listeners instead of inline event handlers for better separation of concerns
- Use const/let instead of var for better scoping

### Java
- Follow Java naming conventions (class names should start with capital letters)
- Consider making methods more modular and reusable
- Add input validation for user-provided data
- Use meaningful variable names

### HTML
- Use semantic HTML elements where appropriate
- Ensure proper accessibility with ARIA labels
- Validate HTML structure
- Use consistent indentation and formatting

### CSS
- Use CSS custom properties for consistent theming
- Implement responsive design principles
- Follow BEM methodology for class naming
- Minimize CSS specificity conflicts

---

## Dependencies

### External Libraries
- **Font Awesome 5.15.4**: For icon support in dropdown navigation
- **Google Fonts**: 'Qahiri' and 'Rampart One' for typography

### Browser Compatibility
- Modern browsers supporting ES6+ JavaScript features
- CSS Flexbox support
- HTML5 semantic elements support

---

## Troubleshooting

### Common Issues

1. **Event handlers not working**:
   - Ensure JavaScript file is properly loaded
   - Check that element IDs match between HTML and JavaScript
   - Verify event binding syntax

2. **Styling not applied**:
   - Confirm CSS file path is correct
   - Check for CSS syntax errors
   - Verify element selectors match HTML structure

3. **Java compilation errors**:
   - Ensure Java Development Kit (JDK) is installed
   - Check Java version compatibility
   - Verify file naming matches class names

---

This documentation provides a comprehensive overview of all public APIs, functions, and components in your codebase. For specific implementation details or additional questions, refer to the individual source files or contact the development team.