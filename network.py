import pandas as pd
import networkx as nx

from paths import PATH_CYTO_DATA
from utils import dump_json

def load_excel_data(path):
    df = pd.read_excel(path)
    return df

def split_and_explode(df: pd.DataFrame, *colunms, sep = "\s*,\s*"):

    colunms = list(colunms)
    df = df.copy()
    df[colunms] = df[colunms].astype('string').apply(lambda x: x.str.split(sep))
    for col in colunms:
        df = df.explode(col)
    return df


def get_edges(df, source, target):
    df = split_and_explode(df, source, target)
    df = df[[source, target]]
    df = df.set_axis(["source", "target"], axis=1)
    return df


def if_else(cond, true_type, false_type):
    mapper = {False:true_type, True:false_type}
    return cond.map(mapper)


def get_df_node_attrs(g, dfraw):
    df_nodes = pd.Series(g.nodes.keys()).to_frame("node")

    df_nodes['degree'] = df_nodes['node'].map(dict(g.degree()))
    
    df_nodes['type'] = if_else(df_nodes['node'].isin(dfraw['processo']), "process", "io")

    width = 20
    df_nodes['label'] = df_nodes['node'].str.wrap(width)
    df_nodes['label_width'] = df_nodes['label'].str.len() % width
    df_nodes['label_height'] = df_nodes['label'].str.contains("\n")+1

    df_nodes = df_nodes.set_index('node')
    return df_nodes

# paths connected to node
# list(nx.dfs_edges(g, "D")) # down
# list(nx.edge_dfs(g, "D")) # up

def process_graph(dfraw, return_cyto=True):

    
    # junta grafos input > processo e processo > output
    dfedge = pd.concat([
    get_edges(dfraw, "input", "processo"),
    get_edges(dfraw, "processo", "output")
    ])
    dfedge["weight"] = 1

    # GRAPH
    g: nx.DiGraph = nx.from_pandas_edgelist(dfedge, source="source", target="target", edge_attr=True, create_using=nx.DiGraph)
    
    df_nodes = get_df_node_attrs(g, dfraw)
    nx.set_node_attributes(g, df_nodes.to_dict('index'))

    if return_cyto:
        return nx.cytoscape_data(g)
    return g
    

def main(input_path, output_path):
    dfraw = load_excel_data(input_path)
    data = process_graph(dfraw, return_cyto=True)
    dump_json(data, output_path)
    print(f"SUCESSO: '{output_path}'")


if __name__=="__main__":

    input_path = "./input/data.xlsx"
    output_path = PATH_CYTO_DATA
    main(input_path, output_path)