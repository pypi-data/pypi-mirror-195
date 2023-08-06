"""
This is the schema class for in network rates
"""

from ..pt_schema import Pt_schema
from .inr_header import Inr_header
from .inr_network import Inr_network
from .inr_provider import Inr_provider
from .in_coverage import In_coverage
from .in_rate import In_rate
from .in_provider import In_provider


class In_network_rates_schema(Pt_schema):

    def set_tables(self):
        self.ingest_tables = {'inr_header': Inr_header(self.spark),
                              'inr_network': Inr_network(self.spark),
                              'inr_provider': Inr_provider(self.spark)}
        self.analytic_tables = {'in_coverage': In_coverage(self.spark),
                                'in_rate': In_rate(self.spark),
                                'in_provider': In_provider(self.spark)}
