import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
file = "/home/siegfried2021/Bureau/BeCode_AI/Projets/ImmoEliza/Preprocessing-Visualization/data/final_dataset.json"
df = pd.read_json(file)
# data_csv = df.to_csv(data)

# importing json with postcodes, and reducing the postcode df to the postcode column
file_postcodes = "preprocessing/georef-belgium-postal-codes.json"
df_postcodes = pd.read_json(file_postcodes)
df_postcodes = df_postcodes[["postcode"]]

print(df.shape)

# merging properties dataset with postcode df
df = df.merge(df_postcodes, how="inner", right_on="postcode")
print(df.shape)
print(df.columns)

# print(df[df["PostalCode"].apply(lambda x: x < 1000 or x > 10000)]["Url"])