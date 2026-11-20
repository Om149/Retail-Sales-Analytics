import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/cleaned_sales.csv")

category_sales = df.groupby(
    "Category"
)["Revenue"].sum().sort_values(ascending=False)

monthly_sales = df.groupby(
    ["Year", "Month"]
)["Revenue"].sum()

top_products = df.groupby(
    "ProductName"
)["Revenue"].sum().sort_values(
    ascending=False
).head(10)

region_sales = df.groupby(
    "Region"
).agg({
    "Revenue": "sum",
    "Profit": "sum",
    "OrderID": "nunique"
})

print(region_sales)
payment_analysis = df.groupby(
    "PaymentMode"
)["Revenue"].sum().sort_values(ascending=False)

print(payment_analysis)