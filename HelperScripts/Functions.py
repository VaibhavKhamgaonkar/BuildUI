
import os,time,numpy as np, pandas as pd 
from collections import deque
#from app import RecordingQueue
from threading import Thread
import pickle
import holidays
from fbprophet import Prophet
import plotly.graph_objs as go
from plotly.subplots import make_subplots
            
class Functions():
    ''' 
    Contains various Functions
    '''
    def __init__(self, dataFilePath = 'D:/Projects/@createUI/online_retail_II.xlsx', dataFileType = 'excel'):  
        if dataFileType.lower() in ['pkl','pickle','cpickle']:
            with open(dataFilePath,'rb') as f: #MergedData_15_OCT.pkl
                #pickle.dump(data,f)
                self.df = pickle.load(f)
        #self.df.reset_index(inplace=True,drop=True)
        elif dataFileType == 'csv':
            self.df = pd.read_csv(dataFilePath)

        elif dataFileType == 'excel':
            self.df = pd.DataFrame()
            x = pd.read_excel(dataFilePath,sheet_name=None)
            if type(x) != 'pandas.core.frame.DataFrame':
                print(f'Creating Dataframe from dictinary')
                for key in x.keys():
                    self.df = pd.concat([self.df,x[key]],axis=0)
                self.df.reset_index(inplace=True, drop=True)
        for col in ['Invoice', 'StockCode', 'Customer ID', 'Country']: 
            self.df[col] = self.df[col].apply(str)
        print(self.df.shape) 
        self.value = None
        self.forecastData = ''
        self.df_grpData = ''

    @staticmethod
    def getRowCol(x):
        if x == 1:
            row,col = 1,1
            specs = [[ {'type':'domain'} for i in range(1)]]
        elif x == 2:
            row,col = 1,2

            specs = [[ {'type':'domain'} for i in range(2)]]
        elif x == 3:
            row,col = 1,3

            specs = [[{'type':'domain'} for i in range(3)]]
        elif x == 4:
            row,col = 2,2
            specs = [[ {'type':'domain'} for i in range(2)] for i in range(2)]

        else:
            col = 3
            row = int(np.ceil(x/col))
            specs = [[ {'type':'domain'} for i in range(col)] for i in range(row)]

        return row, col, specs



             
    def showTopRecords(self, category, targetColumn):
        df_grpBy = pd.DataFrame(self.df.groupby(by=category)[targetColumn].sum())
        df_grpBy.reset_index(drop= False, inplace=True)
        df_grpBy.sort_values(by=targetColumn, inplace=True, ascending= False)
        df_grpBy = df_grpBy.iloc[:25]
        temp = []
        for item in df_grpBy[category]:
            temp.append(dict(label= item, value= item)) 
        return temp        

             
    def getColumns(self):
        temp = []
        for col in self.df.columns:
            temp.append({'label': str(col), 'value': str(col)})
        return temp

    @staticmethod
    def get2ndColumnValues(df, firstColumnAtribute = None):
        temp= []
        #print(f'firstColumnAtribute :::: {firstColumnAtribute}')
        if firstColumnAtribute is None:
            return [{'label' : None, 'value': None}]
        else:
            for col in df[firstColumnAtribute].unique():
                temp.append({'label': str(col), 'value': str(col)})
            return temp


             
    def getItems(self, category, data= None):
        temp = []
        if data is None:
            data = self.df

        for col in data[category].unique():
            temp.append(dict(label= str(col), value= str(col)))
        return temp

            
    def forecast(self, category, parameter, targetAttribute, aggrFlag, countryHoliday,typeOfSeasonality,confidesneRange, seasonalityType , futureDataPoint, category_0, category_1, category_2, category_3,forecastColumn ):

        ''' Filtering the Data based on the arguments '''
        if len(parameter) != 1:
            return None,None,None

        finalDf = []
        if aggrFlag is None:
            aggrFlag = 'W'
        if parameter is None:
            return finalDf

        df = self.filterDataOnParamter(self.df,forecastColumn, category_0, category_1, category_2, category_3)
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

        
    def getData(self, primaryCol, parameters, aggrFlag, targetCol, category_0, category_1, category_2, category_3, forecastColumn ):

        '''  forcastColumn is the name of collumn used for forcasting either quantity or Amount'''
        finalDf = []
        if aggrFlag is None:
            aggrFlag = 'W'
        if parameters is None:
            return finalDf

        df = self.filterDataOnParamter(self.df, forecastColumn, category_0, category_1, category_2, category_3)
        if len(parameters)==1: 
            if targetCol == 'InvoiceDate':
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
                if targetCol != 'InvoiceDate':
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

            
    def filterDataOnParamter(self, df, forecastColumn, category_0=None, category_1=None, category_2=None, category_3=None, ):
                 
        if category_0 is None:
            df = df
        else: 
           df = df[df['Invoice']==category_0]
          
        if  category_1 is None:
            df = df
        else: 
           df = df[df['StockCode']== category_1]
          
        if  category_2 is None:
            df = df
        else: 
           df = df[df['Customer ID']== category_2]
          
        if  category_3 is None:
            df = df
        else: 
           df = df[df['Country']== category_3]
          
        return df

                    