import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚕",
    layout="wide"
)

st.title("🚕 OLA Ride Insights Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("G:\My Drive\Innovexis-Data-Analyst-Task\OLA_Ride-Analysis-Task2\ola_data.csv.csv")
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    return df

df = load_data()

st.sidebar.header("Filters")

vehicle_type = st.sidebar.multiselect(
    "Select Vehicle Type",
    options=df["Vehicle_Type"].unique(),
    default=df["Vehicle_Type"].unique()
)

payment_method = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["Payment_Method"].unique(),
    default=df["Payment_Method"].unique()
)

filtered_df = df[
    (df["Vehicle_Type"].isin(vehicle_type)) &
    (df["Payment_Method"].isin(payment_method))
]

col1, col2, col3 = st.columns(3)

total_rides = len(filtered_df)
total_revenue = filtered_df["Booking_Value"].sum()
cancelled_rides = len(filtered_df[filtered_df["Booking_Status"] == "Cancelled"])

col1.metric("Total Rides", total_rides)
col2.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
col3.metric("Cancelled Rides", cancelled_rides)

st.divider()

if "Date" in filtered_df.columns:
    ride_trend = filtered_df.groupby("Date").size().reset_index(name="Ride_Count")
    fig1 = px.line(ride_trend, x="Date", y="Ride_Count", title="Ride Volume Over Time")
    st.plotly_chart(fig1, use_container_width=True)

status_count = filtered_df["Booking_Status"].value_counts().reset_index()
status_count.columns = ["Booking_Status", "Count"]

fig2 = px.pie(status_count, names="Booking_Status", values="Count", title="Booking Status Breakdown")
st.plotly_chart(fig2, use_container_width=True)

revenue_payment = filtered_df.groupby("Payment_Method")["Booking_Value"].sum().reset_index()
fig3 = px.bar(revenue_payment, x="Payment_Method", y="Booking_Value", title="Revenue by Payment Method")
st.plotly_chart(fig3, use_container_width=True)

if "Driver_Rating" in filtered_df.columns:
    fig4 = px.histogram(filtered_df, x="Driver_Rating", nbins=10, title="Driver Ratings Distribution")
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("SQL Based Insights")

top_customers = (
    filtered_df.groupby("Customer_ID")["Booking_Value"]
    .sum()
    .reset_index()
    .sort_values(by="Booking_Value", ascending=False)
    .head(5)
)

st.dataframe(top_customers)

st.subheader("Power BI Dashboard")

powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiOTg2M2MxYTMtYWM4ZC00MDMzLWJiZTgtMzE5MDRlMWJhMTgyIiwidCI6ImJiYzIxNzVlLTUyZDEtNGVkNi1iYzNhLTNhYzQ3OWY1ODM5ZCIsImMiOjEwfQ%3D%3D"

components.iframe(powerbi_url, height=650)