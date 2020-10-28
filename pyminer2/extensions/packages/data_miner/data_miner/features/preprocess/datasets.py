import pandas as pd
import os
path=os.path.abspath(__file__)
dirname=os.path.dirname(os.path.abspath(__file__))

ccpp=pd.read_csv(dirname+"\\datasets\\ccpp.csv")
class_sas=pd.read_csv(dirname+"\\datasets\\class.csv")
diabetes=pd.read_csv(dirname+"\\datasets\\diabetes.csv")
iris=pd.read_csv(dirname+"\\datasets\\iris.csv")
mtcars=pd.read_csv(dirname+"\\datasets\\mtcars.csv")
mushrooms=pd.read_csv(dirname+"\\datasets\\mushrooms.csv")
uci=pd.read_csv(dirname+"\\datasets\\uci.csv")