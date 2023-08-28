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

    def testMyST2oMD(self):

        self.notebook.myst_to_md()
        self.assertEqual(self.notebook.data[3]['source'], 
                         ["#### Try it out!\n", "\n", "Use `split()` on the `term` variable (defined above) and compare the output with that of `course.split()`. \n", "\n", "Can you tell how `split()` works? How does it know where to separate the string?\n", "\n"],
                         'pure Markdown not created as expected')
        self.assertEqual(self.notebook.data[4]['source'],
                         ["<details>\n    <summary>Click for a Hint</summary>\n    <ul>\n<li>Try changing the text between quotation marks to see how the output varies.</li>\n<li>The name (left side of the equals sign) acts like a label for the value (right side of the equal sign -- here, the content between quotation marks).</li>\n<li>What do you think <code>print</code> does when it is given the name <code>my_workshop</code>?</li>\n</ul>\n\n</details>\n"],
                         'HTML for hints not created as expected'
                         )
        self.assertEqual(self.notebook.data[2]['source'], 
                         "<details>\n<summary>Click for a Solution</summary>\n<pre><code>\nmsg = 'This cell should be hidden'\nprint(msg)\n</code></pre>\n</details>\n",
                         'HTML for code solutions not created as expected')
        self.notebook.add_md_style()
        assert self.notebook.data[0]['source'][0].startswith(r'%%html'), 'expected HTML magic in first cell'