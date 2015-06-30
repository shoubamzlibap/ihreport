import unittest
import os
import sys
import mock

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

class TestBaseReport(unittest.TestCase):
    def setUp(self):
        import base_report
        self.BaseReport = base_report.BaseReport
    
    def tearDown(self):
        pass

    def test_simple_report(self):
        """
        Simple report is created and verified
        """
        body_data = {
            'title': 'A simple test report',
            'author': 'Isaac Hailperin',
            'content': 'Lorem ipsum', }
        body_template = 'tests/templates/simple_report.txt'
        report = self.BaseReport(body_data=body_data, body_template=body_template)
        report.render_to_pdf()
        
