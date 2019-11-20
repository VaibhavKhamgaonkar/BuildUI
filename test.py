
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
    def __init__(self, dataPath = D:/Projects/@createUI/online_retail_II.xlsx, dataFileType = excel):

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

             
    def showTopRecords(self, category, targetColumn):
        df_grpBy = pd.DataFrame(self.df.groupby(by=category)['targetColumn'].sum())
        df_grpBy.reset_index(drop= False, inplace=True)
        df_grpBy.sort_values(by='targetColumn', inplace=True, ascending= False)
        df_grpBy = df_grpBy.iloc[:10]
        temp = []
        for item in df_grpBy[category]:
            temp.append(dict(label= item, value= item)) 
        return temp        

             
    def getColumns(self):
        temp = []
        for col in self.df.columns:
            temp.append({'label': col, 'value': col})
        return temp

             
    def getItems(self, category, data= None):
        temp = []
        if data is None:
            data = self.df

        for col in data[category].unique():
            temp.append(dict(label= item, value= item))
        return temp

            
    def forecast(self, category, parameter, targetAttribute, country, aggrFlag, countryHoliday,typeOfSeasonality,
                        confidesneRange, seasonalityType , futureDataPoint,
                        companyCode, purchasingGrp, profitCenter, costCenter, superCommodity, primaryCommodity, vendorDesc, glAccount, materialGroup, 
                        forecastColumn ):

        ''' Filtering the Data based on the arguments '''
        if len(parameter) != 1:
            ##print(f'Len(items) == {len(parameter), parameter}')
            return None,None,None

        finalDf = []
        if aggrFlag is None:
            aggrFlag = 'W'
        if parameter is None:
            return finalDf

        df = self.filterDataOnParamter(self.df, country, companyCode, purchasingGrp, profitCenter, costCenter, superCommodity, primaryCommodity, vendorDesc, glAccount, materialGroup)
        #df = df[df[forecastColumn] != '*' ]
        #print(f'After removing "*" is of shape -------{df.shape}')

        tempdf = df[df[category] == parameter[0]]
        df_grp = pd.DataFrame(tempdf.groupby(by=[targetAttribute])[forecastColumn].sum())
        #imputing the missing days with 0
        df_grp = df_grp.resample('D').sum().fillna(0)
        '''Aggrigating the Data using seasonal factor'''
        df_grp = df_grp.resample(aggrFlag).sum()
        df_grp.reset_index(inplace=True)
        ''' making DF as per Prophet format for time series analysis '''
        df_grp.columns = ['ds', 'y']
        #print(f'group by done df_grp { df_grp.shape}')
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

            