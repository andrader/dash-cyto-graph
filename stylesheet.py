stylesheet = [
    {
        "selector": "core",
        "style":{
            "selection-box-color": "red"
        }
    },
    {
        "selector": "node",
        "style": {
            #"label": "data(type)",
            "content": 'data(name)',
            "shape": "round-rectangle",
            "width": "100",
            "height": "60",#"data(degree)",
            "text-valign": "center",
            "text-halign": "center",
            "text-wrap": "wrap",
            "text-max-width": 80,
            "background-opacity": 0.5,
            "border-width": 1,
            "border-style": "solid",
            "border-color": "black",
            "border-opacity": 0.5,
        },
    },
    {
        "selector": 'node[type="io"]',
        "style": {
            "background-color": "lightgray",
            
        },
    },
    {
        "selector": 'node[type="process"]',
        "style": {
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
