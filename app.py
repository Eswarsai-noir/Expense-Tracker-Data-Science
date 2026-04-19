import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fintech Dashboard", layout="wide")

st.title("💰 Expense Tracker (Auto Simulation Mode)")

# -----------------------------
# GENERATE SYNTHETIC DATA
# -----------------------------
@st.cache_data
def generate_data():
    np.random.seed(42)

    dates = pd.date_range(end=pd.Timestamp.today(), periods=180)

    categories = ["Food", "Rent", "Travel", "Shopping", "Utilities", "Entertainment"]
    payment_methods = ["Cash", "Card", "UPI"]

    data = pd.DataFrame({
        "Date": np.random.choice(dates, 500),
        "Category": np.random.choice(categories, 500),
        "Amount": np.random.randint(100, 5000, 500),
        "Payment Method": np.random.choice(payment_methods, 500)
    })

    # Convert to datetime safely
    data["Date"] = pd.to_datetime(data["Date"], errors='coerce')
    data = data.dropna(subset=["Date"])

    data["Month"] = data["Date"].dt.month

    return data

data = generate_data()

# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

selected_category = st.sidebar.multiselect(
    "Category",
    options=data["Category"].unique(),
    default=data["Category"].unique()
)

filtered = data[data["Category"].isin(selected_category)]

# -----------------------------
# KPIs
# -----------------------------
total = filtered["Amount"].sum()
avg = filtered["Amount"].mean()
top_cat = filtered.groupby("Category")["Amount"].sum().idxmax()

c1, c2, c3 = st.columns(3)
c1.metric("💸 Total Spend", f"₹{total:,.0f}")
c2.metric("📊 Avg Spend", f"₹{avg:,.0f}")
c3.metric("🔥 Top Category", top_cat)

# -----------------------------
# BUDGET
# -----------------------------
st.subheader("🎯 Budget Tracking")
budget = st.number_input("Monthly Budget", value=50000)

if total > budget:
    st.error(f"⚠️ Exceeded by ₹{total - budget:,.0f}")
else:
    st.success(f"✅ Remaining ₹{budget - total:,.0f}")

# -----------------------------
# CHARTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Category Spending")
    cat = filtered.groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    cat.plot(kind="barh", ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("📈 Monthly Trend")
    month = filtered.groupby("Month")["Amount"].sum()
    fig, ax = plt.subplots()
    month.plot(marker="o", ax=ax)
    st.pyplot(fig)

st.subheader("🧾 Spending Distribution")
fig, ax = plt.subplots()
cat.plot(kind="pie", autopct="%1.1f%%", ax=ax)
st.pyplot(fig)

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📋 Transactions")
st.dataframe(filtered.sort_values(by="Date", ascending=False))

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("🧠 Insights")

st.write(f"Top category: **{top_cat}**")

if total > budget:
    st.warning("Reduce discretionary spending.")
else:
    st.success("Spending is under control.")