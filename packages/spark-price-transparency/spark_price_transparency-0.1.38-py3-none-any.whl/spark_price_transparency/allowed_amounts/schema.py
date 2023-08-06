"""
This is the schema class for allowed amounts
"""

from ..pt_schema import Pt_schema
from .aa_header import Aa_header
from .aa_network import Aa_network

class Allowed_amounts_schema(Pt_schema):

    def set_tables(self):
        self.ingest_tables = {'aa_header': Aa_header(self.spark),
                              'aa_network': Aa_network(self.spark)}
        self.analytic_tables = {}
