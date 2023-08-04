import json
import re
from copy import deepcopy
import click
from pathlib import Path
import logging
from itertools import dropwhile

logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Pattern that contains Sphinx directives in the notebook JSON
DIRECTIVE_PATTERN = re.compile('````{(\w+)}\s?(.*)\n') 
DIRECTIVE_BACKTICKS = 4
# Mapping from Sphinx directives to optional literal text for Markdown headings
DIRECTIVE_MAPPING = {'image': None,
                     'admonition': None,
                     'hint': 'Hint',
                     'toggle': None}
HEADING_SUB_LEVEL = 4
# Cells with tags in this list will be removed
TAGS_TO_REMOVE = {'instructor', 'remove-cell'}
# Pattern for Sphinx glossary directive
TERM_PATTERN = re.compile(r'{term}`([A-Za-z ]+)`')
GLOSSARY_URL = 'https://gwu-libraries.github.io/python-camp/glossary.html#term-'

class Notebook:

    def __init__(self, nb_file):
        '''
        Class to hold an instance of Jupyter Notebook (JSON) for postprocessing. 
        :param nb_file: str or Path to an ipynb file.
        '''
        self.nb_json = self.load_nb(nb_file)
    
    def hide_tags(self):
        ''''
        Hides the Tags cell toolbar by default, to prevent users from accidentally deleting or modifying tags.
        '''
        if 'celltoolbar' in self.nb_json['metadata']:
            del self.nb_json['metadata']['celltoolbar']
        return self

    def make_glossary_links(self):
        '''
        Replaces instances of the {term} directive in notebook Markdown with links to the term in the glossary.
        '''
        def term_expand(match_obj):
            '''
            Function applied in re.sub to replace every instance of the {term} directive in a string with its expanded form as a Markdown link
            '''
            term = match_obj.group(1)
            return f'[{term}]({GLOSSARY_URL}{term.replace(" ", "-")})'

        for cell in self.nb_json['cells']:
            if cell['cell_type'] == 'markdown':
                for i, line in enumerate(cell['source']):
                    # Iterate over matches in line
                    new_line = re.sub(TERM_PATTERN, term_expand, line)
                    cell['source'][i] = new_line
        return self
    
    def ensure_hidden(self):
        '''
        Ensures that cells using the Exercise2 Jupyter Notebook extension are hidden by default. 
        '''
        for cell in self.nb_json['cells']:
            if 'solution2' in cell['metadata']:
                cell['metadata']['solution2'] = 'hidden'
        return self

    def remove_directives(self):
        '''
        Removes MyST directives from the notebook's markdown cells. Assumes such directives are enclosed in four backticks (as opposed to three for code blocks.) Leaves the inner Markdown intact. In the case of the {image} directives, replaces the content with a standard inline image reference.
        '''
        for i, cell in enumerate(self.nb_json['cells']):
            # Assumes the directive encloses the entire cell, excluding any blank initial lines
            cell_content = list(dropwhile(lambda x: not x or x.isspace(), cell['source']))
            m = DIRECTIVE_PATTERN.match(cell_content[0])
            if not m:
                continue
            match m.groups():
                # Custom admonition -- label provided in the text following the directive
                case ('admonition', admon_type):
                    cell_content[0] = '#' * HEADING_SUB_LEVEL + f' {admon_type}\n'
                # Image directive -- URL follows the directive
                case ('image', image_url):
                    # Extract alt text if present
                    alt_tag = [c for c in cell_content if c.startswith(':alt:')]
                    alt_text = alt_tag[0].replace(':alt: ', '') if alt_tag else ''
                    cell_content = [f'![{alt_text}]({image_url})']
                # Other directive -- no label provided, but heading needed
                case (directive, '') if DIRECTIVE_MAPPING.get(directive):
                    cell_content[0] = '#' * HEADING_SUB_LEVEL + f' {DIRECTIVE_MAPPING[directive]}\n'
                # No heading needed
                case _:
                    cell_content.pop(0)
            # Remove closing backticks and any class statements
            cell_content = [c for c in cell_content if not c.startswith('`' * DIRECTIVE_BACKTICKS) and not c.startswith(':class:')]
            self.nb_json['cells'][i]['source'] = cell_content
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
        nb.remove_directives().remove_tagged_cells().make_glossary_links().ensure_hidden().hide_tags().save_nb(out)

if __name__ == '__main__':
    main()