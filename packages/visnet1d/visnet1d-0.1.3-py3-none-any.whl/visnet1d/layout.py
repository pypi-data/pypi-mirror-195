#! /usr/bin/env python

# Module imports
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from PIL import Image

def inputs_from_dict_list(input_list, style=None): 
    """Gets an input layout from a list of dictionary

    Args: 
        input_list (list) : A list of dictionaries where each dictionary has the fields:
            name (str) : Name of variable to be displayed to site.
            id (str) : Name to be passed to the function (also used as ID).
            value (object) : Default value to be displayed to site.
            type (str) : Type of the value.
        style (dict) : The default style for the dash.html.Div object.
            Default to None.
    Returns:
        input_layout (Dash html object) : A Dash html div object.
    """

    input_fields = []
    for dict_item in input_list:
        input_name = f"{dict_item['name']}: " if len(dict_item['name']) > 0 else ""
        field = html.Div([
            input_name,
            dcc.Input(id=dict_item["id"], value=dict_item["value"], type=dict_item["type"]),
        ])
        input_fields.append(field)

    return html.Div(input_fields, style=style)

def format_image(path, height=80):
    if path is None:
        return html.Div()
    config = {
        "modeBarButtonsToAdd": [
            "drawline",
            "drawopenpath",
            "drawclosedpath",
            "drawcircle",
            "drawrect",
            "eraseshape",
            "orbitRotation",
        ],
        #"fillFrame" : True,
    }
    fig = px.imshow(Image.open(path))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return dcc.Graph(figure=fig, config=config, style={'height': f"{height}vh"})
