import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent
import matplotlib
#matplotlib.use('Agg')
import pylab as py
from plotly.tools import mpl_to_plotly
import numpy as np
from plotly import tools
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from plotly import tools
from app import app
import theory as thy

style1={'color': 'black', 'fontSize': 14, 'display': 'inline-block','padding': 10}



layout = html.Div([
    dcc.Link('Go back to menu', href='/'),

    dcc.Markdown(dedent('''
    ## app1: quark gluon fractions
    ''')),



    html.Br(),
    html.Div('Choose kinematics: '),

    html.Div('rS=', style=style1),
    dcc.Input(id='app1-rS',type='number'
              ,min=100.,step=100.,value=5000.0,style=dict(width='10%')),

    html.Div('y3=', style=style1),
    dcc.Input(  id='app1-y3',type='number'
              ,step=0.1,value=0,style=dict(width='10%')),

    html.Div('y4=', style=style1),
    dcc.Input(  id='app1-y4',type='number'
              ,step=0.1,value=0,style=dict(width='10%')),

    html.Div('pT=', style=style1),
    dcc.Input(  id='app1-pT',type='number'
              ,min=10.0,step=10.,value=100.,style=dict(width='10%')),

    html.Div('muR/pT=', style=style1),
    dcc.Input(  id='app1-zR',type='number'
              ,step=0.1,value=1,style=dict(width='10%')),

    html.Div('muF/pT=', style=style1),
    dcc.Input(  id='app1-zF',type='number'
              ,step=0.1,value=1,style=dict(width='10%')),

    html.Br(),
    html.Br(),
    html.Div('resulting momentum fractions: '),
    html.Div(id='app1-mom-frac'),

    dcc.Graph(id='app1-graph'),
    html.Br(),

    dcc.Markdown(dedent('''
    ----
    **Author**: N. Sato (nsato@jlab.org)
    ''')),


   ]) 

@app.callback(
     Output('app1-mom-frac', 'children'),
    [ Input('app1-rS','value'),
      Input('app1-y3'       , 'value'),
      Input('app1-y4'      , 'value'),
      Input('app1-pT'      , 'value'),
      Input('app1-zR'    , 'value'),
      Input('app1-zF'     , 'value')
      ])
def update_mom_frac(rS,y3,y4,pT,zR,zF):
    xT=2.*pT/rS
    x1=0.5*xT*(np.exp( y3)+np.exp( y4))     
    x2=0.5*xT*(np.exp(-y3)+np.exp(-y4))     
    text='x1=%10.2e  x2=%10.2e'%(x1,x2)
    return text 


@app.callback(
     Output('app1-graph'   , 'figure'),
    [ Input('app1-rS','value'),
      Input('app1-y3'       , 'value'),
      Input('app1-y4'      , 'value'),
      Input('app1-pT'      , 'value'),
      Input('app1-zR'    , 'value'),
      Input('app1-zF'     , 'value')
      ])
def update_graph(rS,y3,y4,pT,zR,zF):

    xT=2.*pT/rS
    x1=0.5*xT*(np.exp( y3)+np.exp( y4))     
    x2=0.5*xT*(np.exp(-y3)+np.exp(-y4))     
    if x1<0 or x1>1: return None
    if x2<0 or x2>1: return None

    layout = go.Layout(
              yaxis=dict(
                range=[0,1],
                title='quark/gluon fractions',
                titlefont=dict(
                  family='Courier New, monospace',
                  size=18,
                  color='#7f7f7f')
                )
            )
    muR=zR*pT
    muF=zF*pT
    quark=thy.get_xsec(y3,y4,pT,rS,muR,muF,1,0)
    gluon=thy.get_xsec(y3,y4,pT,rS,muR,muF,0,1)
    tot=quark+gluon
    data = [go.Bar(
              x=['quark', 'gluon'],
              y=[quark/tot, gluon/tot],
              marker=dict(
                color=['rgba(222,45,38,0.8)','rgba(204,204,204,1)'] 
               ),
              )
            ]
    fig = go.Figure(data=data, layout=layout)
    return fig






