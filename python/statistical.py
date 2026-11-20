import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/cleaned_sales.csv")

print("Mean:", df["Revenue"].mean())
print("Median:", df["Revenue"].median())
print("Standard Deviation:", df["Revenue"].std())

Q1 = df["Revenue"].quantile(0.25)
Q3 = df["Revenue"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[
    (df["Revenue"] < lower) |
    (df["Revenue"] > upper)
]

print("Outliers:", len(outliers))