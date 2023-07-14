# python-camp
Repo for lessons, homework, and course dev materials

This repository uses [jupyterbook](https://jupyterbook.org/en/stable/intro.html) to render Jupyter Notebooks and other Markdown content as HTML, hosted on the repository's GitHub Pages site. 

Notebooks can be launched in JupyterHub or downloaded for running locally.

## Using lessons 

- Each lesson in the JupyterBook format has a launch button in the upper right menu that provides an option to open the notebook in JupyterHub.
- For **registered users**, this link allows the user to open an executable notebook in a running instance of JupyterHub. (Currently, this points to a test instance, not for use in production.)
- 

## Publishing/updating lessons

1. All files for processing by JupyterBook reside in the `textbook` directory of this repo.
2. Notebooks reside in `notebooks/lessons` or `notebooks/homework` and are labeled according to their sequence. 
3. The `textbook/_toc.yml` file defines the Table of Contents for the JupyterBook; it contains the names and filenames (without extensions) of all pages for inclusion in the book.
4. Parsons Problems for select exercises are linked from the notebooks, using absolute URL's. To make a new Parsons Problem:
   - Create a YAML file in the `textbook/parsons-yaml` directory, giving it a name that includes its lesson and sequence number. (`homework-1-1.yml` refers to the first Parsons Problem in the notebook called `HW_1`.)
   - Each YAML file should contain two keys: `python_code` and `problem`. Provide a short description of the exercise under the `problem` key and provide the Python code (indented appropriately, if using code blocks) under the `python_code` key.
   - To link the Parsons Problem from the notebook, provide the full URL: `https://gwu-libraries.github.io/python-camp/parsons-problems/html/homework-1-1.html`.
5. To publish your changes, from the root of the repo, run the `./publish.sh` script. This script does the following:
  - Builds Parsons Problems from the YAML files in `textbook/parsons-yml`. 
  - Builds a clean copy of the book itself (using the `jupyter-book publish` command). This script converts the `.ipynb` files to `.html`.
  - Runs a postprocessing script to remove Sphinx directives and any cells tagged as `remove-cell` from the `.ipynb` files in `textbook/_build/html/_sources`. THese are the versions of the notebooks that end users can download or open in JupyterHub. Postprocessing makes for a cleaner user experience in the classic Jupyter environment (and allows us to remove content designed only for instructors, etc.).

## JupyterBook formatting tags

- To create a collapsible cell -- for hiding the solution to an exercise -- do the following:
  - To collapse a code cell, apply the cell tag `hide-cell`. (To apply cell tags, go to the `View--Cell Toolbar` menu in Jupyter and select `Tags`.)
  - To collapse a Markdown cell, use the Sphinx _toggle_ directive. Enclose the Markdown content in four backticks, like so
    ```
    ```` {toggle}
    
    Markdown content goes here.

    `````
    ```
  - **Important**: The classic Jupyter notebook interface will respond to neither the `hide-cell` tag nor the `toggle` directive. To hide these cells for Jupyter notebook users, use the [Exercise2](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/exercise2/readme.html) notebook extension. This extension can be used in conjunction with the `hide-cell` tag/`toggle` directive, since it does not affect the rendered JupyterBook HTML. 
    - The extension must be installed locally and enabled:
        ```
        pip install jupyter_contrib_nbextensions
        jupyter nbextension enable exercise2/main
        jupyter nbextension enable rubberband/main
        ```

- To tag a cell for removal, apply the `remove-cell` tag to the cell. These cells will be removed both from the rendered HTML and the `.ipynb` files for downloading.