"""
A small reporting tool, using asciidoc

"""

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
        output_dir='./reports',
        tmp_dir='./tmp',):
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
        self.body_template = body_template
        self.output_dir = output_dir
        self.tmp_dir = tmp_dir
        # cretae template environment
        #self.template_loader = jinja2.FileSystemLoader(searchpath='/')
        self.template_loader = jinja2.FileSystemLoader(searchpath=os.getcwd())
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self._render_template(template=body_template, data=body_data)

    def _render_template(self, template=None, data=None):
        """
        Render template with input data

        template: the template file
        data: the data the template should be rendered with
        """
        loaded_template = self.template_env.get_template(template)
        return loaded_template.render(data)



    def render_to_pdf(self):
        """
        Convert asciidoc to pdf
        """
        raise Exception('Continue implementation here')
