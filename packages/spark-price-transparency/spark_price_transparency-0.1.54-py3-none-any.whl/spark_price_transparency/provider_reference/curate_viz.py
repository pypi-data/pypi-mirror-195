"""
Provider reference is part of the in network rate curation therefore, we will use the same graphic
"""

from ..in_network_rates.curate_viz import get_curate_html as get_inr_curate_html

def get_curate_html(cat_name='main'):
    get_inr_curate_html(cat_name=cat_name)
