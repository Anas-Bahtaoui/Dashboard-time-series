import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_table
import pandas as pd
import numpy as np
import base64

## Page 1 : Configuration Panel
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

layout1 = html.Div(id="container1", children=[
        html.H1("Panneau de configuration"),
        in_objectif_jour,
        in_takt_time,
        save_button,
        reinit_button,
        html.Div(id="output")
    ])

## Page 2 : Workshop Dashboard
# data examples to replace by actual data
df = pd.DataFrame(np.random.randint(low=0, high=10, size=(2,4)),
                columns=["S00", "S04", "S07", "S14"],
                index=["Produits finis", "Produits restants"])

detailed_df = pd.DataFrame(np.random.randint(low=0, high=10, size=(5,6)),
                columns=["S00", "S04", "S07", "S14", "Total", "Objectif"],
                index=["Etape 1", "Etape 2", "Etape 3", "Etape 4", "Etape 5"])

detailed_df.T.loc["Objectif"] = np.random.randint(low=10, high=20, size=(5,))

Etapes = ["Etape {}".format(1+k) for k in range(5)]
BB_timeX = pd.timedelta_range("00:00:00", "00:30:00", freq="1S")
BB_time3 = pd.timedelta_range("00:00:00", "01:00:00", freq="1S")
BB_time4 = pd.timedelta_range("01:00:00", "03:00:00", freq="1S")
BB_time5 = pd.timedelta_range("03:00:00", "10:00:00", freq="1S")

df_Retard = pd.DataFrame(np.random.choice(BB_timeX,size=(5,1)),index=Etapes,columns=['Actu'])

cross = 'cross.png'
tick = 'tick.png'
encoded_tick = base64.b64encode(open(tick, 'rb').read())
encoded_cross = base64.b64encode(open(cross, 'rb').read())
src_cross = 'data:image/png;base64,{}'.format(encoded_cross.decode())
src_tick = 'data:image/png;base64,{}'.format(encoded_tick.decode())

srcs = [src_tick, src_cross]
steps_states = np.random.randint(0, 2, (5,))


#generate dashboard components
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

def generate_time_data(df):
    etapes = df.T.loc["Actu"]
    prod_etapes = []
    for i in range(5):
        tmp = html.Div(id="u-e{}".format(i+1), children=[
                html.Img(src=srcs[steps_states[i]]),
                html.P(str(etapes.iloc[i])[7:]),
                html.P(etapes.index[i])
            ])
        prod_etapes.append(tmp)

    return prod_etapes


layout2 = html.Div(id="container2", children=[
        html.H1("Tableau de bord : Atelier de production"),
        generate_graph(detailed_df),
        *generate_time_data(df_Retard)
    ])

## Manager Dashboard
#data samples neeh

Etapes = ["Etape {}".format(1+k) for k in range(5)]
Items = ['SO','S04','S07','S14']
Postes = ["Machine {}".format(1+k) for k in range(8)]

BB_timeX = pd.timedelta_range("00:00:00", "00:30:00", freq="1S")
BB_time3 = pd.timedelta_range("00:00:00", "01:00:00", freq="1S")
BB_time4 = pd.timedelta_range("01:00:00", "03:00:00", freq="1S")
BB_time5 = pd.timedelta_range("03:00:00", "10:00:00", freq="1S")
Freq = ["Aujourd'hui","Cette semaine","Ce mois"]
Tor = [True , False]


df_Retard = pd.DataFrame(np.random.choice(BB_timeX,size=(5,1)),index=Etapes,columns=['Actu'])
df_RetardCum = pd.DataFrame(
np.concatenate((np.concatenate((np.random.choice(BB_time3,size=(5,1)),np.random.choice(BB_time4,size=(5,1))),1),np.random.choice(BB_time5,size=(5,1))),1), columns = Freq, index = Etapes)
df_prod = pd.DataFrame(np.random.randint(0, 2,size=(4,1)), columns = ['Selles produites'], index = Items)
df_pannes = pd.DataFrame(np.random.choice(Tor,size=(8,1)),columns = ['Panne'], index = Postes)
df_prodCum = pd.DataFrame(np.concatenate((np.concatenate((np.random.randint(0,10,size=(5,1)),np.random.randint(20,40,size=(5,1))),1),np.random.randint(60,100,size=(5,1))),1), columns = Freq, index = Etapes)



def generate_table1(df):
    return html.Table(
        # Header
        [html.Tr([html.Th("")]+[html.Th(c) for c in df.columns])] +

        # Body
        [html.Tr([html.Td(df.index[i])]
                +   [html.Td(df.iloc[i][c]) for c in df.columns])
                for i in range(len(df))],
        id='prodx'
    )

def generate_table2(df, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th("")]+[html.Th(c) for c in df.columns])] +

        # Body
        [html.Tr([html.Td(df.index[i])]
                +   [html.Td(df.iloc[i][c]) for c in df.columns])
                for i in range(len(df))],
        id='prodxCum'
    )


def generate_table3(df, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th("")]+[html.Th(c) for c in df.columns])] +

        # Body
        [html.Tr([html.Td(df.index[i])]
                +   [html.Td(str(df.iloc[i][c])) for c in df.columns])
                for i in range(len(df))],
        id='panne'
    )


def generate_tabletime1(df, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th("")]+[html.Th(c) for c in df.columns])] +

        # Body
        [html.Tr([html.Td(df.index[i])]
                +   [html.Td(str(df.iloc[i][c])[7:]) for c in df.columns])
                for i in range(len(df))],
        id='retard'
    )


def generate_tabletime2(df, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th("")]+[html.Th(c) for c in df.columns])] +

        # Body
        [html.Tr([html.Td(df.index[i])]
                +   [html.Td(str(df.iloc[i][c])[7:]) for c in df.columns])
                for i in range(len(df))],
        id='retardCum'
    )


# dash_table.DataTable(
#         id='retardCum',
#         columns=[{"name": i, "id": i} for i in dataframe.columns],
#         data=df.to_dict('records'),
#         )

# html.Table(id='retardCum',
#         # Header
#         [html.Tr([html.Th(col) for col in dataframe.columns])] ,
#
#         # Body
#         [html.Tr(dataframe.index[i]+[
#             html.Td(str(dataframe.iloc[i][col])[:7]) for col in dataframe.columns
#         ]) for i in range(min(len(dataframe), max_rows))])


layout3 = html.Div(id="container3", children=[
        html.H1("Suivi d'atelier"),
        generate_table1(df_prod.T),
        generate_table3(df_pannes.T),
        generate_tabletime1(df_Retard.T),
        generate_table2(df_prodCum),
        generate_tabletime2(df_RetardCum)
        ])

