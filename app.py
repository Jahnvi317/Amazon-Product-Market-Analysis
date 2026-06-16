import streamlit as st
import pandas as pd
import plotly.express as px
# Load the cleaned dataset
df= pd.read_csv('amazon_cleaned.csv')
# dashboard setup
st.set_page_config(page_title="Amazon Sales Dashboard", layout="wide")
st.title("Amazon Product performance Dashboard")
#Sidebar for Category filter
selected_cat = st.sidebar.multiselect("Select Category", options=df['category'].unique())
#Filter Data Logic
if selected_cat:
    df_filter = df[df['category'].isin(selected_cat)]
else:
    df_filter = df

#KPI Section
col1, col2, col3 = st.columns(3)
col1.metric("Total Products",len(df_filter))
col2.metric("Average Rating",round(df_filter['rating'].mean(),2))
col3.metric("Average Discount%",f"{round(df_filter['discount_percentage'].mean(),1)}%")

#visual 1: Price vs Rating
st.subheader("Price vs Rating Analysis")
fig= px.scatter(df_filter, x="discounted_price", y="rating", color="category", hover_data=['product_name'],
                title="How Price Affects user Rating ")
fig.update_layout(legend=dict(orientation='h',yanchor='top',y=-0.5,xanchor='center',x=0.5),
                  margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig)

#visual 2 Top Categories
st.subheader("Top Categories by Count")
cat_count = df_filter['category'].value_counts().reset_index().head(10)
cat_count.columns = ['category', 'count']
fig2 = px.bar(cat_count, x='count', y='category',orientation='h',text_auto=True)
fig2.update_layout(yaxis=dict(autorange="reversed"),margin=dict(l=300, r=20, t=50, b=20),height=500)
fig2.update_traces(marker_color='#1f77b4')
st.plotly_chart(fig2, use_container_width=True)

#visual 3 Top rated products
st.subheader("Top Rated Products")
top_rated = df_filter[df_filter['rating']>=4.0].sort_values(by='rating', ascending=False).head(10)
#create a short name column for better display in the bar chart
top_rated['short_name'] = top_rated['product_name'].str[:30] + '...'
# Create a horizontal bar chart for top rated products
fig3 = px.bar(top_rated, x='rating', y='short_name',orientation='h')
fig3.update_layout(yaxis=dict(autorange="reversed"),margin=dict(l=200, r=20, t=30, b=20),height=400)
st.plotly_chart(fig3, use_container_width=True)

#Top 10 products by Rating and Discount
st.subheader("Top 10 Products by Rating and Discount")
top_products = df_filter.sort_values(by=['rating', 'discount_percentage'], ascending=[False, False]).head(10)
top_products['short_name'] = top_products['product_name'].str[:30] + '...'
st.dataframe(top_products[['short_name', 'rating', 'discount_percentage']])
