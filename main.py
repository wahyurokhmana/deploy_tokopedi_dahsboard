import streamlit as st
import pandas as pd
import altair as alt
# from numerize import numerize

st.set_page_config(layout='wide')

df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQMqC_6fkaH6oZweJDIIYFDdE9o3P3G1hB0OKLzkGGf0pB-FjWJoAMoYca2iXV2ID5dE7hoklCSx6hE/pub?gid=0&single=true&output=csv')

df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

df['order_year'] = df['order_date'].dt.year

CURR_YEAR = max(df['order_date'].dt.year)
PREV_YEAR = CURR_YEAR - 1

st.title("Tokopedi Dashboard")

# st.write(CURR_YEAR)

# 1 periksa tahun terakhir dari data
# itung total sales, banyaknya order, banyaknya kosumen, profit %
# di tahun tersebut

data = pd.pivot_table(
    data=df,
    index='order_year',
    aggfunc={
        'sales':'sum',
        'profit':'sum',
        'order_id':pd.Series.nunique,
        'customer_id':pd.Series.nunique
    }
).reset_index()

data['profit_pct'] = 100.0 * data['profit'] / data['sales']

# st.dataframe(data)

# helper function
def format_big_number(num):
    if num >= 1e6:
        return f"{num / 1e6:.2f} Mio"
    elif num >= 1e3:
        return f"{num / 1e3:.2f} K"
    else:
        return f"{num:.2f}"

mx_sales, mx_order, mx_customer, mx_profit_pct = st.columns(4)

with mx_sales:
    curr_sales = data.loc[data['order_year']==CURR_YEAR, 'sales'].values[0]
    prev_sales = data.loc[data['order_year']==PREV_YEAR, 'sales'].values[0]
    
    sales_diff_pct = 100.0 * (curr_sales - prev_sales) / prev_sales

    st.metric("Sales", value=format_big_number(curr_sales), delta=f'{sales_diff_pct:.2f}%')

with mx_order:
     curr_order = data.loc[data['order_year']==CURR_YEAR, 'order_id'].values[0]
     prev_order = data.loc[data['order_year']==PREV_YEAR, 'order_id'].values[0]

     order_diff_pct = 100.0 * (curr_order - prev_order) / prev_order

     st.metric("Order", format_big_number(curr_order), delta=f'{order_diff_pct:.2f}%')

with mx_customer:
    curr_customer = data.loc[data['order_year']==CURR_YEAR, 'customer_id'].values[0]
    prev_customer = data.loc[data['order_year']==PREV_YEAR, 'customer_id'].values[0]
    
    customer_diff_pct = 100.0 * (curr_customer - prev_customer) / prev_customer
    st.metric("customer_id", value=curr_customer, delta=f'{customer_diff_pct:.2f}%')

with mx_profit_pct:
    curr_profit_pct = data.loc[data['order_year']==CURR_YEAR, 'profit_pct'].values[0]
    prev_profit_pct = data.loc[data['order_year']==PREV_YEAR, 'profit_pct'].values[0]
    
    profit_pct_diff_pct = 100.0 * (curr_profit_pct - prev_profit_pct) / prev_profit_pct
    st.metric("customer_id", value=f'{curr_profit_pct:.2f}%', delta=f'{profit_pct_diff_pct:.2f}%')

st.header("Sales trend")
freq = st.selectbox("Freq", ['Harian','Bulanan'])
st.write(freq)

timeUnit = {
    'Harian':'yearmonthdate',
    'Bulanan':'yearmonth'
}

# altair membuat object berupa chart dengan data di dalam parameter
sales_line = alt.Chart(df[df['order_year']==CURR_YEAR]).mark_line().encode(
    alt.X('order_date', title='Order Date', timeUnit=timeUnit[freq]),
    alt.Y('sales', title='Sales', aggregate='sum')
)

st.altair_chart(sales_line,use_container_width=True)

# Barchart
st.header("Category per Segment Performance")

bar_chart = alt.Chart(df[df['order_year']==CURR_YEAR]).mark_bar().encode(
    column="category:N",
    y="sum(sales):Q",
    color="segment:N",
    x="segment:N"
).properties(width=350, height= 160)

st.altair_chart(bar_chart)

# scatter plot
st.header("Sales vs Profit Correlation")

_, midcol, _ = st.columns([1,2,3])

with midcol:
    scatter = alt.Chart(df[df['order_year']==CURR_YEAR]).mark_bar().encode(
        x="sales:Q",
        y="profit:Q",
        color="region:N"
    )
    st.altair_chart(scatter, use_container_width=True)

# # Bikin 4 kolom berisi sales dari tiap kategori
# # Setiap kolom mewakili region yang berbeda

# st.altair_chart(sales_bar,use_container_width=True)

# st.dataframe(df)

# st.dataframe(data, use_container_width=True)