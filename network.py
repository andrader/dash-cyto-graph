import pandas as pd
import networkx as nx

def load_data():

    df = pd.read_excel("./input/data.xlsx")

    return df

def explode_input_output(df: pd.DataFrame, source, target, sep = "\s*,\s*"):
    df = df.copy()
    df[[source,target]] = df[[source,target]].astype('string').apply(lambda x: x.str.split(sep))
    df = df.explode([source]).explode([target])
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




source = "input"
target = "output"
node_name = "processo"


dfraw = load_data()



# edges i/o level
dfedge = explode_input_output(dfraw, source, target)

# map output name -> process name
map_io_to_name = get_map_io_to_name(dfedge, source, target, node_name)

dfedge["source"] = dfedge[source].map(map_io_to_name['name'])
dfedge["target"] = dfedge[target].map(map_io_to_name['name'])

dfedge['weight'] = 1
dfedge['edge_name'] = dfedge[source]

gby = dfedge.groupby(["source", "target"], as_index=False, sort=False, dropna=False)
#df = gby[['weight']].agg('sum')

df = dfedge.copy()


g: nx.DiGraph = nx.from_pandas_edgelist(df, source="source", target="target", edge_attr=True, create_using=nx.DiGraph)


nx.set_node_attributes(g, dict(g.degree()), name='degree')

data = nx.cytoscape_data(g)

data['elements']

from paths import PATH_DATA
from utils import dump_json

path = PATH_DATA

dump_json(data, path)
