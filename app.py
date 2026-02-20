import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("🛒 E-Commerce Sales Intelligence Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("superstore.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

# Apply Filters
filtered_df = df[
    (df["Region"].isin(region_filter)) &
    (df["Category"].isin(category_filter)) &
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1]))
]

# -----------------------------
# KPI SECTION
# -----------------------------
total_revenue = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_revenue) * 100 if total_revenue != 0 else 0

# Monthly Growth
monthly_sales = filtered_df.resample("M", on="Order Date")["Sales"].sum()
if len(monthly_sales) > 1:
    growth = ((monthly_sales.iloc[-1] - monthly_sales.iloc[-2]) / monthly_sales.iloc[-2]) * 100
else:
    growth = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")
col4.metric("Monthly Growth", f"{growth:.2f}%")

st.markdown("---")

# -----------------------------
# SALES TREND
# -----------------------------
sales_trend = filtered_df.groupby("Order Date")["Sales"].sum().reset_index()

fig1 = px.line(
    sales_trend,
    x="Order Date",
    y="Sales",
    title="📈 Sales Over Time"
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# REGION SALES
# -----------------------------
region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig2 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="🌍 Sales by Region",
    color="Region"
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# CATEGORY PERFORMANCE
# -----------------------------
category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig3 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="📦 Sales by Category",
    color="Category"
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# DISCOUNT VS PROFIT
# -----------------------------
fig4 = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    title="💸 Discount vs Profit",
    color="Category"
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------
st.subheader("🧠 Key Insights")

top_region = region_sales.sort_values(by="Sales", ascending=False).iloc[0]["Region"]
top_category = category_sales.sort_values(by="Sales", ascending=False).iloc[0]["Category"]

st.write(f"• The highest revenue generating region is **{top_region}**.")
st.write(f"• The top-performing category is **{top_category}**.")
st.write("• Higher discounts tend to reduce profit margins in certain categories.")
st.write("• Monthly growth indicates recent sales performance trend.")

st.markdown("---")

# -----------------------------
# RECOMMENDATIONS
# -----------------------------
st.subheader("💡 Strategic Recommendations")

st.write("1️⃣ Focus marketing efforts on high-performing regions.")
st.write("2️⃣ Optimize discount strategy to protect profit margins.")
st.write("3️⃣ Invest more in top-performing product categories.")
st.write("4️⃣ Monitor low-growth months and investigate root causes.")