from course_utils.postprocessing import Notebook
import unittest
import json

class TestPostProcessing(unittest.TestCase):

    def setUp(self):
        self.notebook = Notebook('tests/test_postprocessing.ipynb')
        self.notebook.remove_tagged_cells()
        for cell in self.notebook:
            cell.make_glossary_links().apply_hidden().clear_outputs()
        self.notebook.hide_tags()
    
    def testProcessing(self):

        self.assertEqual(self.notebook.data[0]['outputs'], [], 
                         'cell output not cleared')
        self.assertRegex(self.notebook.data[1]['source'][0], r'\[.+\]\(https://gwu-libraries\.github.io/python-camp/glossary\.html#.+\)', 
                         'Markdown link missing or malformed')
        self.assertEqual(self.notebook.data[2]['source'][0], '#Click to see the solution.\n', 'Hidden code cell missing initial comment.')
        self.assertEqual(self.notebook.data[2]['metadata']['jupyter'], 
                         {"source_hidden": True},
                      'source_hidden flag missing from hidden cell metadata')
        cells_for_removal = [cell for cell in self.notebook.data if 'remove-cell' in cell['metadata'].get('tags', [])]
        self.assertEqual(cells_for_removal, [], 'cells tagged for removal not removed')

