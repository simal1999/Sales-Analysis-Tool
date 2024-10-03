# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

# Title of the app
st.title("E-Commerce Sales Analysis Tool")

# Instructions for the user
st.markdown("""
**Instructions**:
- Upload an e-commerce dataset in CSV format.
- The dataset should contain columns 'Date', 'Amount', 'Status', and 'Category'.
- If your dataset doesnt contain above columns please add them and try.
- If your data set has above columns but with different names then please rename the columns as above and try  
""")

# File uploader for dataset
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the dataset
    data = pd.read_csv(uploaded_file)

    # Step 1: Data Cleaning
    # Parse dates and drop rows with missing Amount
    data['Date'] = pd.to_datetime(data['Date'], format='%m-%d-%y', errors='coerce')

    # Ensure 'Amount' is numeric and drop rows with missing Amount
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
    clean_data = data.dropna(subset=['Amount'])
    sales_trend = clean_data.groupby(clean_data['Date'].dt.to_period('M'))['Amount'].sum()

    # Convert month to month name
    sales_trend.index = sales_trend.index.strftime('%B')

    # Plotting Sales Trend Over Time using matplotlib
    plt.figure(figsize=(10, 6))
    sales_trend.plot(kind='line', color='b', marker='o')
    plt.title('Sales Trend Over Time')
    plt.xlabel('Month')
    plt.ylabel('Total Sales (INR)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)
    
    #Insights and interpretations for Sales Trends Over Time.
    st.markdown(f"""### Insights  and Interpretations for Sales Trends Over Time.
                The sales trend graph shows how sales fluctuate over different months.
    This can be used to spot high and low sale periods.
    1. The lowest sales were recorded in {sales_trend.idxmin()}.
    2. The max sales were recorded in {sales_trend.idxmax()}.
    3. The average sales is {sales_trend.mean()}""")

    # Step 3: Analyze Order Status Distribution
    # Get the count of each order status and convert to DataFrame
    status_distribution = clean_data['Status'].value_counts().reset_index()
    status_distribution.columns = ['Status', 'count']  # Rename columns for clarity

    # Plotting Order Status Distribution using matplotlib
    plt.figure(figsize=(15, 10))
    status_distribution.set_index('Status')['count'].plot(kind='bar', color='orange')
    plt.title('Order Status Distribution')
    plt.xlabel('Order Status')
    plt.ylabel('Number of Orders')
    plt.xticks(rotation=25)
    plt.tight_layout()
    st.pyplot(plt)
    
    #Insights and interpretations for Order Status Distribution
    
    st.markdown(f"""### Insights and Interpretations for Order Status Distribution
    Total orders:{status_distribution['count'].sum()}
    Most common order status:{status_distribution.loc[status_distribution['count'].idxmax()]['Status']}
    Least common order status: {status_distribution.loc[status_distribution['count'].idxmin()]['Status']}""")
    
    # Step 4: Analyze Top-Selling Product Categories
    # Group by category to get total sales for each category
    top_categories = clean_data.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(10)

    # Plotting Top-Selling Categories using matplotlib
    plt.figure(figsize=(10, 6))
    top_categories.plot(kind='bar', color='green')
    plt.title('Top 10 Best-Selling Categories')
    plt.xlabel('Category')
    plt.ylabel('Total Sales (INR)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)
    
    #Insights and interpretations for Top-Selling Product Categories
    
    st.markdown(f"""### Insights and Interpretations for Top Selling Product Categories

* **Top selling category:** **{top_categories.index[0]}** (**{top_categories.values[0]}** INR)
* **Second best selling category:** **{top_categories.index[1]}** (**{top_categories.values[1]}** INR)
* **Third best selling category:** **{top_categories.index[2]}** (**{top_categories.values[2]}** INR)
* **Total sales for top 10 categories:** **{top_categories.sum()}** INR
* **Average sales for top 10 categories:** **{top_categories.mean()}** INR
* **Category with lowest sales in top 10:** **{top_categories.index[-1]}** (**{top_categories.values[-1]}** INR)
""")

    # Step 5: Create Interactive Visualizations using Plotly.
    # Interactive Sales Trend Over Time
    sales_trend_df = sales_trend.reset_index()
    sales_trend_df['Date'] = sales_trend_df['Date'].astype(str)
    fig_sales_trend = px.line(sales_trend_df, x='Date', y='Amount', title='Interactive Sales Trend Over Time',
                              labels={'Amount': 'Total Sales (INR)', 'Date': 'Month'}, markers=True)
    st.plotly_chart(fig_sales_trend)
    
    #Insights and interpretations for Sales Trends Over Time.
    st.markdown(f"""### Insights and Interpretations for Sales Trends Over Time.
                The sales trend graph shows how sales fluctuate over different months.
    This can be used to spot high and low sale periods.
    1. The lowest sales were recorded in {sales_trend.idxmin()}.
    2. The max sales were recorded in {sales_trend.idxmax()}.
    3. The average sales is {sales_trend.mean()}""")

    # Interactive Order Status Distribution
    fig_status_distribution = px.bar(status_distribution, x='Status', y='count',
                                     title='Interactive Order Status Distribution',
                                     labels={'Status': 'Order Status', 'count': 'Number of Orders'})
    st.plotly_chart(fig_status_distribution)
    
    #Insights and interpretations for Order Status Distribution
    
    st.markdown(f"""### Insights and Interpretations for Order Status Distribution
    Total orders:{status_distribution['count'].sum()}
    Most common order status:{status_distribution.loc[status_distribution['count'].idxmax()]['Status']}
    Least common order status: {status_distribution.loc[status_distribution['count'].idxmin()]['Status']}""")

    # Interactive Top Selling Categories
    fig_top_categories = px.bar(top_categories.reset_index(), x='Category', y='Amount',
                                title='Interactive Top 10 Best-Selling Categories',
                                labels={'Category': 'Category', 'Amount': 'Total Sales (INR)'})
    st.plotly_chart(fig_top_categories)

    #Insights and interpretations for Top Selling Product Categories
    
    st.markdown(f"""### Insights and Interpretations for Top Selling Product Categories

* **Top selling category:** **{top_categories.index[0]}** (**{top_categories.values[0]}** INR)
* **Second best selling category:** **{top_categories.index[1]}** (**{top_categories.values[1]}** INR)
* **Third best selling category:** **{top_categories.index[2]}** (**{top_categories.values[2]}** INR)
* **Total sales for top 10 categories:** **{top_categories.sum()}** INR
* **Average sales for top 10 categories:** **{top_categories.mean()}** INR
* **Category with lowest sales in top 10:** **{top_categories.index[-1]}** (**{top_categories.values[-1]}** INR)
""")