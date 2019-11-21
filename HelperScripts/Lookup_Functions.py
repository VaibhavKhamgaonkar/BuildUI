
import pandas as pd, numpy as np,os,time

class Lookup_Functions():
    ''' Class for refering the data  '''
    def __init__ (self, dataFilePath, dataFileType, noOfCatColumn, noOfTargetColumn, details):
        
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

        self.noOfCatColumns = noOfCatColumn
        self.noOfTargetColumns = noOfTargetColumn
        self.categories = [k for k,v in details.items() if v == '1' or v == '3']
        self.dateColumn = [k for k,v in details.items() if v == '6']
        self.targetColumns = [k for k,v in details.items() if v == '4']



        #self.paramterList = 'self, category, parameter, targetAttribute, aggrFlag, countryHoliday, typeOfSeasonality, confidesneRange, seasonalityType , futureDataPoint'
        #self.paramterList = self.creatParamters(number = self.noOfCatColumns, paramterList=self.paramterList) 




    def buildStatement(self, cat, val):
        return f""" 
        if {cat} is None:
            df = df
        else: 
            df[df['{val}']=={cat}]
         """

    def creatParamters(self, number, paramterList):
        for i in range(number):
            if len(paramterList)>1:
                paramterList += ', ' + 'category_' + str(i)
            else:
                paramterList += 'category_' + str(i)
        return paramterList

    
    def creatParamtersNew(self, number, paramterList):
        for i in range(number):
            paramterList += ', ' + 'category_' + str(i) + '=None'
        return paramterList


    def buildFunctionKit(self, item):
        if item == 'importStatement' or item == 'import':
            return str(f"""
import os,time,numpy as np, pandas as pd 
from collections import deque
#from app import RecordingQueue
from threading import Thread
import pickle
import holidays
from fbprophet import Prophet
import plotly.graph_objs as go
from plotly.subplots import make_subplots
            """)

        elif item == 'init' or item == 'initialise':
            return str(f"""
class Functions():
    ''' 
    Contains various Functions
    '''
    def __init__(self, dataPath = '{self.dataFilePath}', dataFileType = '{self.dataFileType}'):
        
        if dataFileType.lower() in ['pkl','pickle','cpickle']:
            with open(dataPath,'rb') as f: #MergedData_15_OCT.pkl
                #pickle.dump(data,f)
                self.df = pickle.load(f)
        #self.df.reset_index(inplace=True,drop=True)
        elif dataFileType == 'csv':
            self.df = pd.read_csv(dataPath)

        elif dataFileType == 'excel':
            self.df = pd.DataFrame()
            x = pd.read_excel(dataPath,sheet_name=None)
            if type(x) != 'pandas.core.frame.DataFrame':
                print(f'Creating Dataframe from dictinary')
                for key in x.keys():
                    self.df = pd.concat([self.df,x[key]],axis=0)
                self.df.reset_index(inplace=True, drop=True)

        print(self.df.shape)
        self.value = None
        self.forecastData = ''
        self.df_grpData = ''
            
            """)

        elif item.lower() == 'showtoprecords' or item.lower() == 'showtop':
            return str(f""" 
    def showTopRecords(self, category, targetColumn):
        df_grpBy = pd.DataFrame(self.df.groupby(by=category)['targetColumn'].sum())
        df_grpBy.reset_index(drop= False, inplace=True)
        df_grpBy.sort_values(by='targetColumn', inplace=True, ascending= False)
        df_grpBy = df_grpBy.iloc[:10]
        temp = []
        for item in df_grpBy[category]:
            temp.append(dict(label= item, value= item)) 
        return temp        
            
            """)    

        elif item.lower() == 'getcolumns' or item.lower() == 'getallcolumn':
            return str(""" 
    def getColumns(self):
        temp = []
        for col in self.df.columns:
            temp.append({'label': col, 'value': col})
        return temp
            
            """)

        elif item.lower() == 'getitems':
            return str(""" 
    def getItems(self, category, data= None):
        temp = []
        if data is None:
            data = self.df

        for col in data[category].unique():
            temp.append(dict(label= col, value= col))
        return temp
           
            """)
        
        elif item.lower() == 'forecast':
            para = 'def forecast(self, category, parameter, targetAttribute, aggrFlag, countryHoliday,typeOfSeasonality,confidesneRange, seasonalityType , futureDataPoint'
            param = 'df = self.filterDataOnParamter(self.df'
            return f"""
    {self.creatParamters(self.noOfCatColumns, para)},forecastColumn ):

        ''' Filtering the Data based on the arguments '''
        if len(parameter) != 1:
            return None,None,None

        finalDf = []
        if aggrFlag is None:
            aggrFlag = 'W'
        if parameter is None:
            return finalDf

        {self.creatParamters(self.noOfCatColumns, param)})
        # df = self.filterDataOnParamter(self.df, country, companyCode, purchasingGrp, profitCenter, costCenter, superCommodity, primaryCommodity, vendorDesc, glAccount, materialGroup)
        tempdf = df[df[category] == parameter[0]]
        df_grp = pd.DataFrame(tempdf.groupby(by=[targetAttribute])[forecastColumn].sum())
        #imputing the missing days with 0
        df_grp = df_grp.resample('D').sum().fillna(0)
        '''Aggrigating the Data using seasonal factor'''
        df_grp = df_grp.resample(aggrFlag).sum()
        df_grp.reset_index(inplace=True)
        ''' making DF as per Prophet format for time series analysis '''
        df_grp.columns = ['ds', 'y']
        
        '''fitting the model'''

        if seasonalityType == 'W':
            name= 'Weekly'
            period = 7.5
            fourierOrder = 3
            # dailySeasonality = False
            # weeklySeasonality = True
            # yearlySeasonality = True
        elif seasonalityType == 'M':
            name= 'monthly'
            period = 30.5
            fourierOrder = 5

        elif seasonalityType == 'Y':
            name= 'yearly'
            period = 365
            fourierOrder = 10
        elif seasonalityType == 'D':
            name= 'Daily'
            period = 1.5
            fourierOrder = 2
        else:
            name= 'custom'
            period = 7.5
            fourierOrder = 3
          
        m = Prophet(interval_width=(confidesneRange/100.0),yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False,
            seasonality_mode=typeOfSeasonality,holidays_prior_scale=1,
            changepoint_prior_scale=2)
        if countryHoliday is not None:
            m.add_country_holidays(country_name=countryHoliday)
        
        if seasonalityType is not None:
            m.add_seasonality(name=name, period=period, fourier_order=fourierOrder)
        
        '''Fitting the Data'''
        m.fit(df_grp)

        ''' Creaing the Future Datastamps '''
        future = m.make_future_dataframe(futureDataPoint)
        forecast = m.predict(future)
        self.forecastData = forecast
        self.df_grpData = df_grp
        return forecast,df_grp

            """
        elif item.lower() == 'getgraph':
            return """
    def getGraph(self,forecast, df_grp, parameters, futureDataPoint):
        fig = go.Figure()
        # Add traces
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'],
                            mode='lines',
                                opacity= 0.2,
                                fill='tonextx',
                                fillcolor='#afc9c8',
                                marker_color= '#afc9c8',
                                
                            name='LowerBound'))
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'],
                            mode='lines',
                                #opacity= 0.1,
                                
                                opacity= 0.2,
                                    fill='tonextx',
                                    fillcolor= '#afc9c8', #'turquoise',
                                marker_color= '#afc9c8',
                            name='UpperBound'))

        # fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'],
        #                     mode='lines',
        #                          opacity= 0.3,
        #                     name='linesUpper'))

        fig.add_trace(go.Scatter(x=df_grp['ds'], y=df_grp['y'],
                            mode='markers+lines',
                            marker_color= 'orange',
                            name='Input_data'))

        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'],
                            mode='lines',
                            opacity = 1,
                            marker_color= 'blue',
                            name='Prediction'))
        
        fig.update_layout(title= f"Forecast for {parameters[0]} for next {futureDataPoint} days ")
        return fig

            """

        elif item.lower() == 'getdecompositiongraph':
            return """
    def getDecompositionGraph(self,forecast, df_grp, holiday, checkSeasonality):
        #print(forecast.columns)
        referCode = {'W':'Weekly',
                    'M': 'monthly',
                    'D':'Daily',
                    'Y':'yearly',
                    'C':'CustomDates'
                        }

        fig = go.Figure()
        fig = make_subplots(rows=2, cols=2, subplot_titles=('Trend', 'Holidays', f'{referCode[checkSeasonality]} Trend'))
        # Add traces
        fig.add_trace(go.Scatter(x=forecast['ds'].iloc[len(df_grp):], y=forecast['trend_lower'].iloc[len(df_grp):].values,
                            mode='lines',
                                opacity= 0.7,
                                #fill='tonextx',
                                fillcolor='#75797d',
                                marker_color= '#d2d5d9',
                                name='LowerBound'),row=1,col=1)
        fig.add_trace(go.Scatter(x=forecast['ds'].loc[len(df_grp):], y=forecast['trend_upper'].iloc[len(df_grp):].values,
                                mode='lines',
                                #opacity= 0.1,
                                opacity= 0.7,
                                    fill='tonextx',
                                    fillcolor= '#75797d', #'turquoise',
                                marker_color= '#75797d',
                            name='UpperBound'),row=1,col=1)
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['trend'],
                            mode='lines',
                                opacity= 1,
                                #fill='tonextx',
                                #fillcolor='#afc9c8',
                                #marker_color= '#afc9c8',
                                
                            name='LowerBound'), row=1,col=1)
        if holiday is not None:
            fig.add_trace(go.Scatter(x=forecast['ds'], y=[str(item*100.0) +'%' for item in forecast['holidays']],
                            mode='lines',
                                opacity= 0.8,
                                text = [str(np.round(item*100.0,3)) +'%' for item in forecast['holidays']],
                                #fill='tonextx',
                                #fillcolor='#afc9c8',
                                #marker_color= '#afc9c8',
                                
                            name='Holiday'), row=1,col=2)
        
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast[referCode[checkSeasonality]],
                                mode='lines',
                                    opacity= 0.8,
                                    #fill='tonextx',
                                    #fillcolor='#afc9c8',
                                    #marker_color= '#afc9c8',
                                    
                                name=f'{referCode[checkSeasonality]} Trend'), row=2,col=1)
        
        fig.update_layout(title= f"Decomposition Plot")
        return fig

        """

        elif item.lower() == 'getdata':
            para = 'def getData(self, primaryCol, parameters, aggrFlag, targetCol'
            param = 'df = self.filterDataOnParamter(self.df'
            return f"""
    {self.creatParamters(self.noOfCatColumns, para)}, forecastColumn ):
        
        '''  forcastColumn is the name of collumn used for forcasting either quantity or Amount'''
        finalDf = []
        if aggrFlag is None:
            aggrFlag = 'W'
        if parameters is None:
            return finalDf

        {self.creatParamters(self.noOfCatColumns, param)})
        if len(parameters)==1: 
            if targetCol == 'Calendar Day':
                tempdf = df[df[primaryCol] == parameters[0]]
                df_grp = pd.DataFrame(tempdf.groupby(by=[targetCol])[forecastColumn].sum())
                ''' making the Time series Data Consistense '''
                df_grp = df_grp.resample('D').sum().fillna(0)
                ''' Aggregating the Data'''
                df_grp = df_grp.resample(aggrFlag).sum()
                df_grp.reset_index(inplace= True)
                finalDf.append(df_grp)
                return finalDf
            
            else:
                temp = df[df[primaryCol]==parameters[0]][[targetCol, forecastColumn ]].groupby(targetCol).sum().reset_index()
                x = pd.DataFrame(df[df[primaryCol]==parameters[0]][targetCol].value_counts()).reset_index()
                x['Percent'] = x[targetCol].apply(lambda a : a*100 /len(df[df[primaryCol]==parameters[0]]))
                #print(x.head())
                x.columns = ['index', str(targetCol) + '_Counts', str(parameters[0]) + '_In-Percentage']
                temp = pd.concat([temp,x], axis=1)
                temp.drop('index',axis=1,inplace = True)
                finalDf.append(temp)
                
                return finalDf
        else:
            for parameter in parameters:
                if targetCol != 'Calendar Day':
                    temp = df[df[primaryCol]==parameter][[targetCol, forecastColumn ]].groupby(targetCol).sum().reset_index()
                    x = pd.DataFrame(df[df[primaryCol]==parameter][targetCol].value_counts()).reset_index()
                    x['Percent'] = x[targetCol].apply(lambda a : a*100 /len(df[df[primaryCol]==parameter]))
                    ##print(x.head())
                    x.columns = ['index', str(targetCol) + '_Counts', str(parameter) + '_In-Percentage']
                    temp = pd.concat([temp,x], axis=1)
                    temp.drop('index',axis=1,inplace = True)
                    finalDf.append(temp)
                    
                else:
                    #print('Multiple Entries $$$$$$')
                    tempdf = df[df[primaryCol] == parameter]
                    df_grp = pd.DataFrame(tempdf.groupby(by=[targetCol])[forecastColumn].sum())
                    ''' making the Time series Data Consistense '''
                    df_grp = df_grp.resample('D').sum().fillna(0)
                    ''' Aggregating the Data'''
                    df_grp = df_grp.resample(aggrFlag).sum()
                    df_grp.reset_index(inplace= True)
                    finalDf.append(df_grp)
                    
                
            return finalDf

            """

        elif item.lower() == 'filterDataOnParamter' or item.lower()=='filterdata':
            parameter = 'def filterDataOnParamter(self, df, forecastColumn'
            #c = self.creatParamtersNew(self.noOfCatColumns, parameter)},
            temp = f"""
    {self.creatParamtersNew(self.noOfCatColumns, parameter)}, ):
                """
            for cat,val in zip(self.creatParamters(self.noOfCatColumns,'').split(','), self.categories):
                temp += self.buildStatement(cat,val )
            
            temp += """ 
        return df
        
                    """
        

            return temp
        
        
            
        

            

        


    
















    


    
    

if __name__ == "__main__":
 
    obj = Lookup_Functions(dataFilePath='D:/Projects/@createUI/online_retail_II.xlsx', noOfCatColumn=4,noOfTargetColumn=2, 
    dataFileType = 'excel', details = {'Invoice': '1', 'StockCode': '1', 'Description': '5', 'Quantity': '4', 'InvoiceDate': '6', 'Price': '4', 'Customer ID': '1', 'Country': '1'})
    x = []
    
    x .append(obj.buildFunctionKit('import'))
    x.append(obj.buildFunctionKit('init'))
    x.append(obj.buildFunctionKit('showTopRecords'))
    x.append(obj.buildFunctionKit('getColumns'))
    x.append(obj.buildFunctionKit('getItems'))
    x.append(obj.buildFunctionKit('forecast'))
    x.append(obj.buildFunctionKit('getGraph'))
    x.append(obj.buildFunctionKit('getData'))
    x.append(obj.buildFunctionKit('filterData'))



    with open('./test.py','w') as f:
        f.writelines(x)
