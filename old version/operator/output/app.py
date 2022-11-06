#-*- coding:utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import datetime, time


## data examples to replace by actual data
df = pd.DataFrame(np.random.randint(low=0, high=10, size=(2,4)),
                columns=["S00", "S04", "S07", "S14"],
                index=["Produits finis", "Produits restants"])

detailed_df = pd.DataFrame(np.random.randint(low=0, high=10, size=(5,6)),
                columns=["S00", "S04", "S07", "S14", "Total", "Objectif"],
                index=["Etape 1", "Etape 2", "Etape 3", "Etape 4", "Etape 5"])

detailed_df.T.loc["Objectif"] = np.random.randint(low=10, high=20, size=(5,))

## visualizing functions (chunks of the dashboard)
def generate_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th("")]+[html.Th(c) for c in df.columns])] +

        # Body
        [html.Tr([html.Td(df.index[i])]
                +   [html.Td(df.iloc[i][c]) for c in df.columns])
                for i in range(len(df))]
    )

def generate_graph(detailed_df):
    objectif = detailed_df.T.loc["Objectif"]
    prod_etapes = []
    step = 1
    for i in detailed_df.index:
        if (i!="Objectif"):
            prod_etapes.append({
                "type" : "indicator",
                "mode" : "gauge",
                "value" : 100*detailed_df.loc[i][3]/objectif[i],
                "domain" : {'x': [0.1, 1], 'y': [step-.1, step]},
                "title" : {'text' :"<b>" + i + "</b>"},
                "gauge" : {
                    'shape': "bullet",
                    "bar" : {
                                "color" : "7ba448",
                                "thickness" : 1
                            },
                    'axis': {
                                'range': [None, 100],
                                'visible': False
                            },
                    'steps': [
                                {'range': [0, 20], 'color':'e9f0df'},
                                {'range': [20, 40], 'color':'d4e0c0'},
                                {'range': [40, 60], 'color':'e9f0df'},
                                {'range': [60, 80], 'color':'d4e0c0'},
                                {'range': [80, 100], 'color':'e9f0df'}
                                # {'range': [20, 40], 'color':'e9f0df'},
                                # {'range': [40, 60], 'color':'d4e0c0'},
                                # {'range': [60, 80], 'color':'bed1a2'},
                                # {'range': [80, 100], 'color':'a8c284'}
                            ]
                    }
                })
            step = step - .2

    return dcc.Graph(
        id='production-chart',
        figure= {
            "data": prod_etapes,
            "layout" : {
                "title": 'Production en cours'
            }
        }
    )

def generate_time_data(detailed_df):
    N = 8
    now = time.localtime()
    s_hour = datetime.datetime(now.tm_year, now.tm_mon, now.tm_mday, 7, 0, 0)
    e_hour = datetime.datetime(now.tm_year, now.tm_mon, now.tm_mday, 18, 0, 0)

    x = [s_hour.hour+k*(e_hour.hour-s_hour.hour)/N for k in range(0, N+1)]

    prod_etapes = []

    for i in detailed_df.index:
        if (i!="Objectif"):
            y = np.cumsum(np.random.randint(0, 2, (N+1,)))
            prod_etapes.append({
                "x": x,
                "y": y,
                "mode":"lines+markers",
                "name": i
            })


    return dcc.Graph(
        id="time-evolution",
        figure= {
            "data": prod_etapes,
            "layout":{
                "title":"Evolution temporelle"
            }
        }
    )
    # return html.Div(children=
    #     [html.P("Etat constaté depuis : ")] +
    #     [html.Ul([
    #         html.Li(i + " : " + " heure(s),  minute(s),  seconde(s)") for i in detailed_df.index
    #     ])]
    # )

## Dash application definition
app = dash.Dash(__name__)

app.layout = html.Div(children=[
        html.H1("Tableau de bord : Atelier de production"),
        generate_table(df),
        generate_graph(detailed_df),
        generate_time_data(detailed_df)
    ])

if __name__ == '__main__':
    app.run_server(debug=True)