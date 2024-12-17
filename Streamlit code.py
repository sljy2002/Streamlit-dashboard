#!/usr/bin/env python
# coding: utf-8

# In[1]:


streamlit_code ='''
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Function to fetch data from SQLite database
def get_data(query):
    with sqlite3.connect("retail_data.db") as conn:
        return pd.read_sql_query(query, conn)

# Streamlit Setup (in Jupyter, use st.set_page_config() for layout setup)
st.set_page_config(page_title="Retail Dashboard", layout="wide")

# Load data
st.sidebar.header("Data Selection")
data_type = st.sidebar.radio("Select Data Type:", ("Sales", "Customers", "Products"))

if data_type == "Sales":
    data = get_data("SELECT * FROM Sales")
elif data_type == "Customers":
    data = get_data("SELECT * FROM Customers")
else:
    data = get_data("SELECT * FROM Products")

# Display Data
st.title(f"{data_type} Dashboard")
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader(f"{data_type} Data")
    st.dataframe(data)

# Check the columns to avoid KeyError
st.write("Columns in the data:", data.columns)

# Basic Analysis
st.sidebar.header("Analysis Options")
analyze = st.sidebar.checkbox("Perform Analysis")

if analyze:
    if data_type == "Sales":
        st.subheader("Sales Analysis")
        total_sales = data['TotalSales'].sum()
        avg_sales = data['TotalSales'].mean()
        st.metric("Total Sales", f"${total_sales:,.2f}")
        st.metric("Average Sales", f"${avg_sales:,.2f}")

        # Sales by InvoiceDate (instead of Date or OrderDate)
        if 'InvoiceDate' in data.columns:
            data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
            daily_sales = data.groupby(data['InvoiceDate'].dt.date)['TotalSales'].sum().reset_index()
            fig = px.line(daily_sales, x='InvoiceDate', y='TotalSales', title="Daily Sales Trend")
            st.plotly_chart(fig)
        else:
            st.warning("InvoiceDate column is not available in the Sales data.")

    elif data_type == "Customers":
        st.subheader("Customer Distribution by Country")

        # Group by 'Country' and count the number of unique 'CustomerID' for each country
        customer_distribution = data.groupby('Country')['CustomerID'].nunique().reset_index()
        customer_distribution.columns = ['Country', 'CustomerCount']

        # Plot the distribution
        fig = px.bar(customer_distribution, x='Country', y='CustomerCount', title="Number of Customers by Country")
        st.plotly_chart(fig)

    elif data_type == "Products":
        st.subheader("Product Analysis")
        # Assuming you want to calculate total sales by ProductID using the 'Sales' data
        sales_data = get_data("SELECT * FROM Sales")  # Assuming Sales data has ProductID and Quantity
        product_sales = sales_data.groupby('ProductID').agg({'TotalSales': 'sum'}).reset_index()
        product_sales = product_sales.sort_values(by='TotalSales', ascending=False).head(10)

        # Merge with Products data for ProductName
        products = get_data("SELECT * FROM Products")
        product_sales = pd.merge(product_sales, products[['ProductID', 'ProductName']], on='ProductID', how='left')

        fig = px.bar(product_sales, x='ProductName', y='TotalSales', title="Top 10 Most Sold Products")
        st.plotly_chart(fig, key="top_products")

# Advanced Visualizations
st.sidebar.header("Visualization Options")
visualize = st.sidebar.checkbox("Enable Visualizations")

if visualize:
    st.subheader("Custom Visualizations")
    if data_type == "Sales":
        st.markdown("*Sales Distribution by Product*")
        product_sales = data.groupby('ProductID')['TotalSales'].sum().reset_index()
        fig = px.pie(product_sales, values='TotalSales', names='ProductID', title="Sales by Product")
        st.plotly_chart(fig)

    elif data_type == "Customers":
        st.markdown("**Customer Distribution by Country (Pie Chart)**")

    # Group by 'Country' and count the number of unique 'CustomerID' for each country
        customer_distribution = data.groupby('Country')['CustomerID'].nunique().reset_index()
        customer_distribution.columns = ['Country', 'CustomerCount']

    # Plot the pie chart
        fig = px.pie(
            customer_distribution,
            names='Country',
            values='CustomerCount',
            title="Customer Distribution by Country",
            labels={'Country': 'Country', 'CustomerCount': 'Number of Customers'},
            hole=0.4  # Optional: Creates a donut chart effect
        )

    # Customize appearance
        fig.update_traces(textinfo='percent+label', textfont_size=14)
        fig.update_layout(
            title_font_size=20,
            showlegend=True
        )

    # Display the pie chart in Streamlit
        st.plotly_chart(fig, key="customer_distribution_piechart")



    elif data_type == "Products":
        st.markdown("*Product Sales Distribution*")
        fig = plt.figure(figsize=(10, 4))
        sns.boxplot(x=data['Price'])
        st.pyplot(fig)

st.sidebar.info("Use the options above to customize your dashboard.")'''
with open("dashboard.py", "w") as file:
    file.write(streamlit_code)
print("Streamlit code has been saved to 'dashboard.py'")


# In[ ]:




