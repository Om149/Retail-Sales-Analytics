
import pandas as pd
import sqlite3
from pathlib import Path

# =====================================
# 1. LOAD CSV FILES
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

sales = pd.read_csv(BASE_DIR / "data/raw/sales_raw.csv")
customers = pd.read_csv(BASE_DIR / "data/raw/customers.csv")
products = pd.read_csv(BASE_DIR / "data/raw/products.csv")

# Create SQLite database
connection = sqlite3.connect(BASE_DIR / "retail_analytics.db")

# Import CSV data into SQL tables
sales.to_sql("sales", connection, if_exists="replace", index=False)
customers.to_sql("customers", connection, if_exists="replace", index=False)
products.to_sql("products", connection, if_exists="replace", index=False)

print("Database and tables created successfully!")


# =====================================
# 2. SQL FUNDAMENTALS
# =====================================

# Query 1: Display first 10 sales records
query1 = """
SELECT *
FROM sales
LIMIT 10;
"""

# Query 2: Total number of transactions
query2 = """
SELECT COUNT(DISTINCT OrderID) AS Total_Transactions
FROM sales;
"""

# Query 3: Total quantity sold
query3 = """
SELECT SUM(Quantity) AS Total_Quantity
FROM sales;
"""

# Query 4: Revenue by product
query4 = """
SELECT
    p.ProductName,
    SUM(s.Quantity * p.UnitPrice * (1 - s.DiscountPct)) AS Revenue
FROM sales s
JOIN products p
    ON s.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY Revenue DESC;
"""

# Query 5: Top 10 customers by revenue
query5 = """
SELECT
    c.CustomerName,
    SUM(s.Quantity * p.UnitPrice * (1 - s.DiscountPct)) AS Revenue
FROM sales s
JOIN customers c
    ON s.CustomerID = c.CustomerID
JOIN products p
    ON s.ProductID = p.ProductID
GROUP BY c.CustomerID, c.CustomerName
ORDER BY Revenue DESC
LIMIT 10;
"""

# Query 6: Average Order Value
query6 = """
SELECT AVG(OrderRevenue) AS Average_Order_Value
FROM (
    SELECT
        s.OrderID,
        SUM(s.Quantity * p.UnitPrice * (1 - s.DiscountPct)) AS OrderRevenue
    FROM sales s
    JOIN products p
        ON s.ProductID = p.ProductID
    GROUP BY s.OrderID
);
"""

# Query 7: Sales by category
query7 = """
SELECT
    p.Category,
    SUM(s.Quantity * p.UnitPrice * (1 - s.DiscountPct)) AS Revenue
FROM sales s
JOIN products p
    ON s.ProductID = p.ProductID
GROUP BY p.Category
ORDER BY Revenue DESC;
"""

# Query 8: Most popular payment method
query8 = """
SELECT
    PaymentMode,
    COUNT(DISTINCT OrderID) AS Total_Orders
FROM sales
GROUP BY PaymentMode
ORDER BY Total_Orders DESC;
"""

# Query 9: Sales by region
query9 = """
SELECT
    c.Region,
    SUM(s.Quantity * p.UnitPrice * (1 - s.DiscountPct)) AS Revenue
FROM sales s
JOIN customers c
    ON s.CustomerID = c.CustomerID
JOIN products p
    ON s.ProductID = p.ProductID
GROUP BY c.Region
ORDER BY Revenue DESC;
"""

# Query 10: Customers with more than 5 orders
query10 = """
SELECT
    c.CustomerName,
    COUNT(DISTINCT s.OrderID) AS Total_Orders
FROM sales s
JOIN customers c
    ON s.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.CustomerName
HAVING COUNT(DISTINCT s.OrderID) > 5;
"""


# =====================================
# 3. JOIN OPERATIONS
# =====================================

# INNER JOIN
inner_join = """
SELECT
    s.OrderID,
    c.CustomerName,
    p.ProductName
FROM sales s
INNER JOIN customers c
    ON s.CustomerID = c.CustomerID
INNER JOIN products p
    ON s.ProductID = p.ProductID;
"""

# LEFT JOIN
left_join = """
SELECT
    s.OrderID,
    c.CustomerName,
    p.ProductName,
    s.Quantity
FROM sales s
LEFT JOIN customers c
    ON s.CustomerID = c.CustomerID
LEFT JOIN products p
    ON s.ProductID = p.ProductID;
"""

# RIGHT JOIN equivalent using LEFT JOIN
right_join = """
SELECT
    c.CustomerName,
    s.OrderID
FROM customers c
LEFT JOIN sales s
    ON c.CustomerID = s.CustomerID;
"""

# SELF JOIN
self_join = """
SELECT
    c1.CustomerName AS Customer1,
    c2.CustomerName AS Customer2,
    c1.Region
FROM customers c1
JOIN customers c2
    ON c1.Region = c2.Region
    AND c1.CustomerID < c2.CustomerID;
"""


# =====================================
# 4. ADVANCED SQL - CTE
# =====================================

cte_query = """
WITH CategorySales AS (
    SELECT
        p.Category,
        SUM(s.Quantity * p.UnitPrice *
            (1 - s.DiscountPct)) AS Revenue
    FROM sales s
    JOIN products p
        ON s.ProductID = p.ProductID
    GROUP BY p.Category
)
SELECT *
FROM CategorySales
ORDER BY Revenue DESC;
"""


# =====================================
# 5. WINDOW FUNCTION - RANK PRODUCTS
# =====================================

rank_query = """
SELECT
    p.ProductName,
    SUM(s.Quantity * p.UnitPrice *
        (1 - s.DiscountPct)) AS Revenue,
    RANK() OVER (
        ORDER BY SUM(s.Quantity * p.UnitPrice *
        (1 - s.DiscountPct)) DESC
    ) AS ProductRank
FROM sales s
JOIN products p
    ON s.ProductID = p.ProductID
GROUP BY p.ProductID, p.ProductName;
"""


# =====================================
# 6. RUNNING TOTAL
# =====================================

running_total_query = """
WITH MonthlySales AS (
    SELECT
        strftime('%Y-%m', OrderDate) AS SalesMonth,
        SUM(s.Quantity * p.UnitPrice *
            (1 - s.DiscountPct)) AS Revenue
    FROM sales s
    JOIN products p
        ON s.ProductID = p.ProductID
    GROUP BY SalesMonth
)
SELECT
    SalesMonth,
    Revenue,
    SUM(Revenue) OVER (
        ORDER BY SalesMonth
    ) AS RunningRevenue
FROM MonthlySales
ORDER BY SalesMonth;
"""


# =====================================
# 7. EXECUTE ALL SQL QUERIES
# =====================================

queries = {
    "First 10 Sales Records": query1,
    "Total Transactions": query2,
    "Total Quantity Sold": query3,
    "Revenue by Product": query4,
    "Top 10 Customers": query5,
    "Average Order Value": query6,
    "Sales by Category": query7,
    "Popular Payment Method": query8,
    "Sales by Region": query9,
    "Customers with More Than 5 Orders": query10,
    "INNER JOIN": inner_join,
    "LEFT JOIN": left_join,
    "RIGHT JOIN Equivalent": right_join,
    "SELF JOIN": self_join,
    "CTE Category Sales": cte_query,
    "Product Ranking": rank_query,
    "Monthly Running Total": running_total_query
}

REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

for name, query in queries.items():

    print("\n====================================")
    print(name)
    print("====================================")

    try:
        result = pd.read_sql_query(query, connection)
        print(result.head(20))

        filename = name.lower().replace(" ", "_") + ".csv"
        result.to_csv(REPORT_DIR / filename, index=False)

    except Exception as error:
        print("Error:", error)


# =====================================
# 8. CLOSE DATABASE
# =====================================

connection.close()

print("\nPHASE 6 COMPLETED!")
print("SQL results saved in the reports folder.")
