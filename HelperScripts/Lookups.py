import pandas as pd, numpy as np,os,time


class ReferLookup():
    ''' Class for refering the data  '''
    def __init__ (self, dataFilePath, dataFileType):
        
        self.dataFileType = dataFileType
        self.dataFilePath = dataFilePath
        self.colAttributeDict = {
                '1' : 'categorical',
                '2' : 'continuous',
                '3' : 'ordinal', 
                '4': 'target',
                '5': 'ignore', 
                '6': 'date'

            } 

    def buildToolkit(self, item):
        if item == 'importStatement' or item == 'import':
            return str(f"""
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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets) """)

        
        elif item == 'dataPath':
            return f""" 
dataPath = "{self.dataFilePath}"
func = Functions(dataPath=dataPath, dataFileType="{self.dataFileType}")
print(func.df.shape)

Title = 'Analytics Tool'

"""
        elif item == 'openLayout':
            return """
app.layout = html.Div([
    html.Div([
            html.H3('Data Analytics UI'),
    ],style={'text-align': 'center'}),

"""

        elif item == 'closeLayout':
            return """
],style={'padding': 30},)
"""

        elif item == 'mainBlock':
            return """
app.css.append_css({"external_url": [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
]})

if __name__ == '__main__':
    app.run_server(debug=True)
"""

        elif item == 







if __name__ == "__main__":
 
    obj = ReferLookup(dataFilePath='D:/Projects/@createUI/online_retail_II.xlsx', 
    dataFileType = 'excel')
    x = []
    x .append(obj.buildToolkit('import'))
    x.append(obj.buildToolkit('dataPath'))
    x.append(obj.buildToolkit('openLayout'))
    x.append(obj.buildToolkit('closeLayout'))
    x.append(obj.buildToolkit('mainBlock'))

    with open('./test.py','w') as f:
        f.writelines(x)
