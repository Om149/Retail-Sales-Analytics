import pandas as pd
import numpy as np

sales = pd.read_csv("data/raw/sales_raw.csv")
customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")

sales = sales.drop_duplicates()

sales["CustomerID"] = (
    sales["CustomerID"]
    .fillna("Unknown")
    .str.strip()
    .str.title()
)

sales["OrderDate"] = (
    sales["OrderDate"]
    .fillna("Unknown")
    .str.strip()
    .str.title()
)

sales["PaymentMode"] = (
    sales["PaymentMode"]
    .fillna("Unknown")
    .str.strip()
    .str.title()
)
sales["OrderDate"] = pd.to_datetime(
    sales["OrderDate"], errors="coerce"
)

sales["ShipDate"] = pd.to_datetime(
    sales["ShipDate"], errors="coerce"
)

sales["Quantity"] = pd.to_numeric(
    sales["Quantity"], errors="coerce"
)
df = sales.merge(
    customers,
    on="CustomerID",
    how="left"
)

df = df.merge(
    products,
    on="ProductID",
    how="left"
)
df["GrossSales"] = df["Quantity"] * df["UnitPrice"]

df["DiscountAmount"] = (
    df["GrossSales"] * df["DiscountPct"]
)

df["Revenue"] = (
    df["GrossSales"] - df["DiscountAmount"]
)

df["TotalCost"] = df["Quantity"] * df["UnitCost"]

df["Profit"] = df["Revenue"] - df["TotalCost"]

df["ProfitMargin"] = np.where(
    df["Revenue"] != 0,
    df["Profit"] / df["Revenue"] * 100,
    0
)

df["Month"] = df["OrderDate"].dt.month
df["Year"] = df["OrderDate"].dt.year
print(products.isnull().sum())