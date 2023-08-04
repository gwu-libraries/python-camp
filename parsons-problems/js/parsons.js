function createIndents() {
    // Create left margin for indented blocks
    document.querySelectorAll(".parsons-row-ss").forEach((row) => {
        row.querySelectorAll(".parsons-ss").forEach((cell, i) => {
            cell.style.left = 50*i;
        });
    });
}

function dragstart_handler(ev) {
    // We don't want to drag anything but the actual DIV block

    ev.stopPropagation();
    if ((ev.target.nodeType == Node.TEXT_NODE) || !ev.target.classList.contains("parsons-block")) {
        ev.preventDefault();
        return
    }
    // Add the hidden class to the element; this corrects for the conflict between the browser-native drag-and-drop and the drag-and-drop HTML API
    // Thanks to Max Turer for this!
    ev.target.classList.add("hidden");
    
    // Add the block's id to the data transfer object
    ev.dataTransfer.setData("text/plain", ev.target.id);    

    let dragStartParent = ev.target.parentElement;

    if (dragStartParent.className == "parsons-ss") {

        let previousSibs = getPreviousSiblings(dragStartParent);
        previousSibs.forEach(node => {
            let indentNode = node.querySelector(".indent-char");
            if (indentNode) indentNode.remove();
        });
     }
}

function dragover_handler(ev) {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "move";
}

function dragenter_handler(ev) {
    ev.preventDefault();
    ev.target.classList.add("dragover");
}

function dragleave_handler(ev) {
    ev.preventDefault();
    ev.target.classList.remove("dragover");
}

function drop_handler(ev) {
    // Get the id of the block to move to the current element
    const data = ev.dataTransfer.getData("text/plain");
    let block = document.getElementById(data);
    // If there is already a block in this row (other than the currently selected block), no drop is allowed
    let otherBlock = ev.target.parentElement.querySelector(".parsons-block");
    if ((otherBlock) && (block != otherBlock) && (ev.target.parentElement.className == "parsons-row-ss")) {
        ev.preventDefault();
        ev.target.classList.remove("dragover");
        return;
    }
    // remove the error class in case this is a move from a solution slot with an error applied
    block.classList.remove("parsons-error");

    ev.target.appendChild(block);
    ev.target.classList.remove("dragover");

    // Add indentation symbol as UX cue to previous divs in the current row
    if (ev.target.className == 'parsons-ss') {
        let previousSibs = getPreviousSiblings(ev.target);
        previousSibs.forEach(node => {
            let newIndentChar = document.createElement("span");
            newIndentChar.textContent = "\u21e5";
            newIndentChar.className = "indent-char";
            node.appendChild(newIndentChar);
         });
    }
}

function swapDrop(ev) {
    // Allows swapping one draggable element for another
    const data = ev.dataTransfer.getData("text/plain"); // element to swap
    let block = document.getElementById(data);
    let blockToSwap = ev.target;
    swapElements(block, blockToSwap);
    ev.stopPropagation();
}

function parseParsonsCode() {
    // Extract innerText from all blocks in the solution space and parse 
    const blocks = document.querySelectorAll(".parsons-ss .parsons-block");
    let codeLines = [];
    blocks.forEach(block => {
        // The element ID on the grandparent DIV indicates the row number
        let rowId = block.parentNode.parentNode.id;
        // Extract the row number and convert to int
        let line = rowId.split("-");
        line = +line[line.length-1];
        // The number of sibling DIV's determines how much indentation to add
        let siblings = getPreviousSiblings(block.parentNode, e => (e.nodeName.toUpperCase() == "DIV"));
        // Add indentation to the code line (if necessary) and package as object with line number
        let indent = " ".repeat(4 * siblings.length);
        codeLines.push({line: line,
                        code: indent + block.innerText});
    });
    return codeLines;
}

async function loadPy() {
    // Loads Pyodide to execute code
    // Redirects stdout to function to display in an HTML element
    let pyodide = await loadPyodide({stdout: displayPyOutput});
    console.log("Pyodide loaded");
    // Loads a custom Python error handler into the Pyodide global namespace
    // It handles errors in Python because Pyodide provides only a static dump of stderr to the JS API
    await pyodide.runPython(`
    def reformat_exception():
        # Provide error information for display as Python dict
        import sys
        import traceback
        return {"exc_name": sys.last_value.__class__.__name__,
                "exc_msg": sys.last_value.args[0],
                # The line number for the exception to present to the user is actually at the bottom of the stack, not the top
                "exc_args": sys.last_value.args, # JS --> array of arrays
                "full_tb": traceback.format_exception(sys.last_type, sys.last_value, sys.last_traceback) # JS --> array of strings
                }`);
    // Creates a function context in which to run the user-submitted code. This prevents variables from leaking into the pyodide global scope.
    await pyodide.runPython(`
    def execute_code(code_str):
        exec(code_str)
        return
    `);
    return pyodide;
}

async function runPyodide(codeLines, pyodidePromise) {
    // Runs Python code in a running instance of Pyodide
    // codeLines should be an array containing objects with properties code and line (no)
    let codeBlock = codeLines.map(codeObj => {
        return codeObj.code
    }).join("\n");
    let pyodide = await pyodidePromise;
    // Get a reference to the function executor created on load()
    let execute_code = pyodide.globals.get("execute_code");
    // Get a reference to the global error handler created in load()
    let reformat_exception = pyodide.globals.get("reformat_exception");
    try {
        //await pyodide.runPython(codeBlock);
        execute_code(codeBlock);
    } catch (err) {
        handlePyException(reformat_exception());
    }
}

function handlePyException(excProxy) {
    // Handles a dict returned from the Python reformat_exception function 
    function extractLineNo(tbArray) {
        // Looks for the line number in the stack trace
        // tb should be an array of strings
        return tbArray.reduce( (result, line) => {
            if (line.includes("<string>")) {
                let match = line.match(/.+ line (\d+)/);
                if (match) result = match[1];
            }
            return result;
        }, null);
    }
    
    // Pyodide returns a PyProxy, which we can unpack into a JS map
    let pyproxies = []; // accumulate any nested proxies to destroy later (per the Pyodide documentation)
    let excMap = excProxy.toJs({pyproxies});
    let excArgs = excMap.get("exc_args"),   // should be an int
        excName = excMap.get("exc_name"),
        excMsg = excMap.get("exc_msg"); 
    for (let px of pyproxies) {
        px.destroy();
    }
    excProxy.destroy(); // to prevent memory leaks
    displayPyOutput(`${excName}: ${excMsg}`);
    // If the array of arguments has more than one element, the line number will be the second element of the array in position 1
    let lineNo = excArgs.length > 1 ? excArgs[1][1] : extractLineNo(excMap.get("full_tb"));
    console.log(excMap);
    highlightError(lineNo);
}

function highlightError(lineNo) {
    // Toggles the error CSS class on the Parson's element corresponding to the given line number 
    let block = document.querySelector(`div[id="ss-row-${lineNo}"]`).querySelector(".parsons-block");
    block.classList.toggle("parsons-error");
}

function displayPyOutput(output) {
    // Renders Python stdout/stderr to the screen
    let outputDiv = document.querySelector(".parsons-output");
    let outputSpan = document.createElement("span");
    outputSpan.classList.add("parsons-output-line");
    outputSpan.appendChild(document.createTextNode(output));
    outputDiv.appendChild(outputSpan);
}

function clearOutput() {
    // Clears Python stdout/stderr from the screen
    let outputDiv = document.querySelector(".parsons-output");
    removeAllButFirst(outputDiv);
    // remove error class on any blocks
    document.querySelectorAll(".parsons-block").forEach(elem => {
        elem.classList.remove("parsons-error");
    });
    // clear any rogue highlighting
    document.querySelectorAll(".dragover").forEach(elem => {
        elem.classList.remove("dragover");
    });
}

function resetProblem() {
    // Resets solution space; returns all blocks to problem space and shuffles order; clears output
    clearOutput();
    let blocks = document.querySelectorAll(".parsons-block"),
        problemCells = document.querySelectorAll(".parsons-ps"),
        indices = Array.from(Array(blocks.length).keys()); // array of indices for shuffling
    // shuffles indices 
    indices = indices.sort((a, b) => 0.5 - Math.random());
    // reassign blocks in new, random order
    indices.forEach((index, i) => {
        // just in case
        blocks[index].classList.remove("hidden");
        problemCells[i].appendChild(blocks[index]);
    });
    // remove all indentation markers
    let indentChars = document.querySelectorAll(".indent-char");
    indentChars.forEach(charNode => charNode.remove());

}

window.addEventListener("DOMContentLoaded", async () => {
   
    createIndents();
    // Block while Pyodide loads
    let pyodidePromise = await loadPy();

    // Get the draggable elements by class 
    // These will contain the lines of code
    const blocks = document.querySelectorAll(".parsons-block");
    // Add the ondragstart event listener to each element
    blocks.forEach(block => {
        block.addEventListener("dragstart", dragstart_handler);
        block.addEventListener("dragover", dragover_handler);
        block.addEventListener("drop", swapDrop);
        block.addEventListener("dragend", ev => {
            ev.target.classList.remove("hidden");
        })
    });
    
    // Blocks can be dragged from and dropped in any of these elements
    const dragTargets = document.querySelectorAll(".parsons-ss, .parsons-ps");
    dragTargets.forEach(target => {
        target.addEventListener("dragover", dragover_handler);
        target.addEventListener("drop", drop_handler);
    });
    // For these targets -- the solution cells -- provide more fine-grained UX
    const dropTargets = document.querySelectorAll(".parsons-ss");
    dropTargets.forEach(target => {
        target.addEventListener("dragenter", dragenter_handler);
        target.addEventListener("dragleave", dragleave_handler);
    });

      // button to trigger code execution
    const button = document.querySelector(".parsons-submit");

    button.addEventListener("click", (event) => {
        // clear output area before running new code
       clearOutput();
        let codeToRun = parseParsonsCode();
        runPyodide(codeToRun, pyodidePromise);
    });

    document.querySelector(".parsons-reset").addEventListener("click", resetProblem);

});

function getPreviousSiblings(elem, filter) {
    //this will start from the given element and collect all the previous siblings
    // source: https://stackoverflow.com/questions/4378784/how-to-find-all-siblings-of-the-currently-selected-dom-object
    let sibs = [];
    while (elem = elem.previousSibling) {
        if (elem.nodeType === 3) continue; // text node
        if (!filter || filter(elem)) sibs.push(elem);
    }
    return sibs;
}

function removeAllButFirst(elem) {
    // Removes all but the first child element of a given element
    while (elem.children.length > 1) {
        elem.children[elem.children.length-1].remove();
    }
}

function swapElements(obj1, obj2) {
    // from https://stackoverflow.com/questions/10716986/swap-two-html-elements-and-preserve-event-listeners-on-them
    // save the location of obj2
    var parent2 = obj2.parentNode;
    var next2 = obj2.nextSibling;
    // special case for obj1 is the next sibling of obj2
    if (next2 === obj1) {
        // just put obj1 before obj2
        parent2.insertBefore(obj1, obj2);
    } else {
        // insert obj2 right before obj1
        obj1.parentNode.insertBefore(obj2, obj1);

        // now insert obj1 where obj2 was
        if (next2) {
            // if there was an element after obj2, then insert obj1 right before that
            parent2.insertBefore(obj1, next2);
        } else {
            // otherwise, just append as last child
            parent2.appendChild(obj1);
        }
    }
}