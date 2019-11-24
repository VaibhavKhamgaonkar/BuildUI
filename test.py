

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


    html.Div([
            html.Div([
                #html.Br(),
                html.Label('Select the Primary attribute'),
                
                dcc.Dropdown(
                    id='primaryAttribute',
                    options= func.getColumns(),
                    # [
                    #     {'label': 'New York City', 'value': 'NYC'},
                    #     {'label': u'Montréal', 'value': 'MTL'},
                    #     {'label': 'San Francisco', 'value': 'SF'}
                    # ],
                    value=func.getColumns()[0]['label'],
                    multi=False,
                    style={
                    'backgroundColor' :'#d4c9f0', 'fontSize':12,
                    },


                ),

                dcc.Checklist(
                    id='showTop25',
                    options= 
                    [
                        {'label': 'Show Top 25', 'value': 'top25'},
                    #     {'label': u'Montréal', 'value': 'MTL'},
                    #     {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value= ['top25'],
                    style = {'fontSize':12, 'color': '#2314f5'},
                    #multi=False


                ),
                #html.Br(),
            html.Label('Select Category'),
            dcc.Dropdown(
                id='itemsDropDown',
                options= Functions.get2ndColumnValues(func.df,firstColumnAtribute=func.df.columns[1]),
                    # {'label': 'New York City', 'value': 'NYC'},
                    # {'label': u'Montréal', 'value': 'MTL'},
                    # {'label': 'San Francisco', 'value': 'SF'},
                    # {'label': 'San Jose', 'value': 'SJ'}
                
                value='',
                multi=True,
                placeholder="Select items...",
                style={
                    'backgroundColor':'#cdf6fa', 'fontSize':12,
                },
                ),

            html.Div(id='categoryCheck',style={ 'color':'red', 'fontSize': 13,'display': 'inline-block'}),

            html.Label('Select Target Attribute', style = {'color':'blue'}),
            dcc.Dropdown(
                id='targetAttribute',
                options= func.getColumns(),
                    # {'label': 'New York City', 'value': 'NYC'},
                    # {'label': u'Montréal', 'value': 'MTL'},
                    # {'label': 'San Francisco', 'value': 'SF'},
                    # {'label': 'San Jose', 'value': 'SJ'} 
                
                value=  'InvoiceDate' ,#func.getColumns()[-7]['label'], 
                
                multi=False,
                placeholder="Select the Target Attribute",
                style = {
                    'backgroundColor': '#e2f7ab',

                }
            ),


            html.Br(),
            html.Label('Select Filtering Components',style = {'color': '#9e16a1', 'fontSize':15,}), 
            dcc.Checklist(
                    id='showOnlyAvailableDataPoints',
                    options= 
                    [
                        {'label': 'Show Only Available Data', 'value': 'yes'},
                    #     {'label': u'Montréal', 'value': 'MTL'},
                    #     {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value= ['yes'],
                    style = {'fontSize':11, 'color': '#2314f5'},
                    #multi=False


                ),
                 dcc.Dropdown(
                id='Invoice',
                options= func.getItems(category = 'Invoice'),
                value= None, 
                multi=False, 
                placeholder = 'Select Invoice', 
                style={'fontSize':12,},
            ),
             dcc.Dropdown(
                id='StockCode',
                options= func.getItems(category = 'StockCode'),
                value= None, 
                multi=False, 
                placeholder = 'Select StockCode', 
                style={'fontSize':12,},
            ),
             dcc.Dropdown(
                id='CustomerID',
                options= func.getItems(category = 'Customer ID'),
                value= None, 
                multi=False, 
                placeholder = 'Select Customer ID', 
                style={'fontSize':12,},
            ),
             dcc.Dropdown(
                id='Country',
                options= func.getItems(category = 'Country'),
                value= None, 
                multi=False, 
                placeholder = 'Select Country', 
                style={'fontSize':12,},
            ),
            
              ],className='two columns',style={'height':'800px','padding': 10, 'background-color':'#f7f3d0'}),  
              
            
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
                        options = [{'label': 'Quantity', 'value': 'Quantity'}, {'label': 'Price', 'value': 'Price'}],
                        value= 'Quantity',   
                        style = {'display': 'inline-block', 'width':'50%', 'color':'#b51f9c','verticalAlign' : "middle", }

                    ),
                    ],
                   style={'display': 'inline-block', 'width':'20%', 'fontSize':13, }, 
                ),
                 
    
                html.Div(
                    dcc.Checklist(
                        id='showForcast',
                        options= [
                        
                            {'label': 'Show Forecast', 'value': 'Yes'},
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
                    options= [
                    
                        {'label': 'Show Decomposition Graphs', 'value': 'Yes'},
                   
                    ],
                    value= [''],
                    #multi=False
                    ),
                    style={ "margin-left": 5,  'color': '#4a2775', 'fontSize':15,'display': 'inline-block'},
                ),

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

            
    ]),
],style={'padding': 30},)

 
#-----------------------------Implimenting callbacks Function ----------------------
@app.callback(Output('itemsDropDown', 'options'), [Input('primaryAttribute', "value"), Input('showTop25', "value"), Input('qtyOrAmt', "value")])
def updateList(value,checkbox, qtyOrAmt):
    print(value,checkbox, qtyOrAmt)
    if value is None :
        return [{'label' : '', 'value': ''}]
        
    else:
        if checkbox is None:
            return Functions.get2ndColumnValues(df=func.df,firstColumnAtribute=value)
        
        if len(checkbox) < 1:
            return Functions.get2ndColumnValues(df=func.df,firstColumnAtribute=value)
        else:
            return func.showTopRecords(category = value, targetColumn = qtyOrAmt )


@app.callback(Output('categoryCheck', 'children'), [Input('showForcast', "value"), Input('itemsDropDown', 'value'),])
def updateCheckCategory(showForcast,items):
    #print('we are waiting', showForcast )
    if 'Yes' in showForcast:
        if len(items)>1:
            #print('only 1 is required')
            return str("ALERT!! - Please Select only one Category when Show Forecast is selected.")


''' Clear the Show Forecast flag if target is not calendar day'''
@app.callback(Output('showForcast', 'value'), 
    [
    #Input('showDecompositionGraph', "value"),
    #Input('showForcast', "value"),
    Input('targetAttribute', "value"),
    ])
def ClearShowForecastFlag(targetAttribute):
    return ['']


#for clearing decomposition Graph graph on different attribute selection
@app.callback(Output('showDecompositionGraph', 'value'), 
    [
    #Input('showDecompositionGraph', "value"),
    Input('showForcast', "value"),
    Input('holiday', "value"),
    Input('seasonality', "value"),
    Input('checkSeasonality', "value"),
    Input('inlineWidth', "value"),
    Input('itemsDropDown', "value"),
    Input('forecastSlider', "value"),
    Input('aggregateUsing', "value"),
    Input('selectGraph', "value"), 
    Input('Invoice', "value"),Input('StockCode', "value"),Input('CustomerID', "value"),Input('Country', "value"),
    
    ])   
def updateDecompositionState(forecastFlag,holiday,seasonality,checkSeasonality,inlineWidth,itemsDropDown,forecastSlider,
                             aggrUsing, graphType , category_0, category_1, category_2, category_3  ):
    
    return ['']



#------ For displaying the Graph based on paramters selection---

@app.callback(Output('parameterGraph', 'figure'), 
    [Input('primaryAttribute', "value"),
    Input('itemsDropDown', "value"),
    
    
    Input('targetAttribute', "value"),
   
    Input('aggregateUsing', "value"),
    Input('selectGraph', "value"),
    Input('showForcast', "value"),
    Input('forecastSlider', "value"),
    Input('holiday', "value"),
    Input('seasonality', "value"),
    Input('checkSeasonality', "value"),
    Input('inlineWidth', "value"), 
    Input('Invoice', "value"),Input('StockCode', "value"),Input('CustomerID', "value"),Input('Country', "value"),
    
    Input('qtyOrAmt', "value"),

    ])
def update_graph(primary, items, targetAttribute,  aggrUsing, graphType,
                showForcast,forecastSlider,holiday,seasonality,checkSeasonality,inlineWidth , category_0, category_1, category_2, category_3 , qtyOrAmt):
    print(category_0,category_1, category_2,category_3)
    traces = []
    COLORS = np.random.randint(0,255, size=(len(items), 1, 3), dtype= 'uint8') 

    if len(['Quantity', 'Price']) > 1:
        if qtyOrAmt == 'Quantity':
            forecastColumn = 'Quantity'
        else:
            forecastColumn = 'Price'
    else:
        forecastColumn = 'Quantity'

    if items is None or  primary is None : 
        
        return {'data': traces,
        'layout': go.Layout(
            #xaxis={'title': 'xyz'},
            #yaxis={'title': 'secDD', },
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest'
            )
            }
    if 'Yes' in showForcast :
        if len(items)!=1:
            return {'data': traces,
                'layout': go.Layout(
            #xaxis={'title': 'xyz'},
            #yaxis={'title': 'secDD', },
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest'
            )
            } 
        if graphType != 'line':
            return {'data': traces,
                    'layout': go.Layout(
                #xaxis={'title': 'xyz'},
                #yaxis={'title': 'secDD', },
                #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                #legend={'x': 0, 'y': 1},
                hovermode='closest'
                )
                } 
        
        data, df_grp =  func.forecast(primary, items, targetAttribute,aggrUsing, holiday, seasonality, inlineWidth, checkSeasonality, forecastSlider, category_0, category_1, category_2, category_3, forecastColumn )
        
        

        if data is None and df_grp is None:
            print('Exiting...')
            return {'data': [],
            'layout': go.Layout(
            #xaxis={'title': 'xyz'},
            #yaxis={'title': 'secDD', },
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest'
            )
            }
    else:
        data = func.getData(primary,items, aggrUsing, targetAttribute, category_0, category_1, category_2, category_3, forecastColumn )

        # data = func.getData(primary,items,country, date, aggrUsing, targetAttribute,
        #                     companyCode, purchasingGrp, profitCenter, CostCenter, superCommodity, 
        #                     primaryCommodity, vendorDesc, glAccount, materialGroup, forecastColumn)

        
        
    row,col, specs = Functions.getRowCol(len(data))
    i,j = 1,1

    if len(items) != 0:
        #print(f'ENTERED:::{specs}, {row,col}')
        fig = make_subplots(rows=row , cols=col, specs=specs, subplot_titles=items)
    else:
        #print(f'ELSE ---- ENTERED:::{specs}, {row,col}')
        fig = make_subplots(rows=1 , cols=1, specs=[[{'type':'domain'}]],)


    for color, df,item in zip(COLORS,data,items):
        if targetAttribute != 'InvoiceDate': 
            print(f'targetAttribute {targetAttribute}...######')
            if graphType == 'scatter':
                traces.append(go.Scatter(
                        x=df[targetAttribute],
                        y=df[forecastColumn],
                        #text=df[item + '_In-Percentage'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name= item

                    )
                    )
                    
            elif graphType == 'line':
                traces.append(go.Scatter(
                        x=df[targetAttribute],
                        y=df[forecastColumn],
                        #text=df[item + '_In-Percentage'],
                        mode='lines+markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name= item

                    )
                    )
            elif graphType == 'bar':
                traces.append(go.Bar(
                        x=df[targetAttribute],
                        y=df[forecastColumn],
                        #text=df[str(item) + '_In-Percentage'],
                        #mode='markers',
                        opacity=0.7,
                            # marker={
                            #     'size': 15,
                            #     'line': {'width': 0.5, 'color': 'white'}
                            # },
                        name= item , 
                    )
                    )
            elif graphType == 'pie':
                if i <= row: #2
                    if j <= col: #3
                        fig.add_trace(go.Pie(
                                labels=df[targetAttribute],
                                values =df[forecastColumn],
                                #text= None, #df[str(item) + '_In-Percentage'],
                                #mode='markers',
                                opacity=0.7,
                                textinfo='none',
                                #textinfo='', 
                                #annotations= False,
                                    # marker={
                                    #     'size': 15,
                                    #     'line': {'width': 0.5, 'color': 'white'}
                                    # },
                                name= item,
                            
                            ), i, j,)
                        j+=1
                    else:
                        i+=1
                        j=1
        
        else:
            print('Ploting for target Attribute : Calender Date')
            if graphType == 'scatter':
                traces.append(go.Scatter(x=df[targetAttribute],
                            y=df[forecastColumn],
                            #text=df_grp,
                            mode='markers',
                            marker_color='rgba(' + str(color[0][0]+50) + ',' + str(color[0][1]+70) + ',' + str(color[0][2]+80) + str(0.5) + ')',
                            opacity=0.7,
                            
                            marker={
                                    'size': [item if item > 0 else 0.5 for item in 100 * df[forecastColumn]//np.max(df[forecastColumn])],
                                    'line': {'width': 0.5, 'color': 'white'},
                                    #'color': np.random.randn(25),
                                    #'colorscale':'plotly3',
                                    #'showscale':True
                                    
                                },
                            name = item,
                        
                        )
                        )

            elif graphType == 'bar':
                traces.append(go.Bar(x=df[targetAttribute],
                            y=df[forecastColumn],
                            #text=df_grp,
                            #mode='lines+markers',
                            #marker_color='rgba(' + str(color[0][0]+50) + ',' + str(color[0][1]+70) + ',' + str(color[0][2]+80) + str(0.5) + ')',
                            opacity=0.7,
                            
                            # marker={
                            #         'size': [item if item > 0 else 0.5 for item in 100 * df['Invoice Amount (Translated)']//np.max(df['Invoice Amount (Translated)'])],
                            #         'line': {'width': 0.5, 'color': 'white'},
                            #         #'color': np.random.randn(25),
                            #         #'colorscale':'plotly3',
                            #         #'showscale':True
                                    
                            #     },
                            name = item,
                        
                        )
                        )

            elif graphType == 'line':
                if 'Yes' in showForcast and items is not None:
                    return func.getGraph(data,df_grp, items,forecastSlider)    
                    #traces.append(fig)

                else:
                    traces.append(go.Scatter(x=df[targetAttribute],
                            y=df[forecastColumn],
                            #text=df_grp,
                            mode='lines+markers',
                            #marker_color='rgba(' + str(color[0][0]+50) + ',' + str(color[0][1]+70) + ',' + str(color[0][2]+80) + str(0.5) + ')',
                            opacity=0.7,
                            
                            marker={
                                    'size':10,
                                    #'size': [item if item > 0 else 0.5 for item in 100 * df['Invoice Amount (Translated)']//np.max(df['Invoice Amount (Translated)'])],
                                    #'line': {'width': 0.5, 'color': 'white'},
                                    #'color': np.random.randn(25),
                                    #'colorscale':'plotly3',
                                    #'showscale':True
                                    
                                },
                            name = item,
                        
                        )
                        )

            elif graphType == 'pie':
                if i <= row: #2
                    if j <= col: #3
                        fig.add_trace(go.Pie(
                                labels=df[targetAttribute],
                                values =df[forecastColumn],
                                #text=df[str(item) + '_In-Percentage'],
                                #mode='markers',
                                textinfo='none',
                                opacity=0.7, 
                                
                                    # marker={
                                    #     'size': 15,
                                    #     'line': {'width': 0.5, 'color': 'white'}
                                    # },
                                name= item,
                            
                            ), i, j,)
                        j+=1
                    else:
                        i+=1
                        j=1


    if graphType == 'pie':
        return go.Figure(fig, )

    else:
        return {'data': traces,
            'layout': go.Layout(
                xaxis={'title': str(targetAttribute), 'color': 'black'},
                yaxis={'title':  str(primary) + ' Expenses', 'color':'blue'},
                #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                #legend={'x': 0, 'y': 1},
                title = {"text": str(primary) + ' VS ' + str(targetAttribute) ,
                    "font": {"family": 'Comic Sans MS',
                                "size": 20,
                                "color": '#e811f0'}
                    },
                plot_bgcolor = '#fcfcd4',
                paper_bgcolor =  '#f7f2f7', #'#d7dadb',
                hovermode='closest',
                #textinfo='none',
                #layout_showlegend=False
            )
        }


#for decomposition Graph:------------

@app.callback(Output('subParameterGraph', 'figure'), 
    [Input('showDecompositionGraph', "value"),
    Input('showForcast', "value"),
    Input('holiday', "value"),
    #Input('seasonality', "value"),
    Input('checkSeasonality', "value"),
    ])
def updateSubparameterGraph(showDecompositionGraphFlag,forecast, holiday, checkSeasonality):

    if showDecompositionGraphFlag is None or forecast is None:
        return {'data': [],
            'layout': go.Layout(
            #xaxis={'title': 'xyz'},
            #yaxis={'title': 'secDD', },
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest'
            )
            }

    if 'Yes' in showDecompositionGraphFlag and 'Yes' in forecast:
        print("Sub-graph ================ section")
        # data, df_grp = func.forecast(category=primary,parameter=items,targetAttribute=targetAttribute,aggregateUsing=aggrUsing,countryHoliday=holiday,
        #                     typeOfSeasonality=seasonality,confidesneRange=inlineWidth,
        #                     seasonalityType=checkSeasonality,futureDataPoint=forecastSlider)
        while(len(func.df_grpData) < 1):
            time.sleep(0.25)
        
        print(f'Data found {func.df_grpData.shape}')
        if func.forecastData is None and func.df_grpData is None:
            print('Exiting...')
            return {'data': [],
            'layout': go.Layout(
            #xaxis={'title': 'xyz'},
            #yaxis={'title': 'secDD', },
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest'
            )
            }
        return func.getDecompositionGraph(forecast=func.forecastData ,df_grp=func.df_grpData, holiday= holiday,checkSeasonality= checkSeasonality)
    else:
        return {'data': [],
            'layout': go.Layout(
            #xaxis={'title': 'xyz'},
            #yaxis={'title': 'secDD', },
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest'
            )
            } 

# Filter Component callback methods


        
@app.callback( 
    Output('Invoice', 'options'),
    [Input('showOnlyAvailableDataPoints', "value"),
    Input('primaryAttribute', "value"),
    Input('itemsDropDown', "value"),
    Input('qtyOrAmt', "value"),
    ])
def updateInvoice(showOnlyAvailableData, primaryAttribute, itemsDropDown, qtyOrAmt):
    print(showOnlyAvailableData)
    if len(['Quantity', 'Price']) > 1:
        if qtyOrAmt == 'Quantity':
            forecastColumn = 'Quantity'
        else:
            forecastColumn = 'Price'
    else:
        forecastColumn = 'Quantity' 

    if len(showOnlyAvailableData) < 1: 
        return func.getItems(category='Invoice')
    else:
        if len(itemsDropDown)<1:
            return func.getItems(category='Invoice')
        
        #data = func.df
        ''' Filter the Data using primary attribute '''
        temp = pd.DataFrame()
        for item in itemsDropDown:
            temp = pd.concat([temp,func.df[func.df[primaryAttribute]== item]],axis=0).reset_index(drop=True)
        temp = func.filterDataOnParamter(df=temp, forecastColumn=forecastColumn)
        
        temp = pd.DataFrame(temp.groupby('Invoice')[forecastColumn].sum()).reset_index().sort_values(by=forecastColumn, ascending=False)
        return func.getItems(category='Invoice', data=temp)

        


       
@app.callback( 
    Output('StockCode', 'options'),
    [Input('showOnlyAvailableDataPoints', "value"),
    Input('primaryAttribute', "value"),
    Input('itemsDropDown', "value"),
    Input('qtyOrAmt', "value"),
    Input('Invoice', 'value'),
    ])
def updateStockCode (showOnlyAvailableData, primaryAttribute, itemsDropDown, qtyOrAmt, Invoice, ):
    print(showOnlyAvailableData)
    if len(['Quantity', 'Price']) > 1:
        if qtyOrAmt == 'Quantity':
            forecastColumn = 'Quantity'
        else:
            forecastColumn = 'Price'
    else:
        forecastColumn = 'Quantity' 

    if len(showOnlyAvailableData) < 1: 
        return func.getItems(category='StockCode')
    else:
        if len(itemsDropDown)<1:
            return func.getItems(category='StockCode')
        
        #data = func.df
        ''' Filter the Data using primary attribute '''
        temp = pd.DataFrame()
        for item in itemsDropDown:
            temp = pd.concat([temp,func.df[func.df[primaryAttribute]== item]],axis=0).reset_index(drop=True)
        temp = func.filterDataOnParamter(df=temp, forecastColumn=forecastColumn , category_0 = Invoice  )
        
        temp = pd.DataFrame(temp.groupby('StockCode')[forecastColumn].sum()).reset_index().sort_values(by=forecastColumn, ascending=False)
        return func.getItems(category='StockCode', data=temp)

        
       
@app.callback( 
    Output('CustomerID', 'options'),
    [Input('showOnlyAvailableDataPoints', "value"),
    Input('primaryAttribute', "value"),
    Input('itemsDropDown', "value"),
    Input('qtyOrAmt', "value"),
    Input('Invoice', 'value'),Input('StockCode', 'value'),
    ])
def updateCustomerID (showOnlyAvailableData, primaryAttribute, itemsDropDown, qtyOrAmt, Invoice,StockCode, ):
    print(showOnlyAvailableData)
    if len(['Quantity', 'Price']) > 1:
        if qtyOrAmt == 'Quantity':
            forecastColumn = 'Quantity'
        else:
            forecastColumn = 'Price'
    else:
        forecastColumn = 'Quantity' 

    if len(showOnlyAvailableData) < 1: 
        return func.getItems(category='Customer ID')
    else:
        if len(itemsDropDown)<1:
            return func.getItems(category='Customer ID')
        
        #data = func.df
        ''' Filter the Data using primary attribute '''
        temp = pd.DataFrame()
        for item in itemsDropDown:
            temp = pd.concat([temp,func.df[func.df[primaryAttribute]== item]],axis=0).reset_index(drop=True)
        temp = func.filterDataOnParamter(df=temp, forecastColumn=forecastColumn , category_0 = Invoice,  category_1 = StockCode  )
        
        temp = pd.DataFrame(temp.groupby('Customer ID')[forecastColumn].sum()).reset_index().sort_values(by=forecastColumn, ascending=False)
        return func.getItems(category='Customer ID', data=temp)

        
       
@app.callback( 
    Output('Country', 'options'),
    [Input('showOnlyAvailableDataPoints', "value"),
    Input('primaryAttribute', "value"),
    Input('itemsDropDown', "value"),
    Input('qtyOrAmt', "value"),
    Input('Invoice', 'value'),Input('StockCode', 'value'),Input('CustomerID', 'value'),
    ])
def updateCountry (showOnlyAvailableData, primaryAttribute, itemsDropDown, qtyOrAmt, Invoice,StockCode,CustomerID, ):
    print(showOnlyAvailableData)
    if len(['Quantity', 'Price']) > 1:
        if qtyOrAmt == 'Quantity':
            forecastColumn = 'Quantity'
        else:
            forecastColumn = 'Price'
    else:
        forecastColumn = 'Quantity' 

    if len(showOnlyAvailableData) < 1: 
        return func.getItems(category='Country')
    else:
        if len(itemsDropDown)<1:
            return func.getItems(category='Country')
        
        #data = func.df
        ''' Filter the Data using primary attribute '''
        temp = pd.DataFrame()
        for item in itemsDropDown:
            temp = pd.concat([temp,func.df[func.df[primaryAttribute]== item]],axis=0).reset_index(drop=True)
        temp = func.filterDataOnParamter(df=temp, forecastColumn=forecastColumn , category_0 = Invoice,  category_1 = StockCode,  category_2 = CustomerID  )
        
        temp = pd.DataFrame(temp.groupby('Country')[forecastColumn].sum()).reset_index().sort_values(by=forecastColumn, ascending=False)
        return func.getItems(category='Country', data=temp)

        





































        





app.css.append_css({"external_url": [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
]})

if __name__ == '__main__':
    app.run_server(debug=True)
