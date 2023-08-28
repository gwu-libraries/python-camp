from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import yaml
import click
import logging
import re
from random import shuffle
 

logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Regex for extracting leading spaces from strings of code
LEADING_SPACES = re.compile('^(\s*)\S.+')


def load_template(template_dir):
    '''
    Loads and returns Jinja template for creating Parsons Problems HTML. If template_dir is given, it is expected to be relative to the repository root. Template should be called "parsons-layout.html"
    '''
    templates_dir = Path(__file__).parents[1] / template_dir
    env = Environment(loader = FileSystemLoader(templates_dir))
    template = env.get_template('parsons-layout.html')
    return template


def load_yaml(yaml_files):
    '''
    Loops over a list of files, expected to be in valid YAML format, and loads the data and returns the objects.
    '''
    for file in yaml_files:
        with open(file) as f:
            parsons_dict = yaml.safe_load(f)
            if (not 'python_code' in parsons_dict) or (not 'problem' in parsons_dict):
                logging.warning(f'Expected key(s) missing from {file}. Each YAML file should contain a "python_code" key and an "problem" key.')
                logger.warning(f'Skipping {file}.')
                yield None
            else:
                # Strips leading/trailing whitespace from the code block and split on line breaks
                for key in ('python_code', 'python_setup'):
                    if key in parsons_dict:
                        parsons_dict[key] = parsons_dict[key].strip().split('\n')
                # Randomize code order
                shuffle(parsons_dict['python_code'])
                yield file, parsons_dict

def get_max_depth(python_code):
    '''
    Calculates the maximum depth of nested blocks in a given string of Python code. Expects whitespace to be consistent (tabs or spaces).
    '''
    spaces = [LEADING_SPACES.match(c).group(1) for c in python_code]
    lengths = [len(s) for s in spaces]
    # Find the length of the whitespace at the minimum depth (if any indentations exist)
    # Otherwise, max depth = 1
    try:
        min_length = min([l for l in lengths if l > 0])
    except ValueError:
        return 1
    max_length = max(lengths)
    # Express max depth in terms of units of min length (e.g., 12 spaces / 4 spaces = max depth of 3, 2 tabs / 1 tab = max depth of 2)
    return int(max_length / min_length)


def render_template(parsons_to_render, template, html_path):
    '''
    :param parsons_to_render: a list of tuples consisting of a file Path and a YAML object representing a Parsons Problem
    :param template: a Jinja template object
    :param html_path: path to a folder where the rendered HTML files reside. Should be relative to repository root
    '''
    for fp, parsons_dict in parsons_to_render:
        filename = fp.stem
        filepath = Path(__file__).parents[1] / html_path / filename
        logger.info(f' Rendering template for {filename}...')
        with open(f'{filepath}.html', 'w') as fhp:
            # Add max depth to template arguments
            parsons_dict['max_depth'] = get_max_depth(parsons_dict['python_code'])
            fhp.write(template.render(parsons=parsons_dict))

@click.command()
@click.option('--template-dir', default='textbook/_templates')
@click.option('--yaml-dir', default='textbook/parsons-yaml')
@click.option('--html-dir', default='textbook/parsons-assets/parsons-problems/html')
def main(template_dir, yaml_dir, html_dir):
    # load template
    template = load_template(template_dir)
    # load YAML files representing Parsons Problems
    yaml_dir = Path(__file__).parents[1] / yaml_dir
    yaml_files = yaml_dir.glob("*.yml")
    parsons_problems = [p for p in load_yaml(list(yaml_files)) if p]
    # Render HTML versions with template
    render_template(parsons_problems, template, html_dir)

if __name__ == '__main__':
    main()




