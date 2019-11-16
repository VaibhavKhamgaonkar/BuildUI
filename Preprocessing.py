import pandas as pd, numpy as np, os, time
import argparse


''' Get the dataset file '''
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--datasetPath", required=True,
	help="path to dataset File")
ap.add_argument("-t", "--type", required=True,
	help="type of dataset file excel or csv")

args = vars(ap.parse_args())

print(args['datasetPath'])
''' Reading the data'''
if args['type'].lower() == 'csv': 
    df = pd.read_csv(args['datasetPath'], nrows=5)
elif args['type'].lower() == 'excel': 
    df = pd.read_excel(args['datasetPath'],nrows=5, sheet_name=None)

if type(df) != 'pandas.core.frame.DataFrame':
    print(f'Creating Dataframe from dictinary')
    df= df[list(df.keys())[-1]]
print(df.shape)

columnDict = {}
''' Creating a dict for the type of column'''
for col in df.columns:
    print(df.head(3))
    print(f'Enter the type for the column appearing below (1 : categorical, 2 : continuous, 3 : ordinal, 4: target, 5: ignore, 6: dateColumn ) ' )
    print(f'enter choice for attribute  -- {col}: \n')
    columnDict[col]= str(input('Enter:'))


print(columnDict)