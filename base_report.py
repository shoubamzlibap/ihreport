"""
A small reporting tool, using asciidoc

"""

import calendar
import datetime
import jinja2
import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '/usr/bin'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

import a2x

class BaseReportAttributeMissing(Exception):
    pass

class BaseReport(object):
    """
    Basic reporting class.

    """

    def __init__(self, 
        body_data=None,
        body_template=None,
        output_filename=None,
        output_dir='reports',
        tmp_dir='tmp',):
        """
        Create a report object

        body_data: a dict containing the data for the report. Will be consumed by the template
                   renderer
        body_template: a template file to be rendered.
        output_dir: directory to save output to
        temp_dir: a directory to save intermediate files to
        """
        if not body_data:
            raise BaseReportAttributeMissing('body_data') 
        if not body_template:
            raise BaseReportAttributeMissing('body_template')
        self.body_data = body_data
        if output_filename: 
            self.output_filename = output_filename
        else:
            self.output_filename = 'report_' + self.today()
        self.body_template = body_template
        self.output_dir = os.getcwd() + '/' + output_dir
        self.tmp_dir = os.getcwd() + '/' + tmp_dir
        self.asciidoc = self._render_template(template=body_template, data=body_data)


    @staticmethod
    def today():
        """
        Return today formatted as dd-mmm-yyyy

        """
        today = datetime.datetime.today()
        day = str(today.day)
        if len(day) == 1: day = '0' + day
        month = calendar.month_abbr[today.month]
        year = str(today.year)
        return day + '-' + month + '-' + year


    def _render_template(self, template=None, data=None):
        """
        Render template with input data

        template: the template file
        data: the data the template should be rendered with
        """
        try:
            self.template_env
        except AttributeError:
            #self.template_loader = jinja2.FileSystemLoader(searchpath='/')
            self.template_loader = jinja2.FileSystemLoader(searchpath=os.getcwd())
            self.template_env = jinja2.Environment(loader=self.template_loader)
        loaded_template = self.template_env.get_template(template)
        return loaded_template.render(data)


    def _write_asciidoc(self):
        """
        Write rendered asciidoc to disk for further processing.

        One could probably just keep it in memory, but it is nice
        for debugging to see the asciidoc source. 
        """
        self.asciidoc_filename = self.tmp_dir + '/' + self.output_filename + '.txt'
        with open(self.asciidoc_filename, 'w') as filehandle:
            filehandle.write(self.asciidoc)


    def render_to_pdf(self):
        """
        Convert asciidoc to pdf

        """
        self._write_asciidoc()
        # can we do better then this? - like just adding the non-defaults ...
        a2x_opts = {'verbose': 0, 'keep_artifacts': False, 'backend': None, 'skip_asciidoc': False,
'destination_dir': self.output_dir, 'fop': True, 'backend_opts': '', 'dry_run': False, 'icons':
False, 'conf_file': None, 'stylesheet': None, 'epubcheck': False, 'lynx': False, 'resources':
[], 'format': 'pdf', 'resource_manifest': None, 'safe': False, 'fop_opts': '', 'xsltproc_opts':
'', 'copy': False, 'asciidoc_opts': '', 'doctype': 'book', 'xsl_file': None, 'dblatex_opts':
'', 'icons_dir': None, 'attributes': ['docinfo'], 'no_xmllint': False}
        a2x_obj = a2x.A2X(a2x_opts)
        a2x.OPTIONS = a2x_obj       # verbose and dry_run used by utility functions.
        a2x_obj.asciidoc_file = self.asciidoc_filename
        try:
            a2x_obj.load_conf()
            a2x_obj.execute()
        except KeyboardInterrupt:
            exit(1)

