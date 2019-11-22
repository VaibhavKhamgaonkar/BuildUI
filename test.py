

import numpy as np, os, time, pandas as pd 
from collections import deque 
import dash_core_components as dcc 
import dash 
import plotly.graph_objs as go 
import dash_html_components as html 
from dash.dependencies import Input, Output 
#from HelperScripts.Lookup_Functions import Lookup_Functions
#from HelperScripts.Lookup_Layout import Lookup_layout
from HelperScripts.Functions import Functions
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
func = Functions(dataFilePath=dataPath, dataFileType="excel")
print(func.df.shape)

Title = 'Analytics Tool'


app.layout = html.Div([
    html.Div([
            html.H3('Data Analytics UI'),
    ],style={'text-align': 'center'}),

 
    #=============Forecasting Area ======================================
            html.Div([
                html.Div(html.H6('Forecast Paramters',style={'text-align': 'center', 'color':'#b00471'})),

                html.Div(
                    [
                    html.Label('Select the Data Aggregating value ', style={'width':'15%','verticalAlign' : "middle", 'display': 'inline-block'}),
                    html.Div(dcc.Dropdown(
                            id='aggregateUsing',
                            options= 
                                [ 
                                {'label': 'Day Level', 'value': 'D'},
                                {'label': 'Week Level', 'value': 'W'},
                                {'label': 'Monthy', 'value': 'M'},
                                {'label': 'Yearly', 'value': 'Y'}
                            ],
                            value='W',
                            multi=False,
                            placeholder="Select aggregating Value...",
                            style= { 'backgroundColor':'#d2f0a5', 'width':'100%', },
                            ),
                            style= { 'width':'20%', 'display': 'inline-block', 'verticalAlign' : "middle"},
                    ),
                    ],
                    style={ 'width':'80%', 'color': '#603c73', 'verticalAlign' : "middle", 'fontSize':13, },

                ),
                # html.Div(
                #     [




                #     ],
                #     style={ 'width':'20%', 'color': '#603c73', 'fontSize':13,},

                # ),



                html.Div(
                    children=[
                        html.Label('Select Country Holidays',),

                        dcc.Dropdown(
                            id='holiday',
                            options= 
                                [{'label': 'US', 'value': 'US'},
                                {'label': 'India', 'value': 'IN'},
                                {'label': 'Brazil', 'value': 'BR'},
                                {'label': 'China ', 'value': 'CN'},
                                {'label': 'Russia', 'value': 'RU'},
                                {'label': 'Malaysia ', 'value': 'MY'},
                                {'label': 'Turkey  ', 'value': 'TU'},
                                {'label': 'Vietnam ', 'value': 'VN'},
                                {'label': 'Thailand  ', 'value': 'TH'},
                                {'label': 'Philippines   ', 'value': 'PH'},
                                {'label': 'Pakistan   ', 'value': 'PK'},
                                {'label': 'Bangladesh    ', 'value': 'BD'},
                                {'label': 'Indonesia     ', 'value': 'ID'}],

                            value= 'US', #func.getDateRange()[0]['label'],
                            multi=False,
                            placeholder='Include Holidays',
                            style = {'width':'70%','display': 'inline-block',},
                            ),
                    ],
                    style={ "margin-left": 0, 'width':'20%', 'color': '#603c73', 'fontSize':12,'display': 'inline-block'},
                ),

                html.Div(
                    children = [
                        html.Label('Select the Seasonality Method'),

                        dcc.Dropdown(
                        id='seasonality',
                        options= 
                            [{'label': 'Multiplicative', 'value': 'multiplicative'},
                            {'label': 'Additive', 'value': 'additive'},
                            ],

                        value= 'multiplicative', #func.getDateRange()[0]['label'],
                        multi=False,
                        placeholder='Select Seasonality Factor',
                        style = {'width':'100%', 'fontSize': 12, 'fontColor':'blue', 'display': 'inline-block'},
                        ),
                    ],
                    style={ "margin-left": 0, 'width':'15%', 'color': '#603c73', 'fontSize':13,'display': 'inline-block'},
                ),


                html.Div(
                    children = [ 
                        html.Label('Include Seasonality',),

                        dcc.Dropdown(
                        id='checkSeasonality',
                        options= 
                            [{'label': 'Weekly', 'value': 'W'},
                            {'label': 'Monthly', 'value': 'M'},
                            {'label': 'Yearly', 'value': 'Y'},
                            {'label': 'Daily', 'value': 'D'},

                            ],

                        value= 'W', #func.getDateRange()[0]['label'],
                        multi=False,
                        placeholder='Add Seasonality Factor',
                        style = {'width':'70%', 'display': 'inline-block'},
                        ),
                    ],
                    style={ "margin-left": 5,'width':'20%', 'color': '#603c73', 'fontSize':12,'display': 'inline-block'},
                    #style={ "margin-left": 5, 'align':'right','width':'100%',},

                ),

                # html.Div(
                #     dcc.Checklist(
                #         id='showForcast',
                #         options= 
                #         [
                #             {'label': 'Show Forecast', 'value': 'Yes'},
                #         #     {'label': u'Montréal', 'value': 'MTL'},
                #         #     {'label': 'San Francisco', 'value': 'SF'}
                #         ],
                #         value= [],
                #         labelStyle={'color': '#0004ed', 'width':'100%', 'fontSize':15,}
                #         #multi=False
                #     ),
                # style={ "margin-left": 0,  'color': '#603c73', 'fontSize':15,'display': 'inline-block'},
                # ),

                # html.Div(
                #     dcc.Checklist(
                #     id='showDecompositionGraph',
                #     options= 
                #     [
                #         {'label': 'Show Decomposition Graphs', 'value': 'Yes'},
                #     #     {'label': u'Montréal', 'value': 'MTL'},
                #     #     {'label': 'San Francisco', 'value': 'SF'}
                #     ],
                #     value= [''],
                #     #multi=False
                #     ),
                #     style={ "margin-left": 5,  'color': '#4a2775', 'fontSize':15,'display': 'inline-block'},
                # ),

                html.Div(html.H5('Confidense Interval',style={'color': '#6e0066', 'fontSize':15,'display': 'inline-block'})),
                #html.Div(id='output-container-confidense-slider',style={'display': 'inline-block'}),
                html.Div(dcc.Slider(
                            id = 'inlineWidth',
                            min=1,
                            max=100,
                            value=80,
                            #included=True,
                            marks={
                                50: {'label': '50%', 'style': {'color': '#77b0b1'}},
                                75: {'label': '75%', 'style':{'color':'#38a666'}},
                                25: {'label': '25%', 'style':{'color':'#38a666'}},
                                80: {'label': '80%', 'style': {'color': '#f5498e'}},
                                90: {'label': '90%','style': {'color': '#f5498e'}},
                                100: {'label': '100%', 'style': {'color': '#f5498e'}}
                            },
                            tooltip= {'always_visible': False, 'placement':'top',},

                        ),
                        style={'width': '65%', 'display': 'inline-block'},
                        ),


                html.Br(),
                html.Br(),
                html.Div(
                    [html.Label('Select the future data points', style={'width': '50'}),
                    dcc.Slider(
                        id = 'forecastSlider',
                        min=10,
                        max=365*2,
                        value=30,
                        included=True,
                        marks={
                            30: {'label': '1 month', 'style': {'color': '#77b0b1'}},
                            90: {'label': '3 months', 'style':{'color':'#38a666'}},
                            180: {'label': '6 months', 'style':{'color':'#38a666'}},
                            365: {'label': '1 year', 'style': {'color': '#f5498e'}},
                            540: {'label': '1.5 yrs'},
                            365*2: {'label': '2 yr', 'style': {'color': '#f5498e', 'width': '5%'}}
                        },
                        tooltip= {'always_visible': False, 'placement':'top',},
                ),
                ],
                style={'width': '65%', 'margin': 0 },
                ),
                #html.Div(id='output-container-range-slider',style={'margin-top': 20,'display': 'inline-block'}),
                html.Br( style= {'width': '100%'}),

                html.Div(
                    [html.Label('Select Graph type', style = {'display': 'inline-block', 'width':'30%', 'verticalAlign' : "middle", }),
                    dcc.Dropdown(
                        id='selectGraph',
                        options= [
                            {'label': 'Scatter', 'value': 'scatter'},
                            {'label': 'Bar', 'value': 'bar'},
                            {'label': 'Line', 'value': 'line'},
                            {'label': 'Pie', 'value': 'pie'},
                            # {'label': 'San Jose', 'value': 'SJ'}
                            ],
                        value='line',
                        multi=False,
                        placeholder="Select the Graph",
                        style = {'display': 'inline-block', 'width':'60%', 'margin-left': 5, 'verticalAlign' : "middle", }
                        ),
                    ],
                        style={'display': 'inline-block', 'width':'30%', 'fontSize':13, },
                ),

                html.Div(
                    [html.Label('Forecast for : ', style = {'display': 'inline-block', 'verticalAlign' : "middle", }),
                    dcc.RadioItems(
                        id='qtyOrAmt',
                        options= [
                            {'label': 'Quantity', 'value': 'qty'},
                            {'label': 'Amount', 'value': 'amt'},
                            ],
                        value='qty',
                        style = {'display': 'inline-block', 'width':'50%', 'color':'#b51f9c','verticalAlign' : "middle", }

                    ),
                    ],
                   style={'display': 'inline-block', 'width':'20%', 'fontSize':13, }, 
                ),


                html.Div(
                    dcc.Checklist(
                        id='showForcast',
                        options= 
                        [
                            {'label': 'Show Forecast', 'value': 'Yes'},
                        #     {'label': u'Montréal', 'value': 'MTL'},
                        #     {'label': 'San Francisco', 'value': 'SF'}
                        ],
                        value= [],
                        labelStyle={'color': '#0004ed', 'width':'100%', 'fontSize':15,}
                        #multi=False
                    ),
                style={ "margin-left": 0,  'color': '#603c73', 'fontSize':15,'display': 'inline-block'},
                ),

                html.Div(
                    dcc.Checklist(
                    id='showDecompositionGraph',
                    options= 
                    [
                        {'label': 'Show Decomposition Graphs', 'value': 'Yes'},
                    #     {'label': u'Montréal', 'value': 'MTL'},
                    #     {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value= [''],
                    #multi=False
                    ),
                    style={ "margin-left": 5,  'color': '#4a2775', 'fontSize':15,'display': 'inline-block'},
                ),


                #html.Br(),


            ],className='two columns',style={'width':'1000px','padding': 5, 'background-color':'#f2efed'}), 

            
            #==============================Graph Area=======================================
            #html.Br(),
            html.Div(
                    dcc.Graph(id='parameterGraph',
                    style = {'bgcolor': '#fcfcd4', 'paper_bgcolor': '#f7f2f7'}

                    ),className='ten columns',style={'padding-top': 5,}
            ), 

            html.Div(
                    dcc.Graph(id='subParameterGraph',
                    style = {'bgcolor': '#fcfcd4', 'paper_bgcolor': '#f7f2f7'},
                    ),
              className='ten columns', style={'padding-left': 80,}
            ),

            
],style={'padding': 30},)

app.css.append_css({"external_url": [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
]})

if __name__ == '__main__':
    app.run_server(debug=True)
