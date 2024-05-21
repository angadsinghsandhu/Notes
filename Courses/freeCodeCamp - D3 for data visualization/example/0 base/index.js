// D3 selectors (accept css selector or name of DOM element as parameter) 
// that return selection of element
d3.select();        // returns first selection matching criteria
d3.selectAll();     // returns all selections matching criteria

// example: chaining H1 tag seletion
d3.select('h1').style('color', 'red')       // changing styling of H1 tag
.attr('class', 'heading')                   // adding sttributes
.text("Second Header (updated)")            // editing text

// example: adding text
d3.select('body').append('p').text("First Para")    // adding <p> tag
d3.select('body').append('p').text("Second Para")    // adding <p> tag
d3.select('body').append('p').text("Third Para")    // adding <p> tag
