"""
This is the schema class for in table of contents
"""

from ..pt_schema import Pt_schema
from .toc_header import Toc_header
from .toc_reporting import Toc_reporting

class Table_of_contents_schema(Pt_schema):

    def set_tables(self):
        self.ingest_tables = {'toc_header': Toc_header(self.spark),
                              'toc_reporting': Toc_reporting(self.spark)}
        self.analytic_tables = {}
