import pandas as pd
import networkx as nx

from paths import PATH_DATA
from utils import dump_json

def load_data():
    df = pd.read_excel("./input/data.xlsx")
    return df

def split_and_explode(df: pd.DataFrame, *colunms, sep = "\s*,\s*"):

    colunms = list(colunms)
    df = df.copy()
    df[colunms] = df[colunms].astype('string').apply(lambda x: x.str.split(sep))
    for col in colunms:
        df = df.explode(col)
    return df

def get_map_io_to_name(dfedge, source, target, node_name):
    name_map = dfedge[[target, node_name]].drop_duplicates().set_index(target)[node_name]
    all_io = pd.concat([dfedge[source], dfedge[target]], ignore_index=True, axis=0)
    all_io = all_io.drop_duplicates().to_frame("io")
    all_io['name'] = all_io['io'].map(name_map)
    all_io['no_name'] = all_io['name'].isna()
    all_io['name'] = all_io['name'].fillna(all_io['io'])
    all_io = all_io.set_index('io')
    return all_io


def get_edges(df, source, target):
    df = split_and_explode(df, source, target)
    df = df[[source, target]]
    df = df.set_axis(["source", "target"], axis=1)
    return df

source = "input"
target = "output"
node_name = "processo"


dfraw = load_data()

dfraw = dfraw.replace({
    "A":"AAAAAA AAA AAAAAA AAAAAAAAAAAAAAA", 
    "C": "CCCCCCC CCCCCC"})




# junta grafos
# input > processo
# processo > output
dfedge = pd.concat([
get_edges(dfraw, "input", "processo"),
get_edges(dfraw, "processo", "output")
])

dfedge['weight'] = 1
dfedge['edge_name'] = ""#dfedge[source]

dfedge['label_width'] = ""

dfedge

# TO GRAPH
g: nx.DiGraph = nx.from_pandas_edgelist(dfedge, source="source", target="target", edge_attr=True, create_using=nx.DiGraph)

#
list(nx.dfs_edges(g, "D"))
list(nx.edge_dfs(g, "D"))

df_nodes = pd.Series(g.nodes.keys()).to_frame("node")

df_nodes['degree'] = df_nodes['node'].map(dict(g.degree()))
df_nodes['type'] = df_nodes['node'].isin(dfraw['processo']).map({False:"io", True:"process"})

width = 20
df_nodes['label'] = df_nodes['node'].str.wrap(width)
df_nodes['label_width'] = df_nodes['label'].str.len() % width
df_nodes['label_height'] = df_nodes['label'].str.contains("\n")+1

df_nodes = df_nodes.set_index('node')

nx.set_node_attributes(g, df_nodes.to_dict('index'))

# EXPORT
data = nx.cytoscape_data(g)
data['elements']['nodes']
path = PATH_DATA
dump_json(data, path)
