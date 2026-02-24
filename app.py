import streamlit as st
import pandas as pd
import mysql.connector
st.set_page_config(page_title="OLA Ride Insights", layout="wide")
st.title("OLA Ride Insights Dashboard")
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SamyakKumar@200418",
        database="Innovexis_Task_2"
    )
conn = get_connection()
@st.cache_data
def load_data(query):
    return pd.read_sql(query, conn)
st.sidebar.header("Filters")
vehicle_type = st.sidebar.selectbox(
    "Select Vehicle Type",
    ["All", "Mini", "Micro", "Prime Sedan", "Auto"]
)
payment_method = st.sidebar.selectbox(
    "Select Payment Method",
    ["All", "Cash", "UPI", "Card"]
)
query = "SELECT * FROM bookings WHERE 1=1"
if vehicle_type != "All":
    query += f" AND vehicle_type = '{vehicle_type}'"
if payment_method != "All":
    query += f" AND payment_method = '{payment_method}'"
data = load_data(query)
col1, col2, col3 = st.columns(3)
col1.metric("Total Rides", len(data))
col2.metric("Total Revenue", f"₹ {data['booking_value'].sum():,.2f}")
col3.metric("Average Rating", round(data['customer_rating'].mean(), 2))
st.divider()
st.subheader("Filtered Ride Data")
st.dataframe(data)
st.subheader("SQL Insights")

if st.button("Show Successful Bookings"):
    success_query = "SELECT * FROM bookings WHERE booking_status='Success'"
    success_data = load_data(success_query)
    st.write(success_data)
if st.button("Average Ride Distance by Vehicle"):
    avg_query = """
    SELECT vehicle_type, AVG(ride_distance) as avg_distance
    FROM bookings
    GROUP BY vehicle_type
    """
    avg_data = load_data(avg_query)
    st.write(avg_data)
st.subheader("📊 Power BI Dashboard")
powerbi_url = "PASTE_YOUR_POWER_BI_EMBED_LINK"
st.components.v1.iframe(powerbi_url, height=600)