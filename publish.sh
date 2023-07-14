#!/bin/bash

set -e

echo "Building Parsons Problems"
python ./course-utils/parsons_builder.py

echo "Building book from scratch"
jupyter-book clean textbook/
jupyter-book build textbook/

echo "Cleaning up notebook formatting"
python ./course-utils/postprocessing.py

echo "Publishing to GH pages"
ghp-import -n -p -f textbook/_build/html