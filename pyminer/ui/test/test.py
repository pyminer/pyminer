import pandas as pd
data=pd.read_csv("c:/demo/class.csv")

grouped=data.groupby('Sex').