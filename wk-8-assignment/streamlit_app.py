import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration
st.set_page_config(page_title="Car Sales Analysis", page_icon="🚗", layout="wide")


# Load the data
@st.cache_data  # This will cache the data to avoid reloading it on every interaction
def load_data():
    return pd.read_csv("car_sales_data.csv")


df = load_data()

# Title and description
st.title("🚗 Car Sales Analysis Dashboard")
st.markdown(
    """
This interactive dashboard helps you explore car sales data. Use the filters on the sidebar to analyze different aspects of the data.
"""
)

# Sidebar filters
st.sidebar.header("Filters")

# Year range slider
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df["Year of manufacture"].min()),
    max_value=int(df["Year of manufacture"].max()),
    value=(2000, 2022),
)

# Manufacturer multiselect
manufacturers = st.sidebar.multiselect(
    "Select Manufacturers",
    options=df["Manufacturer"].unique(),
    default=df["Manufacturer"].unique(),
)

# Apply filters
filtered_df = df[
    (df["Year of manufacture"] >= year_range[0])
    & (df["Year of manufacture"] <= year_range[1])
    & (df["Manufacturer"].isin(manufacturers) if manufacturers else True)
]

# Show data summary
st.subheader("Data Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Cars", len(filtered_df))
col2.metric("Average Price", f"${filtered_df['Price'].mean():,.0f}")
col3.metric("Average Mileage", f"{filtered_df['Mileage'].mean():,.0f} miles")

# Show sample data
expander = st.expander("View Sample Data")
with expander:
    st.dataframe(filtered_df.head(10))

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["Sales Over Time", "Price Analysis", "Top Models"])

with tab1:
    st.subheader("Car Sales by Year")
    yearly_sales = filtered_df["Year of manufacture"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(yearly_sales.index, yearly_sales.values, color="skyblue")
    ax.set_title("Number of Cars Sold by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Cars Sold")
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

with tab2:
    st.subheader("Price Analysis")

    # Scatter plot
    fig, ax = plt.subplots(figsize=(10, 5))
    scatter = ax.scatter(
        x=filtered_df["Mileage"],
        y=filtered_df["Price"],
        c=filtered_df["Engine size"],
        cmap="viridis",
        alpha=0.6,
        s=20,
    )

    # Add trendline
    z = np.polyfit(filtered_df["Mileage"], filtered_df["Price"], 1)
    p = np.poly1d(z)
    ax.plot(filtered_df["Mileage"], p(filtered_df["Mileage"]), "r--", linewidth=2)

    # Customize plot
    plt.colorbar(scatter, label="Engine Size (L)")
    ax.set_title("Price vs Mileage (Colored by Engine Size)")
    ax.set_xlabel("Mileage (miles)")
    ax.set_ylabel("Price ($)")
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

    # Show correlation
    correlation = filtered_df["Price"].corr(filtered_df["Mileage"])
    st.metric("Correlation between Price and Mileage", f"{correlation:.2f}")

with tab3:
    st.subheader("Top Selling Models")

    # Get top 10 models
    top_models = filtered_df["Model"].value_counts().head(10).sort_values()

    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(top_models)))
    bars = ax.barh(top_models.index, top_models.values, color=colors, height=0.7)

    # Add data labels
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}",
            va="center",
            fontsize=9,
        )

    # Customize plot
    ax.set_title("Top 10 Best-Selling Car Models")
    ax.set_xlabel("Number of Cars Sold")
    ax.set_ylabel("Car Model")
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    st.pyplot(fig)

# Add some space at the bottom
st.markdown("---")
st.markdown("*Data Analysis Dashboard created with Streamlit*")
