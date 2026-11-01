
# Import required libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "OnlineRetail_Cleaned.csv"
FORECAST_PATH = BASE_DIR / "data" / "forecast_results.csv"

# --------------------------------------------------
# 3. CUSTOM CSS
# --------------------------------------------------

st.markdown("""

<style>
    .stApp {
        background-color: #F4F7FB;
    }

    [data-testid="stSidebar"] {
        background-color: #102A43;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #102A43;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #627D98;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .metric-card {
        background-color: white;
        padding: 22px;
        border-radius: 14px;
        border-left: 5px solid #16A6A1;
        box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }

    .metric-label {
        color: #627D98;
        font-size: 14px;
        font-weight: 600;
    }

    .metric-value {
        color: #102A43;
        font-size: 25px;
        font-weight: 800;
    }

    .section-title {
        color: #102A43;
        font-size: 21px;
        font-weight: 700;
        margin-top: 15px;
    }

    /* Sidebar filter styling */
[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] input {
    color: #102A43 !important;
    background-color: white !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: white !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #102A43 !important;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 4. LOAD DATASET
# --------------------------------------------------

@st.cache_data
def load_data(path):
    return pd.read_csv(path, low_memory=False)

if not DATA_PATH.exists():
    st.error("Cleaned dataset not found. Please check the data folder.")
    st.stop()

df = load_data(str(DATA_PATH))

# Convert date column
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)

# Ensure Revenue is numeric
df["Revenue"] = pd.to_numeric(
    df["Revenue"], errors="coerce"
)

df = df.dropna(subset=["InvoiceDate", "Revenue"])

# --------------------------------------------------
# INTERACTIVE FILTERS
# --------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Dashboard Filters")

# Date range filter
min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Country filter
countries = ["All Countries"] + sorted(
    df["Country"].dropna().unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

# Apply selected filters
if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    df = df[
        (df["InvoiceDate"].dt.date >= start_date) &
        (df["InvoiceDate"].dt.date <= end_date)
    ]

if selected_country != "All Countries":
    df = df[df["Country"] == selected_country]

# --------------------------------------------------
# 5. SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.markdown("# 📊 Sales BI")
st.sidebar.caption("Business Intelligence Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    ["🏠 Overview", "📈 Sales Analytics", "🔮 Forecast Results"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Sales Forecasting Project")
st.sidebar.caption("Built with Python & Streamlit")

# --------------------------------------------------
# 6. DASHBOARD HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">Sales Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Analyze sales performance, customer '
    'markets and business trends.</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# 7. OVERVIEW PAGE
# --------------------------------------------------

if page == "🏠 Overview":

    total_sales = df["Revenue"].sum()
    total_orders = df["InvoiceNo"].nunique()
    total_customers = df["CustomerID"].nunique()
    total_products = df["Description"].nunique()

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "💰 Total Revenue", f"£{total_sales:,.0f}"),
        (col2, "🧾 Total Orders", f"{total_orders:,}"),
        (col3, "👥 Customers", f"{total_customers:,}"),
        (col4, "📦 Products", f"{total_products:,}")
    ]

    for column, label, value in metrics:
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Monthly Sales Trend
    monthly_sales = (
        df.groupby(df["InvoiceDate"].dt.to_period("M"))["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_sales["Month"] = monthly_sales["InvoiceDate"].astype(str)

    # Top Countries
    country_sales = (
        df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="section-title">📈 Monthly Sales Trend</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(
            monthly_sales["Month"],
            monthly_sales["Revenue"],
            marker="o",
            linewidth=2
        )
        ax.set_ylabel("Revenue (£)")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(alpha=0.2)
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    with right:
        st.markdown(
            '<div class="section-title">🌍 Top 10 Countries</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(8, 4))
        country_sales.plot(kind="barh", ax=ax)
        ax.set_xlabel("Revenue (£)")
        ax.set_ylabel("")
        ax.grid(axis="x", alpha=0.2)
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    # Top Products
    st.markdown(
        '<div class="section-title">🏆 Top 10 Products</div>',
        unsafe_allow_html=True
    )

    top_products = (
        df.groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(11, 5))
    top_products.plot(kind="barh", ax=ax)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

# --------------------------------------------------
# 8. SALES ANALYTICS PAGE
# --------------------------------------------------

elif page == "📈 Sales Analytics":

    st.subheader("📈 Detailed Sales Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Country-wise Sales")
        country_table = (
            df.groupby("Country")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        st.dataframe(country_table, width="stretch")

    with col2:
        st.markdown("### Product-wise Sales")
        product_table = (
            df.groupby("Description")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(20)
            .reset_index()
        )
        st.dataframe(product_table, width="stretch")

    st.markdown("### Monthly Sales Report")

    monthly_report = (
        df.groupby(df["InvoiceDate"].dt.to_period("M"))["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_report["Month"] = monthly_report["InvoiceDate"].astype(str)
    monthly_report = monthly_report[["Month", "Revenue"]]

    st.dataframe(monthly_report, width="stretch")

# --------------------------------------------------
# 9. FORECAST RESULTS PAGE
# --------------------------------------------------

elif page == "🔮 Forecast Results":

    st.subheader("🔮 Sales Forecast Results")

    if FORECAST_PATH.exists():

        forecast_df = pd.read_csv(FORECAST_PATH)

                # Calculate model performance metrics
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        import numpy as np

        # Select actual and predicted sales columns
        actual = forecast_df["Actual_Sales"]
        predicted = forecast_df["Predicted_Sales"]

        # Calculate MAE, RMSE and R2 Score
        mae = mean_absolute_error(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        r2 = r2_score(actual, predicted)

        # Display performance metrics
        st.markdown("### 🎯 Model Performance")

        col1, col2, col3 = st.columns(3)

        col1.metric("MAE", f"{mae:,.2f}")
        col2.metric("RMSE", f"{rmse:,.2f}")
        col3.metric("R² Score", f"{r2:.4f}")

        st.success("Forecast results loaded successfully!")

        st.markdown("### Forecast Dataset Preview")
        st.dataframe(forecast_df.head(20), width="stretch")

        # Find actual and predicted columns
        actual_col = next(
            (c for c in forecast_df.columns
             if c.lower() in ["actual", "actual_sales", "y_test"]),
            None
        )

        predicted_col = next(
            (c for c in forecast_df.columns
             if c.lower() in ["predicted", "predicted_sales", "y_pred"]),
            None
        )

        if actual_col and predicted_col:

            fig, ax = plt.subplots(figsize=(11, 5))

            ax.plot(
                forecast_df[actual_col].values,
                label="Actual Sales"
            )

            ax.plot(
                forecast_df[predicted_col].values,
                label="Predicted Sales"
            )

            ax.set_title("Actual vs Predicted Sales")
            ax.set_xlabel("Test Records")
            ax.set_ylabel("Revenue")
            ax.legend()
            ax.grid(alpha=0.2)

            fig.tight_layout()
            st.pyplot(fig, width="stretch")
            plt.close(fig)

        else:
            st.info(
                "Forecast file is available, but actual and predicted "
                "column names need to be matched."
            )

    else:
        st.warning(
            "Forecast results file not found in the data folder."
        )

# --------------------------------------------------
# 10. FOOTER
# --------------------------------------------------

st.markdown("---")
st.markdown(
    "<center>Sales Forecasting & Business Intelligence | "
    "Built using Python, Pandas, Matplotlib and Streamlit</center>",
    unsafe_allow_html=True
)