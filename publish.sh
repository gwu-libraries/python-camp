#!/bin/bash

set -e

shopt -s nullglob    # Use empty array if globbing pails
shopt -s nocaseglob  # Ignore case in globbing
shopt -s extglob     # Extended globbing

function update_hw_modules() {

    echo "Looking for graded homework notebooks"
    homework_files=(./textbook/notebooks/homework/HW*GR.ipynb)
    submodule_dirs=(./homework-modules/*)
    for file in "${homework_files[@]}"
    do
        # Extract file base name and remove dashes and underscores
        fname=$(basename $file .ipynb)
        fname=${fname//_/}
        fname=${fname//-/}
        # Look for matching directory/submodule
        for dir in "${submodule_dirs[@]}"
        do
            dname=$(basename $dir)
            dname=${dname##python-camp}; # Remove directory prefix
            dname=${dname//-/}
            dname=${dname//_/}
            if [[ "$fname" =~ "$dname" ]]; then
                echo "Copying ${file} to ${dir}/"
                cp ${file} ${dir}/
                echo "Committing and updating"
                git -C ${dir} commit -am "Change to ${fname}.ipynb commited from main repo"
                git -C ${dir} push origin main
            fi
        done
    done
    
}

function main() {

    echo "Building Parsons Problems"
    python ./course-utils/parsons_builder.py

    echo "Building book from scratch"
    jupyter-book clean textbook/
    jupyter-book build textbook/

    echo "Cleaning up notebook formatting"
    python ./course-utils/postprocessing.py

    echo "Publishing to GH pages"
    ghp-import -n -p -f textbook/_build/html

    echo "Updating submodules"
    update_hw_modules

    echo "Committing post-processing changes"
    # Add any new Parsons Problems created in step one
    git add textbook/parsons-assets/parsons-problems/html
    git commit -a -m "Committing submodule changes"

}

main
