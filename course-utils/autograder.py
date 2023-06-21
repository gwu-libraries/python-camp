import json
from itertools import groupby
import unittest
import os

def get_file_from_envvars():
    '''
    Used in lieu of command-line arguments, since technically unittest doesn't support them
    '''
    return os.environ.get('homework_nb')

def extract_nb_code(nb_json):
    '''
    Extract tagged setup, solution, and test cells from the JSON of an .ipynb file. 
    Returns a list of dicts, each dict containing setup, solution, and test case code.
    Expects each type of cell to be tagged appropriately with matching indices, e.g.,
       setup:ex1, solution:ex1, test-case:ex1
    Expects setup, solution, and test case cells to be sequential.
    Expect each relevant metadata tag to follow the above format.
    '''
    code = []
    for cell in nb_json['cells']:
        # Filter for code cells
        if cell['cell_type'] == 'code':
            # Filter for the right kind of metadata
            tags = [t for t in cell['metadata'].get('tags', [])
                   if t.startswith('setup') or t.startswith('solution') or t.startswith('test-case')]
            if tags:
                # Assume only one relevant tag per cell
                tag_type, tag_idx = tags[0].split(':')
                code.append({'code': cell['source'],
                             'type': tag_type,
                             'index': tag_idx})
    # Group code cells according to their index (so that the setup, solution and test code for each exercise will be in the same dict)
    groups =  [list(g) for k, g in groupby(code, lambda x: x['index'])]
    # Create one dict per exercise, containing setup, solution, and test code
    # Each line of code in a cell is a separate string, so we join them for use in exec() below
    return  [{g['type']: ''.join(g['code']) for g in group} for group in groups]

class HomeWorkTest(unittest.TestCase):

    def setUp(self):
        '''
        Loads .ipynb file supplied as ENV variable when running script and extract code from notebook JSON.
        '''
        file = get_file_from_envvars()
        if not file:
            raise OSError('Required environment variable not supplied. Please run with homework_nb=[path to .ipynb file].')
        with open(file) as f:
            homework_nb = json.load(f)
        self.hw_code = extract_nb_code(homework_nb)

    def test_homework(self):
        for i, ex in enumerate(self.hw_code):
            with self.subTest(exercise=i+1):
               # Pass this as the "locals" param to the first two exec statements to store variables set by the code
               test_vars = {}
               # Run setup code, if it exists
               exec(ex.get('setup', ''), None, test_vars)
               # Run solution code
               exec(ex['solution'], None, test_vars)
               # Run test code as assertion
               # Pass our local vars dict as globals so that it can be accessed at compile time by exec()
               exec(ex['test-case'], test_vars)


if __name__ == '__main__':
    unittest.main()