
from dash import Dash, html
import dash_cytoscape as cyto

# Load extra layouts
cyto.load_extra_layouts()

from utils import load_json
from paths import PATH_DATA
from stylesheet import stylesheet

data = load_json(PATH_DATA)

#https://github.com/cytoscape/cytoscape.js-klay

app = Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        layout={
            #https://github.com/cytoscape/cytoscape.js-dagre
            'name': 'dagre',
            #'align': 'UL'
            'rankDir': "LR",
            "padding": 0,
            "rankSep": 50,
        },
        style={'width': '100%', 'height': '600px'},
        elements=data['elements'],
        stylesheet=stylesheet
    )
])



if __name__ == '__main__':
    app.run_server(debug=True)