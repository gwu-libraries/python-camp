document.addEventListener("DOMContentLoaded", function() {
    // Update the URL of the Colab launch button
    let dropdownMenu = document.getElementsByClassName("dropdown-launch-buttons")[0];
    let notebookUrl = dropdownMenu.querySelectorAll("a[href*='colab']")[0].href;
    if (notebookUrl && (notebookUrl.slice(-5) == "ipynb")) {
        notebookUrl = notebookUrl.slice(0, -6) + "-md.ipynb"; // Update Colab URL to point to simple Markdown version
        document.getElementsByClassName("dropdown-launch-buttons")[0].querySelectorAll("a[href*='colab']")[0].href = notebookUrl;
    }
    // Swap the order of the buttons
    let linkNodes = dropdownMenu.getElementsByTagName('a');
    linkNodes[0].parentNode.insertBefore(linkNodes[1], linkNodes[0]);

});
  