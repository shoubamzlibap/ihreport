import unittest
import mock
import re

from .. import base_report

class TestBaseReport(unittest.TestCase):
    def setUp(self):
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
        report = self.BaseReport(
            body_data=body_data, 
            body_template='tests/templates/simple_report.txt',
            output_dir='tests/reports',
            tmp_dir='tests/tmp',)
        report.render_to_pdf()
        today = self.BaseReport.today()
        expected_asciidoc_file = 'tests/tmp/report_' + today + '.txt'
        expected_asciidoc = """= A simple test report
Isaac Hailperin


Lorem ipsum"""
        with open(expected_asciidoc_file, 'r') as fh:
            actual_asciidoc = fh.read()
        self.assertEqual(expected_asciidoc, actual_asciidoc)
        
    def test_today(self):
        """
        "Today" string constructred correctly
        """
        today = self.BaseReport.today()
        self.assertTrue(re.match('[0-9]{2}-[A-Za-z]{3}-[0-9]{4}', today))
