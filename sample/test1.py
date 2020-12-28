from logic.roughset.roughset import RoughSet as rs
import pandas as pd

df = pd.read_csv('./test_data.csv')
print('df:\n', df,'\n')
A = ['Headache', 'Muscle-pain', 'Temperature']
r = rs(df, A).init()
print('knowledge index:\n', r.knowledge,'\n')

X = df[df['Flu'].str.contains('y')]
print('X:\n', X,'\n')

r.set_X(X)

print('lower index:\n', r.lower,'\n')
print('upper index:\n', r.upper,'\n')
