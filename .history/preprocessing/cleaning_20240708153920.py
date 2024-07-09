import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
file = "/home/siegfried2021/Bureau/BeCode_AI/Projets/ImmoEliza/Preprocessing-Visualization/data/final_dataset.json"
df = pd.read_json(file)
# data_csv = df.to_csv(data)

file_codes = "preprocessing/georef-belgium-postal-codes.json"

print(df[df["PostalCode"].apply(lambda x: x < 1000 or x > 10000)]["Url"])