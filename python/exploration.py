
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ----------------------------------
# 1. Load the cleaned dataset
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_sales.csv"
CHART_DIR = BASE_DIR / "reports" / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

# Convert date column
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

print("\n========== DATA OVERVIEW ==========")

print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())


# ----------------------------------
# 2. Basic Business Metrics
# ----------------------------------

print("\n========== BUSINESS METRICS ==========")

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_orders = df["OrderID"].nunique()
total_customers = df["CustomerID"].nunique()
total_quantity = df["Quantity"].sum()

print("Total Revenue: ₹", round(total_revenue, 2))
print("Total Profit: ₹", round(total_profit, 2))
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Total Quantity Sold:", total_quantity)


# ----------------------------------
# 3. Category-wise Sales Analysis
# ----------------------------------

category_sales = df.groupby("Category")["Revenue"].sum().sort_values(
    ascending=False
)

print("\n========== CATEGORY-WISE REVENUE ==========")
print(category_sales)

category_sales.to_csv(
    BASE_DIR / "reports" / "category_sales.csv"
)

plt.figure(figsize=(10, 6))
category_sales.plot(kind="bar")

plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(CHART_DIR / "category_revenue.png")
plt.show()


# ----------------------------------
# 4. Monthly Revenue Analysis
# ----------------------------------

df["MonthYear"] = df["OrderDate"].dt.to_period("M").astype(str)

monthly_revenue = df.groupby("MonthYear")["Revenue"].sum()

print("\n========== MONTHLY REVENUE ==========")
print(monthly_revenue)

monthly_revenue.to_csv(
    BASE_DIR / "reports" / "monthly_revenue.csv"
)

plt.figure(figsize=(14, 6))
monthly_revenue.plot(kind="line", marker="o")

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig(CHART_DIR / "monthly_revenue.png")
plt.show()


# ----------------------------------
# 5. Region-wise Sales Analysis
# ----------------------------------

region_sales = df.groupby("Region")["Revenue"].sum().sort_values(
    ascending=False
)

print("\n========== REGION-WISE REVENUE ==========")
print(region_sales)

plt.figure(figsize=(9, 5))
region_sales.plot(kind="bar")

plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(CHART_DIR / "region_revenue.png")
plt.show()


# ----------------------------------
# 6. Top 10 Products
# ----------------------------------

top_products = (
    df.groupby("ProductName")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS ==========")
print(top_products)

plt.figure(figsize=(11, 6))
top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (₹)")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig(CHART_DIR / "top_10_products.png")
plt.show()


# ----------------------------------
# 7. Payment Mode Analysis
# ----------------------------------

payment_sales = df.groupby("PaymentMode")["Revenue"].sum().sort_values(
    ascending=False
)

print("\n========== PAYMENT MODE ANALYSIS ==========")
print(payment_sales)

plt.figure(figsize=(8, 6))
payment_sales.plot(kind="pie", autopct="%1.1f%%")

plt.title("Revenue by Payment Mode")
plt.ylabel("")
plt.tight_layout()

plt.savefig(CHART_DIR / "payment_mode.png")
plt.show()


# ----------------------------------
# 8. Profit Analysis
# ----------------------------------

profit_by_category = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== PROFIT BY CATEGORY ==========")
print(profit_by_category)

plt.figure(figsize=(10, 6))
profit_by_category.plot(kind="bar")

plt.title("Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(CHART_DIR / "category_profit.png")
plt.show()


# ----------------------------------
# 9. Sales Channel Analysis
# ----------------------------------

channel_sales = df.groupby("SalesChannel")["Revenue"].sum().sort_values(
    ascending=False
)

print("\n========== SALES CHANNEL ANALYSIS ==========")
print(channel_sales)

plt.figure(figsize=(9, 5))
channel_sales.plot(kind="bar")

plt.title("Revenue by Sales Channel")
plt.xlabel("Sales Channel")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(CHART_DIR / "sales_channel.png")
plt.show()


# ----------------------------------
# 10. Statistical Analysis
# ----------------------------------

print("\n========== STATISTICAL SUMMARY ==========")

print(df[[
    "Quantity",
    "UnitPrice",
    "Revenue",
    "Profit"
]].describe())

print("\n========== CORRELATION ==========")

print(df[[
    "Quantity",
    "UnitPrice",
    "Revenue",
    "Profit"
]].corr())

plt.figure(figsize=(8, 6))

sns.heatmap(
    df[["Quantity", "UnitPrice", "Revenue", "Profit"]].corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Sales Data Correlation")
plt.tight_layout()

plt.savefig(CHART_DIR / "correlation_heatmap.png")
plt.show()


# ----------------------------------
# 11. Save Final EDA Summary
# ----------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Profit",
        "Total Orders",
        "Total Customers",
        "Total Quantity Sold"
    ],
    "Value": [
        total_revenue,
        total_profit,
        total_orders,
        total_customers,
        total_quantity
    ]
})

print("\nEDA ANALYSIS COMPLETED SUCCESSFULLY!")
print("Charts saved in:", CHART_DIR)
print("Reports saved in:", BASE_DIR / "reports")
