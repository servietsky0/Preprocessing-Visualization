import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
file = "/home/siegfried2021/Bureau/BeCode_AI/Projets/ImmoEliza/Preprocessing-Visualization/data/final_dataset.json"
df = pd.read_json(file)
# data_csv = df.to_csv(data)

# # importing json with postcodes, and reducing the postcode df to the postcode column
# file_postcodes = "preprocessing/georef-belgium-postal-codes.json"
# df_postcodes = pd.read_json(file_postcodes)
# df_postcodes = df_postcodes[["postcode"]]

# # merging properties dataset with postcode df and drop duplicated values
# df = df.merge(df_postcodes, how="inner", right_on="postcode", left_on="PostalCode").drop_duplicates()
# del df["postcode"]

# # filling null values for SwimmingPool by False, since no mention of swimming pool is interpreted as absence of swimming pool
# df["SwimmingPool"] = df["SwimmingPool"].fillna(False)

# # suggestion to delete the openfire column, because of the absence of True values
# del df["Openfire"]

df = df[['TypeOfProperty', 'PostalCode', 'SubtypeOfProperty',
       'Price', 'Kitchen', 'StateOfBuilding', 'Heating', 'Bedrooms', 'LivingArea', 'NumberOfFacades']]

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import IterativeImputer

# Identify numerical and categorical columns
numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
categorical_cols = df.select_dtypes(include=['object']).columns

# Create a ColumnTransformer to handle the different types of data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse=False), categorical_cols)
    ])

# Create a pipeline that first transforms the data and then applies the iterative imputer
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('imputer', IterativeImputer())
])

# Fit and transform the data
df_imputed = pipeline.fit_transform(df)

# Convert the result back to a DataFrame
df_imputed = pd.DataFrame(df_imputed, columns=pipeline.named_steps['preprocessor'].get_feature_names_out())
print("\nDataFrame after MICE imputation and one-hot encoding:")
print(df_imputed)

# Inverse transform the one-hot encoded columns back to the original categorical values
def inverse_transform(encoded_df, original_df, categorical_cols):
    for col in categorical_cols:
        # Get the one-hot encoded columns for this categorical column
        one_hot_cols = [c for c in encoded_df.columns if col in c]
        # Find the column with the maximum value (1) to get the original category
        original_df[col] = encoded_df[one_hot_cols].idxmax(axis=1).apply(lambda x: x.split('_')[-1])
        # Drop the one-hot encoded columns from the original DataFrame
        original_df = original_df.drop(columns=one_hot_cols)
    return original_df

# Apply inverse transformation
df_restored = inverse_transform(df_imputed, df.copy(), categorical_cols)
print("\nDataFrame after reversing one-hot encoding:")
print(df_restored)