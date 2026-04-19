import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Fintech Expense Tracker", layout="wide")

st.title("💰 Fintech Expense Tracker Dashboard")

# -----------------------------
# LOAD / GENERATE DATA
# -----------------------------
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=180)

    categories = ["Food", "Rent", "Travel", "Shopping", "Utilities", "Entertainment"]
    payment_methods = ["Cash", "Card", "UPI"]

    df = pd.DataFrame({
        "Date": np.random.choice(dates, 500),
        "Category": np.random.choice(categories, 500),
        "Amount": np.random.randint(100, 5000, 500),
        "Payment Method": np.random.choice(payment_methods, 500)
    })

    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    return df


data = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=data['Category'].unique(),
    default=data['Category'].unique()
)

selected_payment = st.sidebar.multiselect(
    "Payment Method",
    options=data['Payment Method'].unique(),
    default=data['Payment Method'].unique()
)

filtered_data = data[
    (data['Category'].isin(selected_category)) &
    (data['Payment Method'].isin(selected_payment))
]

# -----------------------------
# KPIs (FINTECH STYLE)
# -----------------------------
total_spend = filtered_data['Amount'].sum()
avg_spend = filtered_data['Amount'].mean()
max_category = filtered_data.groupby('Category')['Amount'].sum().idxmax()

col1, col2, col3 = st.columns(3)

col1.metric("💸 Total Spend", f"₹{total_spend:,.0f}")
col2.metric("📊 Avg Transaction", f"₹{avg_spend:,.0f}")
col3.metric("🔥 Top Category", max_category)

st.markdown("---")

# -----------------------------
# CHARTS
# -----------------------------

col4, col5 = st.columns(2)

# Category Spending
with col4:
    st.subheader("📊 Category Spending")
    cat_spend = filtered_data.groupby("Category")['Amount'].sum().sort_values()
    fig, ax = plt.subplots()
    cat_spend.plot(kind='barh', ax=ax)
    st.pyplot(fig)

# Monthly Trend
with col5:
    st.subheader("📈 Monthly Trend")
    month_spend = filtered_data.groupby("Month")['Amount'].sum()
    fig, ax = plt.subplots()
    month_spend.plot(marker='o', ax=ax)
    st.pyplot(fig)

# -----------------------------
# PIE CHART
# -----------------------------
st.subheader("🧾 Spending Distribution")
fig, ax = plt.subplots()
cat_spend.plot(kind='pie', autopct='%1.1f%%', ax=ax)
st.pyplot(fig)

# -----------------------------
# TABLE VIEW
# -----------------------------
st.subheader("📋 Transaction Data")
st.dataframe(filtered_data.sort_values(by="Date", ascending=False))

# -----------------------------
# INSIGHTS SECTION
# -----------------------------
st.subheader("🧠 Insights")

st.write(f"- You are spending most on **{max_category}**.")

if total_spend > 100000:
    st.warning("⚠️ High spending detected! Consider budgeting.")
else:
    st.success("✅ Spending is under control.")
