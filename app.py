import pandas as pd
import streamlit as st
import plotly.express as px 
st.set_page_config(
    page_title="OLA Ride Analytics",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/ola_data.csv")
    df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")
    return df

df = load_data()

st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
h1, h2, h3, h4 {
    color: #e5e7eb;
    font-weight: 600;
}
.metric-card {
    background: #020617;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.65);
}
section[data-testid="stSidebar"] {
    background: #020617;
}
span[data-baseweb="tag"] {
    background-color: #16a34a !important;
    color: white !important;
    border-radius: 10px;
}
button[data-baseweb="tab"][aria-selected="true"] {
    border-bottom: 2px solid #16a34a;
}
header, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## Filters")

booking_status = st.sidebar.multiselect(
    "Booking Status",
    df["Booking_Status"].unique(),
    df["Booking_Status"].unique()
)

vehicle_type = st.sidebar.multiselect(
    "Vehicle Type",
    df["Vehicle_Type"].unique(),
    df["Vehicle_Type"].unique()
)

payment_method = st.sidebar.multiselect(
    "Payment Method",
    df["Payment_Method"].unique(),
    df["Payment_Method"].unique()
)

filtered_df = df.copy()

if booking_status:
    filtered_df = filtered_df[filtered_df["Booking_Status"].isin(booking_status)]
if vehicle_type:
    filtered_df = filtered_df[filtered_df["Vehicle_Type"].isin(vehicle_type)]
if payment_method:
    filtered_df = filtered_df[filtered_df["Payment_Method"].isin(payment_method)]

total_rides = len(filtered_df)
success_rate = (
    len(filtered_df[filtered_df["Booking_Status"] == "Success"]) / total_rides * 100
    if total_rides else 0
)
cancellation_rate = 100 - success_rate if total_rides else 0

st.markdown("""
<h1>OLA Rides Analytics Dashboard</h1>
<p style="color:#9ca3af;">High-level overview of ride performance</p>
<hr style="border:0.5px solid rgba(255,255,255,0.1);">
""", unsafe_allow_html=True)

tabs = st.tabs([
    "Overall",
    "Vehicle Type",
    "Payment Method",
    "Cancellation",
    "Ratings"
])

with tabs[0]:
    st.markdown("""
<h2 style="margin-bottom:6px;">Overall Performance Overview</h2>
<p style="color:#9ca3af; font-size:14px;">
Summary of total rides, success rate and cancellations
</p>
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    c1.markdown(
        f"<div class='metric-card'><h4>Total Rides</h4><h2>{total_rides:,}</h2></div>",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"<div class='metric-card'><h4>Success Rate</h4><h2>{success_rate:.1f}%</h2></div>",
        unsafe_allow_html=True
    )
    c3.markdown(
        f"<div class='metric-card'><h4>Cancellation Rate</h4><h2>{cancellation_rate:.1f}%</h2></div>",
        unsafe_allow_html=True
    )

    st.info("Filters selected from sidebar apply to all pages.")

    status_df = filtered_df["Booking_Status"].value_counts().reset_index()
    status_df.columns = ["Booking Status", "Count"]

    fig = px.bar(
        status_df,
        x="Booking Status",
        y="Count",
        color="Booking Status",
        text_auto=True,
        title="Booking Status Distribution"
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Key Insights")
    st.markdown("""
- Majority of rides are successfully completed.
- Cancellation rate indicates scope for operational improvements.
- Driver-related cancellations form a significant share.
    """)

with tabs[1]:
    st.markdown("## Rides by Vehicle Type")

    vehicle_df = filtered_df["Vehicle_Type"].value_counts().reset_index()
    vehicle_df.columns = ["Vehicle Type", "Total Rides"]

    fig = px.bar(
        vehicle_df,
        x="Vehicle Type",
        y="Total Rides",
        color="Vehicle Type",
        text_auto=True,
    )
    fig.update_layout(template="plotly_dark", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Key Insights")
    st.markdown("""
- Prime Sedan and eBike show the highest ride volumes.
- Demand is balanced across vehicle types.
- Fleet planning should prioritize high-demand categories.
    """)

with tabs[2]:
    st.markdown("## Rides by Payment Method")

    payment_df = filtered_df["Payment_Method"].value_counts().reset_index()
    payment_df.columns = ["Payment Method", "Total Rides"]

    fig = px.bar(
        payment_df,
        x="Payment Method",
        y="Total Rides",
        color="Payment Method",
        text_auto=True,
    )
    fig.update_layout(template="plotly_dark", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Key Insights")
    st.markdown("""
- Cash and UPI dominate as preferred payment methods.
- Digital payments show strong adoption.
- Card usage has scope for promotional growth.
    """)

with tabs[3]:
    st.markdown("## Cancellation Breakdown")

    cancel_df = filtered_df[filtered_df["Booking_Status"] != "Success"]
    cancel_df = cancel_df["Booking_Status"].value_counts().reset_index()
    cancel_df.columns = ["Cancellation Reason", "Count"]

    fig = px.bar(
        cancel_df,
        x="Cancellation Reason",
        y="Count",
        color="Cancellation Reason",
        text_auto=True,
    )
    fig.update_layout(template="plotly_dark", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Key Insights")
    st.markdown("""
- Driver-side cancellations are most common.
- Customer cancellations are comparatively lower.
- Improving driver allocation can reduce cancellations.
    """)

with tabs[4]:
    st.markdown("## Ratings Analysis")

    if "Customer_Rating" in filtered_df.columns:

        rating_df = (
            filtered_df["Customer_Rating"]
            .dropna()
            .value_counts()
            .sort_index()
            .reset_index()
        )

        rating_df.columns = ["Customer Rating", "Count"]

        fig_rating = px.bar(
            rating_df,
            x="Customer Rating",
            y="Count",
            text_auto=True
        )

        fig_rating.update_layout(
            template="plotly_dark",
            height=420,
            showlegend=False
        )

        st.plotly_chart(fig_rating, use_container_width=True)

        st.markdown("### Key Insights")
        st.markdown("""
- Majority of customers rate between 4 and 5.
- Low ratings are minimal.
- Maintaining service quality is essential.
        """)

    else:
        st.warning("Customer_Rating column not found in dataset")

st.markdown("---")
st.caption("OLA Ride Analytics | Streamlit Dashboard")