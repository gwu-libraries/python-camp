# python-camp
Repo for lessons, homework, and course dev materials

This repository uses [jupyterbook](https://jupyterbook.org/en/stable/intro.html) to render Jupyter Notebooks and other Markdown content as HTML, hosted on the repository's GitHub Pages site. 

Notebooks can be launched in JupyterHub or downloaded for running locally.

## Using lessons 

Each lesson in the JupyterBook format has a launch button (rocket icon) in the upper right menu that provides an option to open the notebook in JupyterHub.

- For **registered users**, this link allows the user to open an executable notebook in LAI's instance of JupyterHub. 
- Users who don't have access to LAI's JupyterHub can download the notebooks (from the same menu) for use in other environments: e.g., Jupyter Notebook/Jupyterlab, Google Colab, VS Code, etc. 
- Note that the formatted notebooks require the Jupyterlab extension [jupyterlab_myst](https://github.com/executablebooks/jupyterlab-myst). If this extension is not available, an alternative version of the notebook with less formatting can be obtained by appending `-md` to the name of the notebook in the download URL. For instance, to download the simple Markdown version of [this notebook](https://gwu-libraries.github.io/python-camp/_sources/notebooks/homework/HW_1_from_code_to_data.ipynb), the URL would be `https://gwu-libraries.github.io/python-camp/_sources/notebooks/homework/HW_1_from_code_to_data-md.ipynb`.

## Autograded homeworks/GitHub Classroom (beta)

GitHub Classroom supports autograding of assignments submitted by students from a roster. 

- Each assignment corresponds to a separate repo on GitHub. Each repo ([example](https://github.com/gwu-libraries/python-camp-hw-2-gr)) should contain only the assignment notebook, a README, and, in a `course-utils` folder, the `autograder.py` script from the `course-utils` folder in the main Python Camp repo.
- When a student accepts the invitation to an assignment, GitHub creates a new repo for that student for that particular assignment. (It's not currently possible to manage all assignments as a single repo with GitHub Classroom.) 
  - The student uploads their version of the homework notebook, and a GitHub Actions workflow runs the tests in `course-utils/autograder.py` against the committed file. 
  - Pass/fail is recorded both in the student's repo and in the GitHub Classroom site. 

To manage development in these separate assignment repos, I am experimenting with the following workflow:

  1. Each homework assignment repo is linked to the main repo as a git [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
  2. These submodule links are housed within the `homework-modules` folder of the main repo.
  3. To clone the repo with the submodules, run `git clone --recurse-submodules` on the main repo.
  4. When running the `publish.sh` script, changes made to the homework notebooks will be copied into the appropriate submodule directory within `homework-modules`, and changes pushed to the corresponding linked repo on GitHub.
  5. Changes can be pulled from the remote repos using `git submodule update --remote --merge` (or `git submodule update --remote --rebase`).

## Publishing/updating lessons

1. All files for processing by JupyterBook reside in the `textbook` directory of this repo.
2. Notebooks reside in `notebooks/lessons` or `notebooks/homework` and are labeled according to their sequence. 
3. The `textbook/_toc.yml` file defines the Table of Contents for the JupyterBook; it contains the names and filenames (without extensions) of all pages for inclusion in the book.
4. Parsons Problems for select exercises are linked from the notebooks, using absolute URL's. To make a new Parsons Problem:
   - Create a YAML file in the `textbook/parsons-yaml` directory, giving it a name that includes its lesson and sequence number. (`homework-1-1.yml` refers to the first Parsons Problem in the notebook called `HW_1`.)
   - Each YAML file should contain two or three keys: `python_code` and `problem` are required, `python_setup` is optional.  
     1. Provide a short description of the exercise under the `problem` key.
     2. Provide the Python code (indented appropriately, if using code blocks) under the `python_code` key.
     3. Any code under `python_setup` will be executed but not included in the Parsons Problem itself. This code can be used, for instance, to define a global variable to which the code in `python_code` should refer.
   - To link the Parsons Problem from the notebook, provide the full URL: `https://gwu-libraries.github.io/python-camp/parsons-problems/html/homework-1-1.html`.
5. To publish your changes, from the root of the repo, run the `./publish.sh` script. This script does the following:
  - Builds Parsons Problems from the YAML files in `textbook/parsons-yml`. 
  - Builds a clean copy of the book itself (using the `jupyter-book publish` command). This script converts the `.ipynb` files to `.html`.
  - Runs a postprocessing script to prepare the downloadable/executable notebooks, applying the following logic:
    - MyST `{term}` directives are replaced with hard-coded links to glossary terms.
    - Cells with the `hide-cell` tag are coded for hidden in the Jupyterlab/Notebook 7 interface.
    - Cells with the `remove-cell` tag are deleted, and outputs from all code cells are cleared.
    - Markdown-alternative versions (with the `-md` suffix) are created, replacing MyST directives with regular Markdown or HTML code.
  - Copies any homework notebooks for autograding (these should be labeled as follows: `HW-1-GR`, `HW-2-GR`, etc.) from the `textbook/notebooks/homework` directory to the appropriate subdirectory (these should be labeled as follows: `python-camp-hw-1-gr`, `python-camp-hw-2-gr`, etc.) in the `homework-modules` directory. These subdirectories are manages as git submodules; upon copying the files over, the `publish.sh` script will commit and push any changes (to the associated repos).
6. From the root of the `python-camp` repo, create a new commit and push to `origin main` (to update the reference to the submodule commits).

## Testing Environment

- The provided `docker-compose.yml` file will build and launch a Jupyterlab/notebook server within a Docker container with the necessary extensions. The `nginx-proxy` container can be used to make the Jupyter server available on an open port (e.g., from an AWS server). Note that this setup does provide the full functionality of JupyterHub; the Docker image is used in production as part of a Kubernetes implementation of JupyterHub; this image provides only the Jupyter server component. 