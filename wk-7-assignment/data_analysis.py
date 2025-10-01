import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.system("cls" if os.name == "nt" else "clear")  # Clear terminal


def main():

    # Load the dataset using pandas
    df = pd.read_csv("CountryGDP-2020-2025.csv")

    # Display first ten rows
    print("\nFirst 5 rows:")
    print(df.head())

    # Explore the dataset structure
    print("\n=== Dataset Information ===")
    print(f"Shape of the dataset: {df.shape}")

    print("\n=== Data Types ===")
    print(df.dtypes)

    # Check for missing values
    print("\n=== Missing Values ===")
    missing_values = df.isnull().sum()
    print(missing_values[missing_values > 0])  # Only show columns with missing values

    # Handle missing values
    # For years with missing GDP values, use forward fill (fill with previous year's value)
    print("\n=== Handling Missing Values ===")
    print("Filling missing values using forward fill...")
    df_filled = df.ffill(axis=1)

    # If there are still missing values (e.g., in the first column), use backward fill
    df_filled = df_filled.bfill(axis=1)

    # Verify if any missing values remain
    print("\nMissing values after filling:")
    print(df_filled.isnull().sum().sum(), "missing values remaining")

    # Display the cleaned data
    print("\n=== First 5 rows of cleaned data ===")
    print(df_filled.head())

    # Basic statistics of the cleaned data
    print("\n=== Basic Statistics ===")
    print(df_filled.describe())

    ########################### Data Visualization  #########################################

    # Set the style for better-looking plots
    plt.style.use("seaborn-v0_8")

    # 1. Line Chart: GDP Trends Over Time
    print("\n=== Creating Visualizations ===")
    plt.figure(figsize=(12, 6))

    # Get year columns (assuming they are in format YYYY)
    year_columns = [col for col in df_filled.columns if col.isdigit() and len(col) == 4]

    # Convert years to datetime for better x-axis
    if year_columns:
        years = pd.to_datetime(year_columns, format="%Y")

        # Plot GDP trends for top 5 countries
        top_countries = df_filled.nlargest(5, year_columns[-1])  # Top 5 by latest year

        for _, row in top_countries.iterrows():
            plt.plot(
                years, row[year_columns], marker="o", label=row["Country"]
            )  # Assuming 'Country' column exists

        plt.title("GDP Trends (2020-2025) - Top 5 Countries", fontsize=14, pad=20)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("GDP (in Trillions USD)", fontsize=12)
        plt.legend(title="Country")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("gdp_trends-line_chart.png")
        plt.show()
        plt.close()
        print("- Created line chart: gdp_trends-line_chart.png")

    # 2. Bar Chart: Group by first letter of country name
    plt.figure(figsize=(12, 6))

    # Create a new column for the first letter of each country
    df_filled["First_Letter"] = df_filled["Country"].str[0]

    # Get the latest year with data
    latest_year = year_columns[-1]

    # Calculate average GDP by first letter
    avg_gdp = (
        df_filled.groupby("First_Letter")[latest_year]
        .mean()
        .sort_values(ascending=False)
    )

    # Create bar plot
    ax = sns.barplot(x=avg_gdp.index, y=avg_gdp.values, palette="viridis")

    # Add value labels on top of bars
    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.1f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 10),
            textcoords="offset points",
        )

    plt.title(
        f"Average GDP by Country's First Letter ({latest_year})", fontsize=14, pad=20
    )
    plt.xlabel("First Letter of Country", fontsize=12)
    plt.ylabel("Average GDP (in Millions USD)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("gdp_by_first_letter-bar_chart.png")
    plt.show()
    plt.close()
    print("- Created bar chart: gdp_by_first_letter-bar_chart.png")

    # 3. Histogram: Distribution of GDP
    plt.figure(figsize=(10, 6))
    if year_columns:
        latest_year = year_columns[-1]
        sns.histplot(data=df_filled[latest_year], bins=20, kde=True, color="skyblue")
        plt.title(f"Distribution of GDP Values ({latest_year})", fontsize=14, pad=20)
        plt.xlabel("GDP (in Trillions USD)", fontsize=12)
        plt.ylabel("Number of Countries", fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()
        plt.savefig("gdp_distribution-histogram.png")
        plt.show()
        plt.close()
        print("- Created histogram: gdp_distribution-histogram.png")

    # 4. Scatter Plot: compare gdp between two years
    if len(year_columns) >= 2:
        plt.figure(figsize=(10, 8))

        # Use the first and last years for comparison
        year1 = year_columns[0]
        year2 = year_columns[-1]

        # Create scatter plot
        sns.scatterplot(
            data=df_filled,
            x=year1,
            y=year2,
            hue="Country",
            size=year2,  # Size points by the latest year's GDP
            sizes=(20, 200),
            alpha=0.7,
            legend=False,
        )

        # Add a diagonal line for reference
        max_val = max(df_filled[[year1, year2]].max())
        plt.plot([0, max_val], [0, max_val], "r--", alpha=0.5)

        plt.title(f"GDP Comparison: {year1} vs {year2}", fontsize=14, pad=20)
        plt.xlabel(f"GDP in {year1} (Millions USD)", fontsize=12)
        plt.ylabel(f"GDP in {year2} (Millions USD)", fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()
        plt.savefig("gdp_comparison-scatter_plot.png")
        plt.show()
        plt.close()
        print(
            f"- Created scatter plot: gdp_comparison-scatter_plot.png (comparing {year1} and {year2})"
        )

    print("\nAll visualizations have been saved as PNG files.")


if __name__ == "__main__":
    main()
