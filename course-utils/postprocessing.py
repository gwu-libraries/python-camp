import json
import re
from copy import deepcopy
import click
from pathlib import Path
import logging

logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DIRECTIVE_QUOTES = '````'
# Pattern for an {image} directive followed by a URL
IMAGE_PATTERN = re.compile('````{image}\s?(.+)\n') 
# Cells with tags in this list will be removed
TAGS_TO_REMOVE = {'instructor', 'remove-cell'}


class Notebook:

    def __init__(self, nb_file):
        '''
        Class to hold an instance of Jupyter Notebook (JSON) for postprocessing. 
        :param nb_file: str or Path to an ipynb file.
        '''
        self.nb_json = self.load_nb(nb_file)
    

    def remove_directives(self):
        '''
        Removes MyST directives from the notebook's markdown cells. Assumes such directives are enclosed in four backticks (as opposed to three for code blocks.) Leaves the inner Markdown intact. In the case of the {image} directives, replaces the content with a standard inline image reference.
        '''
        for i, cell in enumerate(self.nb_json['cells']):
            # Assumes the directive encloses the entire cell
            if cell['cell_type'] == 'markdown' and cell['source'][0].startswith(DIRECTIVE_QUOTES):
                # If image directive, extract URL and construct standard markdown expression
                image_match = IMAGE_PATTERN.match(cell['source'][0])
                if image_match:
                    image_url = image_match.group(1)
                    self.nb_json['cells'][i]['source'] = [f'![Flow chart with three boxes, one labeled Python Camp, one labeled Instructor, and one labeled Learner. The Python Camp box is connected to the other two with arrows labeled \"has one or more\"]({image_url})']
                else:
                    # Otherwise, remove enclosing backticks and directive
                    self.nb_json['cells'][i]['source'] = cell['source'][1:-1]
        return self
    
    def remove_tagged_cells(self, tags=TAGS_TO_REMOVE):
        '''
        :param tags: should be a Python set of tags. Any cells with any of these tags will be removed from the output notebook.
        '''
        output = []
        for cell in self.nb_json['cells']:
            cell_tags = cell['metadata'].get('tags', [])
            if not (tags & set(cell_tags)):
                output.append(deepcopy(cell))
        self.nb_json['cells'] = output
        return self      

    def save_nb(self, nb_file):
        '''
        Saves notebook json at provided path
        '''          
        with open(nb_file, 'w') as f:
            json.dump(self.nb_json, f)
        return self
    
    @staticmethod
    def load_nb(nb_file):
        '''
        Loads as JSON an ipynb file.
        '''
        with open(nb_file) as f:
            return json.load(f)

@click.command()
@click.option('--nb-input', default='textbook/notebooks')
@click.option('--nb-output', default='textbook/_build/html/_sources/notebooks')
def main(nb_input, nb_output):
    '''
    :param nb_input: path for reading a notebook or directory containing notebooks (may be nested)
    :param nb_output: path where processed notebooks will be saved
    '''
    root = Path(__file__).parents[1]
    nb_input = root / Path(nb_input)
    nb_output = root / Path(nb_output)
    if nb_input.is_file() and nb_input.suffix == '.ipynb':
        nb_paths = [(nb_input, nb_output)]
    else:
        glob = nb_input.rglob('*.ipynb')
        # Assumes output notebooks should follow the same directory structure as input notebooks, e.g., lessons and homework
        nb_paths = [(p, nb_output / p.parts[-2] / p.name) for p in glob if p.parts[-2] != '.ipynb_checkpoints']
    for in_, out in nb_paths:
        
        logger.info(f'Processing notebook {in_}; saving output to {out}.')
        nb = Notebook(in_)
        nb.remove_directives().remove_tagged_cells().save_nb(out)

if __name__ == '__main__':
    main()