import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("OLA_DataSet_final.csv")

# Clean columns
df.columns = df.columns.str.strip()

# Convert Date
df['Date'] = pd.to_datetime(df['Date'])

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚖 Filters")

vehicle = st.sidebar.multiselect(
    "Vehicle Type",
    options=df['Vehicle_Type'].dropna().unique(),
    default=df['Vehicle_Type'].dropna().unique()
)

payment = st.sidebar.multiselect(
    "Payment Method",
    options=df['Payment_Method'].dropna().unique(),
    default=df['Payment_Method'].dropna().unique()
)

# Apply filters
df = df[
    (df['Vehicle_Type'].isin(vehicle)) &
    (df['Payment_Method'].isin(payment))
]

# ---------------- KPIs ----------------
total_rides = df['Booking_ID'].count()
total_revenue = df['Booking_Value'].sum()
success_rate = (df['Booking_Status'] == 'Success').mean()
cancel_rate = (df['Booking_Status'] != 'Success').mean()
avg_rating = df['Customer_Rating'].mean()

# ---------------- TITLE ----------------
st.title("🚖 OLA Ride Insights Dashboard")

# ---------------- KPI CARDS ----------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Rides", f"{total_rides:,}")
col2.metric("Total Revenue", f"{int(total_revenue):,}")
col3.metric("Success Rate", round(success_rate, 2))
col4.metric("Cancellation Rate", round(cancel_rate, 2))
col5.metric("Avg Rating", round(avg_rating, 2))

# ---------------- RIDE VOLUME ----------------
st.subheader("📈 Ride Volume Over Time")

rides_per_day = df.groupby(df['Date'].dt.date)['Booking_ID'].count().reset_index()
rides_per_day.columns = ['Date', 'Total Rides']

fig1 = px.line(rides_per_day, x='Date', y='Total Rides')
st.plotly_chart(fig1, use_container_width=True, key="ride_volume")

# ---------------- STATUS + RATING ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Booking Status Distribution")

    status = df['Booking_Status'].value_counts().reset_index()
    status.columns = ['Status', 'Count']

    fig2 = px.pie(status, names='Status', values='Count')
    st.plotly_chart(fig2, use_container_width=True, key="booking_status")

with col2:
    st.subheader("⭐ Avg Rating by Vehicle Type")

    rating = df.groupby('Vehicle_Type')['Customer_Rating'].mean().reset_index()
    fig3 = px.bar(rating, x='Vehicle_Type', y='Customer_Rating')

    st.plotly_chart(fig3, use_container_width=True, key="avg_rating")

# ---------------- DISTANCE + REVENUE ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Ride Distance by Vehicle Type")

    dist = df.groupby('Vehicle_Type')['Ride_Distance'].sum().reset_index()
    fig4 = px.bar(dist, x='Vehicle_Type', y='Ride_Distance')

    st.plotly_chart(fig4, use_container_width=True, key="ride_distance")

with col2:
    st.subheader("💰 Revenue by Payment Method")

    revenue = df.groupby('Payment_Method')['Booking_Value'].sum().reset_index()
    fig5 = px.bar(revenue, x='Payment_Method', y='Booking_Value')

    st.plotly_chart(fig5, use_container_width=True, key="revenue")

# ---------------- CUSTOMER CANCEL ----------------
st.subheader("❌ Customer Cancellation Reasons")

cust_cancel = df[df['Canceled_Rides_by_Customer'].notna()]

if cust_cancel.empty:
    st.warning("No customer cancellations for selected filters")
else:
    cust_reason = cust_cancel['Canceled_Rides_by_Customer'].value_counts().reset_index()
    cust_reason.columns = ['Reason', 'Count']

    fig6 = px.bar(cust_reason, x='Reason', y='Count')
    st.plotly_chart(fig6, use_container_width=True, key="cust_cancel")

# ---------------- DRIVER CANCEL ----------------
st.subheader("🚫 Driver Cancellation Reasons")

driver_cancel = df[df['Canceled_Rides_by_Driver'].notna()]

if driver_cancel.empty:
    st.warning("No driver cancellations for selected filters")
else:
    driver_reason = driver_cancel['Canceled_Rides_by_Driver'].value_counts().reset_index()
    driver_reason.columns = ['Reason', 'Count']

    fig7 = px.bar(driver_reason, x='Reason', y='Count')
    st.plotly_chart(fig7, use_container_width=True, key="driver_cancel")