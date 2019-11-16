
import numpy as np, os, time, pandas as pd 
from collections import deque 
import dash_core_components as dcc 
import dash 
import plotly.graph_objs as go 
import dash_html_components as html 
from dash.dependencies import Input, Output 
from HelperScripts.Functions import Functions
from HelperScripts.Lookups import ReferLookup
import pickle 
import dash_table 
from datetime import datetime 
from plotly.subplots import make_subplots 
#import dash_bootstrap_components as dbc 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   #['https://codepen.io/chriddyp/pen/bWLwgP.css'] 
#['https://codepen.io/chriddyp/pen/bWLwgP.css'] #['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'] 
#
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] 

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  
dataPath = "D:/Projects/@createUI/online_retail_II.xlsx"
func = Functions(dataPath=dataPath, dataFileType="excel")
print(func.df.shape)

Title = 'Analytics Tool'


app.layout = html.Div([
    html.Div([
            html.H3('Data Analytics UI'),
    ],style={'text-align': 'center'}),


],style={'padding': 30},)

app.css.append_css({"external_url": [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
]})

if __name__ == '__main__':
    app.run_server(debug=True)
