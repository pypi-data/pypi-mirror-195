"""
Provide Graphic to show curation

Curation for table of contents isn't straight forward - this graphic is provided for explainability
"""

def get_curate_html(cat_name='hive_metastore'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')

    def tbl_link(wh_name, tbl_name, ttip=''):
        return {'tooltip': ttip, 'href': f'./explore/data/{cat_name}/{wh_name}/{tbl_name}', 'target': "_blank"}

    with dot.subgraph(name='cluster_workflow') as c:
        c.body.append('label="Price Transparency: Table-of-Contents Workflow"')
        with c.subgraph(name='cluster_pt_raw') as r:
            r.body.append('label="pt_raw"')
            r.body.append('style="filled"')
            r.body.append('color="#808080"')
            r.body.append('fillcolor="#F5F5F5"')
            with r.subgraph(name='cluster_pt_raw_toc') as rtoc:
                rtoc.body.append('label="Table-of-Contents Files"')
                rtoc.body.append('style="filled"')
                rtoc.body.append('color="#808080"')
                rtoc.body.append('fillcolor="#DCDCDC"')
                rtoc.node('meta_toc', 'meta_toc', fillcolor='#F5F5F5', style='filled', shape='tab')
                rtoc.node('table_of_contents_file', '.../schema=table-of-contents/*.json', fillcolor='#FFFACD', style='filled',
                          shape='folder')
        with c.subgraph(name='cluster_pt_stage') as s:
            s.body.append('label="pt_stage"')
            s.body.append('style="filled"')
            s.body.append('color="#808080"')
            s.body.append('fillcolor="#F5F5F5"')
            s.node('toc', '', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'toc'), shape='point')
            s.node('toc_header', 'toc_header', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'toc_header'))
            s.node('toc_reporting', 'toc_reporting', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'toc_reporting'))
            s.node('index_reports', 'index_reports', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'index_reports'))
        with c.subgraph(name='cluster_pt') as p:
            p.body.append('label="pt"')
            p.body.append('style="filled"')
            p.body.append('color="#808080"')
            p.body.append('fillcolor="#F5F5F5"')
            p.node('v_index_reports', 'index_reports', fillcolor='#CAD9EF', style='filled,dashed', **tbl_link('pt', 'in_coverage'))

        dot.edge('table_of_contents_file', 'toc', ltail='cluster_pt_raw_toc')

        dot.edge('toc', 'toc_header')
        dot.edge('toc', 'toc_reporting')

        dot.edge('toc_header', 'index_reports')
        dot.edge('toc_reporting', 'index_reports')

        dot.edge('index_reports', 'v_index_reports')

    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="900pt" aligned=center', html)
    html = re.sub(r'font-size=\"14.00\">Fact Tables</text>', 'font-size=\"12.00\">Fact Tables</text>', html)
    html = re.sub(r'font-size=\"14.00\">Dimension Tables</text>', 'font-size=\"12.00\">Dimension Tables</text>', html)
    html = re.sub(r'font-size=\"14.00\">Reference Tables</text>', 'font-size=\"12.00\">Reference Tables</text>', html)
    html = re.sub(r'font-size=\"14.00\">DI Operational Tables</text>',
                  'font-size=\"12.00\">DI Operational Tables</text>', html)
    html = re.sub(r'stroke-width=\"2\"', 'stroke-width=\"4\"', html)
    html = re.sub(r'</svg>', '</div</svg>', html)

    return html
