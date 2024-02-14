import json
import re
import click
from pathlib import Path
import logging
from itertools import dropwhile
from markdown_it.renderer import RendererHTML
from myst_parser.config.main import MdParserConfig
from myst_parser.parsers.mdit import create_md_parser
import configparser

logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

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
FOOTNOTE_PATTERN = re.compile(r'\[\^\d+\]')
FOOTNOTE_ANCHOR_PAT = re.compile(r'\[\^\d+\]:')
GLOSSARY_URL = config['Constants']['GLOSSARY_URL']
IMAGE_URL = config['Constants']['IMAGE_URL']
# HTML for hint directives (dropdowns)
HINT_HTML = '''<details>
    <summary>{title}</summary>
    {content}
</details>
'''
# HTML for hidden code 
CODE_HTML = '''<details>
<summary>Click for a Solution</summary>
<pre><code>
{code}
</code></pre>
</details>
'''

# HTML to style hidden cells in NB classic
MD_STYLE = '''%%html
<style>
details {
  border: 1px solid;   border-radius: 4px;   padding: 0.5em 0.5em 0; }
summary {
  font-weight: bold;   margin: -0.5em -0.5em 0;   padding: 0.5em; background-color: rgba(233,140,61,.2);}
details[open] {
  padding: 0.5em; }
details[open] summary {
  border-bottom: 1px solid;   margin-bottom: 0.5em; background-color: rgba(66,129,81, .2); }
details li {
  margin: 10px 0;
}
</style>
'''

class Notebook:

    def __init__(self, nb_file):
        '''
        Class to hold an instance of Jupyter Notebook (JSON) for postprocessing. 
        :param nb_file: str or Path to an ipynb file.
        '''
        self.nb_json = self.load_nb(nb_file)
        self.data = self.nb_json['cells']
         # Markdown parser for inner content when creating HTML directly
        self.md = create_md_parser(MdParserConfig(), RendererHTML)

    def __iter__(self):
        # implements iteration protocol
        self.index = -1
        return self

    def __next__(self):
        # iterates through notebook cells
        if self.index < len(self.data) - 1:
            self.index += 1
            return self
        else:
            raise StopIteration
    
    def hide_tags(self):
        ''''
        Hides the Tags cell toolbar by default, to prevent users from accidentally deleting or modifying tags.
        '''
        if 'celltoolbar' in self.nb_json['metadata']:
            del self.nb_json['metadata']['celltoolbar']
        return self
    
    def clear_outputs(self):
        '''
        Clears output on cells -- assuming the student notebooks should be clean of all outputs.
        '''
        if self.data[self.index]['cell_type'] == 'code':
            self.data[self.index]['outputs'] = []
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

        if self.data[self.index]['cell_type'] == 'markdown':
            for i, line in enumerate(self.data[self.index]['source']):
                # Iterate over matches in line
                new_line = re.sub(TERM_PATTERN, term_expand, line)
                self.data[self.index]['source'][i] = new_line
        return self
    
    def ensure_hidden(self):
        '''
        Ensures that cells using the Exercise2 Jupyter Notebook extension are hidden by default. 
        '''
        if 'solution2' in self.data[self.index]['metadata']:
            self.data[self.index]['metadata']['solution2'] = 'hidden'
        return self

    def apply_hidden(self):
        '''
        Toggles the visibility of cells with the hide-cell tag.
        '''
        if 'hide-cell' in self.data[self.index]['metadata'].get('tags', []): 
            self.data[self.index]['metadata']['jupyter'] = {'source_hidden': True}
            if self.data[self.index]['cell_type'] == 'code':
                # Add comment that will be visible on toggled cell
                self.data[self.index]['source'].insert(0, '#Click to see the solution.\n')
        return self
    
    def hide_for_classic(self, cell):
        '''
        Replaces a hidden/collapsed code cell with an HTML/Markdown cell to hide the content on the "Classic" interface
        '''
        cell_source = cell['source']
        # Remove leading comment
        if cell_source[0].startswith('#'):
            cell_source.pop(0)
        cell_source = CODE_HTML.format(code=''.join(cell_source))
        # Change cell type
        cell['cell_type'] = 'markdown'
        # Remove code-specific metadata
        del cell['execution_count']
        del cell['outputs']
        cell['source'] = cell_source
        # Unhide the cell in Notebook 7
        if 'jupyter' in cell['metadata']:
            cell['metadata']['jupyter']['source_hidden'] = False
        return cell

    def strip_footnotes(self):
        '''
        Removes Markdown footnotes from a given cell
        '''
        if self.data[self.index]['cell_type'] == 'markdown':
            for i, line in enumerate(self.data[self.index]['source']):
                # Remove any lines starting with a footnote anchor
                if FOOTNOTE_ANCHOR_PAT.match(line):
                     self.data[self.index]['source'][i] = ''
                else:
                    # Delete footnote references from any other lines
                    new_line = re.sub(FOOTNOTE_PATTERN, '', line)
                    self.data[self.index]['source'][i] = new_line
        return self
    
    def inline_images(self):
        '''
        Converts MyST images directives to Markdown inline images, when they occur within larger blocks of Markdown.
        '''
        if self.data[self.index]['cell_type'] == 'markdown':
            is_directive = False
            image_url = ''
            alt_text = ''
            lines = []
            for i, line in enumerate(self.data[self.index]['source']):
                if not is_directive and (line.startswith('```{image}') or line.startswith('````{image}')):
                    is_directive = True
                    _, image_url = line.strip().split() # Assume URL separate from directive by a space
                    image_url = re.sub(r'^\./', f'{IMAGE_URL}/', image_url) # Replace initial relative path with absolute path
                elif is_directive:
                    if line.startswith(':alt:'):
                        alt_text = line.replace(':alt: ', '') # Extract alt text
                    # End of directive
                    elif line == '```\n' or line == '````\n': 
                        lines.append(f'![{alt_text}]({image_url})\n')
                        is_directive = False
                else:
                    lines.append(line)
            self.data[self.index]['source'] = lines

        return self  
    
    def remove_admonitions(self):
        '''
        Removes any cells with admonitions
        '''
        if self.data[self.index]['cell_type'] == 'markdown' and self.data[self.index]['source'] and (self.data[self.index]['source'][0].startswith('````{admonition}') or self.data[self.index]['source'][0].startswith('````{note}')):
            self.data.pop(self.index)
            # Backtrack for iteration
            self.index = self.index - 1
        return self

    def myst_to_md(self):
        '''
        Replaces MyST directives in notebook's markdown cells with regular Markdown/rendered HTML, to facilitate use in environments lacking the jupyterlab_myst plugin. 
        '''
        for i, cell in enumerate(self.nb_json['cells']):
            # Check for hidden code cells and replace with HTML
            if cell['cell_type'] == 'code' and ('hide-cell' in cell['metadata'].get('tags', [])):
                self.nb_json['cells'][i] = self.hide_for_classic(cell)
                continue
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
                case (directive, _) if DIRECTIVE_MAPPING.get(directive):
                    # Check for dropdowns
                    if cell_content[1] == ':class: dropdown\n':
                        cell_title = f'Click for a {DIRECTIVE_MAPPING.get(directive)}'
                        # Render the rest of the cell as HTML, removing blank lines first
                        inner_content = [c for c in cell_content if not c.startswith('`' * DIRECTIVE_BACKTICKS) and not c.startswith(':class:') and not c.isspace()]
                        # Remove blank lines from the resulting HTML
                        inner_content = self.md.render(''.join(inner_content))#.replace('\n\n', '')
                        cell_content = [HINT_HTML.format(title=cell_title, content=inner_content) ]   
                # No heading needed
                case _:
                    cell_content.pop(0)
            # Remove closing backticks and any class statements
            cell_content = [c for c in cell_content if not c.startswith('`' * DIRECTIVE_BACKTICKS) and not c.startswith(':class:')]
            self.nb_json['cells'][i]['source'] = cell_content
        return self
    
    def add_md_style(self):
        '''
        Adds an %%html block to the top of the notebook, allowing custom styles in classic/non-myst notebooks
        '''
        cell = {
                "cell_type": "code",
                "execution_count": 0,
                "id": "md-style",
                "metadata": {},
                "outputs": [],
                "source": [MD_STYLE]
            }
        self.data.insert(0, cell)
        return self
    
    def remove_tagged_cells(self, tags=TAGS_TO_REMOVE):
        '''
        :param tags: should be a Python set of tags. Any cells with any of these tags will be removed from the output notebook.
        '''
        self.data = [cell for cell in self.data 
                     if not (tags & set(cell['metadata'].get('tags', [])))]
        return self      

    def save_nb(self, nb_file):
        '''
        Saves notebook json at provided path
        '''          
        self.nb_json['cells'] = self.data
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
@click.option('--nb-output-md', default='textbook/_build/html/_sources/notebooks')
@click.option('--inline-images', is_flag=True, default=False)
@click.option('--remove-admonitions', is_flag=True, default=False)
@click.option('--render-md/--no-render', is_flag=True, default=True)
def main(nb_input, nb_output, nb_output_md, inline_images, remove_admonitions, render_md):
    '''
    :param nb_input: path for reading a notebook or directory containing notebooks (may be nested)
    :param nb_output: path where processed notebooks will be saved
    '''
    root = Path(__file__).parents[1]
    nb_input = root / Path(nb_input)
    nb_output = root / Path(nb_output)
    nb_output_md = root / Path(nb_output_md)
    # Create folder for storing pure-Markdown notebooks, if it doesn't exist
    if not nb_output_md.exists() and nb_output_md.is_dir:
        nb_output_md.mkdir()
    if nb_input.is_file() and nb_input.suffix == '.ipynb':
        nb_paths = [(nb_input, nb_output, nb_output_md)]
    else:
        glob = nb_input.rglob('*.ipynb')
        # Assumes output notebooks should follow the same directory structure as input notebooks, e.g., lessons and homework
        nb_paths = [(p, 
                     nb_output / p.parts[-2] / p.name, 
                     nb_output_md / p.parts[-2] / f'{p.stem}-md{p.suffix}') # Add -md to end of non-MyST notebooks
                     for p in glob if p.parts[-2] != '.ipynb_checkpoints']
    for in_, out, md_out in nb_paths:
        
        logger.info(f'Processing notebook {in_}; saving output to {out}.')
        nb = Notebook(in_)
        nb.remove_tagged_cells()
        for cell in nb:
            cell.make_glossary_links().strip_footnotes().apply_hidden().clear_outputs()
            if inline_images:
                cell.inline_images()
            if remove_admonitions:
                cell.remove_admonitions()
        nb.hide_tags().save_nb(out)
        if render_md:
            logger.info(f'Creating pure Markdown notebook at {md_out}.')
            nb.myst_to_md().add_md_style().save_nb(md_out)

if __name__ == '__main__':
    main()