import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd


app = dash.Dash(__name__)

in_objectif_jour = html.Div(id="objectif-jour", children=[
                html.H2("Objectif du jour", style={"grid-row": "1 / 2"}),
                html.Label(id="l-total", children="Total Commandes"),
                dcc.Input(id="total", value="0", type="text"),
                html.Label(id="l-e1", children="Etape 1"),
                dcc.Input(id="e1", value="0", type="text"),
                html.Label(id="l-e2", children="Etape 2"),
                dcc.Input(id="e2", value="0", type="text"),
                html.Label(id="l-e3", children="Etape 3"),
                dcc.Input(id="e3", value="0", type="text"),
                html.Label(id="l-e4", children="Etape 4"),
                dcc.Input(id="e4", value="0", type="text"),
                html.Label(id="l-e5", children="Etape 5"),
                dcc.Input(id="e5", value="0", type="text")
            ])

in_takt_time = html.Div(id="takt-time", children=[
                html.H2("Takt Time (par commande)"),
                html.Label(id="l-tt-total", children="Durée totale (mns)"),
                dcc.Input(id="tt-total", value="0", type="text"),
                html.Label(id="l-tt-e1", children="Etape 1 (mns)"),
                dcc.Input(id="tt-e1", value="0", type="text"),
                html.Label(id="l-tt-e2", children="Etape 2 (mns)"),
                dcc.Input(id="tt-e2", value="0", type="text"),
                html.Label(id="l-tt-e3", children="Etape 3 (mns)"),
                dcc.Input(id="tt-e3", value="0", type="text"),
                html.Label(id="l-tt-e4", children="Etape 4 (mns)"),
                dcc.Input(id="tt-e4", value="0", type="text"),
                html.Label(id="l-tt-e5", children="Etape 5 (mns)"),
                dcc.Input(id="tt-e5", value="0", type="text")
            ])

save_button = html.Button(
                            id="save-button",
                            children="Sauvegarder"
                        )
reinit_button = html.Button(
                            id="reinit-button",
                            children="Réinitialiser"
                        )

app.layout = html.Div(id="container", children=[
        html.H1("Panneau de configuration"),
        in_objectif_jour,
        in_takt_time,
        save_button,
        reinit_button,
        html.Div(id="output")
    ])


@app.callback(
        Output("output", "children"),
        [Input("save-button", "n_clicks"),
        Input("reinit-button", "n_clicks")],
        [State("total", "value"),
        State("e1", "value"),
        State("e2", "value"),
        State("e3", "value"),
        State("e4", "value"),
        State("e5", "value"),
        State("tt-total", "value"),
        State("tt-e1", "value"),
        State("tt-e2", "value"),
        State("tt-e3", "value"),
        State("tt-e4", "value"),
        State("tt-e5", "value")]
    )

def update_output(save, reinit, *states):
    return "{}, {}, {}".format(save, reinit, states)


if __name__ == '__main__':
    app.run_server(debug=True)