
#import speech_recognition as sr
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
    def __init__(self, dataPath = './Data/FinalData_V2.pkl', dataFileType = 'csv'):
        
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

    ''' for displaying top 25 items for perticular category '''
    
    def showTop25(self, category):
        df_grpBy = pd.DataFrame(self.df[self.df['Year']=='2019'].groupby(by=category)['Invoice Amount (Translated)'].sum())
        df_grpBy.reset_index(drop= False, inplace=True)
        df_grpBy.sort_values(by='Invoice Amount (Translated)', inplace=True, ascending= False)
        df_grpBy = df_grpBy.iloc[:25]
        temp = []
        for item in df_grpBy[category]:
            temp.append({'label': item, 'value': item}) 
        return temp
