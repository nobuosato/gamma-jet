#!/usr/bin/env python
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent
from app import app
from apps import app1


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

server = app.server
style={'color': 'black', 'fontSize': 14, 'display': 'inline-block','padding': 10}


index = html.Div([

    dcc.Markdown(dedent('''
    # gamma+jet 
    #### **Author**: N. Sato (nsato@jlab.org)
    ---- 
    ''')),
    html.Div('Select available apps below:'),
    html.Br(),

    dcc.Link('app1', href='/apps/app1'),#,style=style),
    html.Div('quark/gluon fractions'),
    html.Br(),


   ]) 


@app.callback(Output('page-content', 'children'),[ Input('url', 'pathname')])
def update(url):
    if    url=='/apps/app1': return app1.layout
    else: return index 

if __name__ == '__main__':
    app.run_server(debug=True)


