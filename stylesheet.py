stylesheet = [
    {
        "selector": "node",
        "style": {
            "label": "data(name)",
            "shape": "round-rectangle",
            "width": "(data(degree))+10",
            "height": "data(degree)+10",
            "background-color": "green",
        },
    },
    {
        "selector": "edge",
        "style": {
            "label": "data(edge_name)",
            "width": "data(weight)",
            # "line-color": "black",
            "curve-style": "bezier",
            # "line-width": "data(weight)*100",
            # "target-arrow-color": "red",
            "target-arrow-shape": "triangle",
        },
    },
]
