document.addEventListener("DOMContentLoaded", function() {
    let notebookUrl = document.getElementsByClassName("dropdown-launch-buttons")[0].querySelectorAll("a[href*='colab']")[0].href;
    if (notebookUrl && (notebookUrl.slice(-5) == "ipynb")) {
        notebookUrl = notebookUrl.slice(0, -6) + "-md.ipynb"; // Update Colab URL to point to simple Markdown version
        document.getElementsByClassName("dropdown-launch-buttons")[0].querySelectorAll("a[href*='colab']")[0].href = notebookUrl;
    }
});
  