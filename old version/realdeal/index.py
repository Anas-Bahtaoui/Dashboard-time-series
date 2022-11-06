import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import layout1, layout2, layout3

app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/manager-panel':
         return layout1
    elif pathname == '/workshop-dashboard':
         return layout2
    elif pathname == '/manager-dashboard':
         return layout3
    else:
        return '404'

import callbacks

if __name__ == '__main__':
    app.run_server(debug=True)