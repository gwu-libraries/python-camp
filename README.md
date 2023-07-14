# python-camp
Repo for lessons, homework, and course dev materials

This repository uses [jupyterbook](https://jupyterbook.org/en/stable/intro.html) to render Jupyter Notebooks and other Markdown content as HTML, hosted on the repository's GitHub Pages site. 

Notebooks can be launched in JupyterHub or downloaded for running locally.

## Publishing/updating lessons

1. All files for processing by JupyterBook reside in the `textbook` directory of this repo.
2. Notebooks reside in `notebooks/lessons` or `notebooks/homework` and are labeled according to their sequence. 
3. The `textbook/_toc.yml` file defines the Table of Contents for the JupyterBook; it contains the names and filenames (without extensions) of all pages for inclusion in the book.
4. Parsons Problems for select exercises are linked from the notebooks, using absolute URL's. To make a new Parsons Problem:
   - Create a YAML file in the `textbook/parsons-yaml` directory, giving it a name that includes its lesson and sequence number. (`homework-1-1.yml` refers to the first Parsons Problem in the notebook called `HW_1`.)
   - Each YAML file should contain two keys: `python_code` and `problem`. Provide a short description of the exercise under the `problem` key and provide the Python code (indented appropriately, if using code blocks) under the `python_code` key.
   - From the repository root, run `python course-utils/parsons_builder.py`. This script will render all YAML files in `textbook/parsons-yml` using the Jinja template in the `textbook/_templates` folder.
5. To update the JupyterBook with new content, run `jupyter-book build textbook` from the repository root. This will render all notebook and markdown content in the `textbook` directory and place the resulting HTML files in the `textbook/_build` directory. 
6. In order to take advantage of the advanced Markdown features of JupyterBook (built on Sphinx) while also creating notebooks that display properly in the classic Jupyter interface, it's necessary to do some post-processing. After running a new build (step 5), 

## JupyterBook formatting tags
- To create a collapsible cell -- for hiding the solution to an exercise -- do the following:
  - To collapse a code cell, add the cell tag `hide-cell`.
  - To collapse a Markdown cell, use the Sphinx _toggle_ directive. Enclose the Markdown content in four backticks, like so
    ```
    ```` {toggle}
    
    Markdown content goes here.

    `````
    ```
  - **Important**: The classic Jupyter notebook interface will not respond to either the `hide-cell` tag or the `toggle` directive. To hide these cells for notebook users, use the [Exercise2](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/exercise2/readme.html) notebook extension. The extension must be installed and enabled