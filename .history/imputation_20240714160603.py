import pandas as pd

final_df = pd.read_csv("/home/siegfried2021/Bureau/BeCode_AI/Projets/ImmoEliza/Preprocessing-Visualization/data/final_set.csv")

df _impute = finaldf.select_dtypes(include=['int', 'float'])
