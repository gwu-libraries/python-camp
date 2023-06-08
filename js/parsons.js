function dragstart_handler(ev) {
    // Add the block's id to the data transfer object
    ev.dataTransfer.setData("text/plain", ev.target.id);
    // If the block being dragged is located in a solution cell, and if the cell spans multiple columns, we need to reset it and add back another sibling 
    let oldParent = ev.target.parentNode;
    if ((oldParent.className == "parsons-ss") && oldParent.style.gridColumn.includes("span")) {
           // Reset column span on parent element
           oldParent.style.gridColumn = "";
           // Add new solution-space cell
           let ss = document.createElement("div");
           ss.className = "parsons-ss";
           // Add the event listeners to the new element
           ss.addEventListener("dragover", dragover_handler);
           ss.addEventListener("drop", drop_handler);
           // Add this to the block's grandparent
           if (oldParent.parentNode) {
               oldParent.parentNode.appendChild(ss);
           }
    }
}

function dragover_handler(ev) {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "move";
}

function disAllowDrop(ev) {
    // Added to draggable elements to prevent them becoming drop zones
    ev.stopPropagation();
}

function drop_handler(ev) {
    ev.preventDefault();
    // TO DO:  implement check to allow each row to have at most 1 block
    // If there is already a block in this row, no drop is allowed (unless it's the block being moved)
    // Get the id of the block to move to the current element
    const data = ev.dataTransfer.getData("text/plain");
    let block = document.getElementById(data);
    // remove the error class in case this is a move from a solution slot with an error applied
    block.classList.remove("parsons-error");

    // If the target is a solution cell and has a next sibling element, we remove it and set the grid-column property so that this element spans its own place and that vacated by its former sibling
    if ((ev.target.className == "parsons-ss") && ev.target.nextElementSibling) {
        ev.target.nextElementSibling.remove();
        ev.target.style.gridColumn = "span 2";
    }
    ev.target.appendChild(block);

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
    return pyodide;
}

async function runPyodide(codeLines, pyodidePromise) {
    // Runs Python code in a running instance of Pyodide
    // codeLines should be an array containing objects with properties code and line (no)
    let codeBlock = codeLines.map(codeObj => {
        return codeObj.code
    }).join("\n");
    let pyodide = await pyodidePromise;
    // Get a reference to the global error handler created in load()
    let reformat_exception = pyodide.globals.get("reformat_exception");
    try {
        await pyodide.runPython(codeBlock);
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
            if (line.includes("<exec>")) {
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

window.addEventListener("DOMContentLoaded", () => {
    // Get the draggable elements by class 
    // These will contain the lines of code
    const blocks = document.querySelectorAll(".parsons-block");
    // Add the ondragstart event listener to each element
    blocks.forEach(block => {
        block.addEventListener("dragstart", dragstart_handler);
        block.addEventListener("dragover", disAllowDrop);
    });
    
    // Get the drag targets (the drop zones)
    const targets = document.querySelectorAll(".parsons-ss, .parsons-ps");
    targets.forEach(target => {
        target.addEventListener("dragover", dragover_handler);
        target.addEventListener("drop", drop_handler);
    });

      // button to trigger code execution
    const button = document.querySelector(".parsons-submit");

    // TO DO: delay listening for drag events until Pyodide is loaded
    let pyodidePromise = loadPy();

    button.addEventListener("click", (event) => {
        // clear output area before running new code
        let outputDiv = document.querySelector(".parsons-output");
        removeAllButFirst(outputDiv);
        // remove error class on any blocks
        document.querySelectorAll(".parsons-block").forEach(elem => {
            elem.classList.remove("parsons-error");
        });
        let codeToRun = parseParsonsCode();
        runPyodide(codeToRun, pyodidePromise);
    });


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