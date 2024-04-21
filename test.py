import pandas as pd
df = pd.read_csv('./output.csv')
print(df.head())
print(df.columns)
print(df.describe())
print(df.shape)