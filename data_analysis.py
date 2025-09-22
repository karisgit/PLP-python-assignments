import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset using pandas
df = pd.read_csv('CountryGDP-2020-2025.csv')   

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
plt.style.use('seaborn-v0_8')

# 1. Line Chart: GDP Trends Over Time
print("\n=== Creating Visualizations ===")
plt.figure(figsize=(12, 6))

# Get year columns (assuming they are in format YYYY)
year_columns = [col for col in df_filled.columns if col.isdigit() and len(col) == 4]

# Convert years to datetime for better x-axis
if year_columns:
    years = pd.to_datetime(year_columns, format='%Y')
    
    # Plot GDP trends for top 5 countries
    top_countries = df_filled.nlargest(5, year_columns[-1])  # Top 5 by latest year
    
    for _, row in top_countries.iterrows():
        plt.plot(years, row[year_columns], marker='o', label=row['Country'])  # Assuming 'Country' column exists
    
    plt.title('GDP Trends (2020-2025) - Top 5 Countries', fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('GDP (in Trillions USD)', fontsize=12)
    plt.legend(title='Country')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('gdp_trends.png')
    plt.close()
    print("- Created line chart: gdp_trends.png")

# 2. Bar Chart: Average GDP by Region (if Region exists)
if 'Region' in df_filled.columns:
    plt.figure(figsize=(10, 6))
    
    # Calculate average GDP by region for the latest year
    latest_year = year_columns[-1]
    avg_gdp = df_filled.groupby('Region')[latest_year].mean().sort_values(ascending=False)
    
    # Create bar plot
    ax = sns.barplot(x=avg_gdp.index, y=avg_gdp.values, palette='viridis')
    
    # Add value labels on top of bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}T', 
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center', 
                   xytext=(0, 10), 
                   textcoords='offset points')
    
    plt.title(f'Average GDP by Region ({latest_year})', fontsize=14, pad=20)
    plt.xlabel('Region', fontsize=12)
    plt.ylabel('Average GDP (in Trillions USD)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('gdp_by_region.png')
    plt.close()
    print("- Created bar chart: gdp_by_region.png")

# 3. Histogram: Distribution of GDP
plt.figure(figsize=(10, 6))
if year_columns:
    latest_year = year_columns[-1]
    sns.histplot(data=df_filled[latest_year], bins=20, kde=True, color='skyblue')
    plt.title(f'Distribution of GDP Values ({latest_year})', fontsize=14, pad=20)
    plt.xlabel('GDP (in Trillions USD)', fontsize=12)
    plt.ylabel('Number of Countries', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('gdp_distribution.png')
    plt.close()
    print("- Created histogram: gdp_distribution.png")

# 4. Scatter Plot: GDP vs Population (if Population column exists)
if 'Population' in df_filled.columns and year_columns:
    plt.figure(figsize=(10, 6))
    latest_year = year_columns[-1]
    
    # Create scatter plot with size based on GDP per capita
    scatter = plt.scatter(
        x=df_filled['Population'],
        y=df_filled[latest_year],
        s=df_filled[latest_year]/df_filled[latest_year].max() * 300,  # Scale point sizes
        alpha=0.6,
        c=df_filled[latest_year],
        cmap='viridis'
    )
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('GDP (in Trillions USD)')
    
    plt.title(f'GDP vs Population ({latest_year})', fontsize=14, pad=20)
    plt.xlabel('Population (in Billions)', fontsize=12)
    plt.ylabel('GDP (in Trillions USD)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Add a trendline
    z = np.polyfit(df_filled['Population'], df_filled[latest_year], 1)
    p = np.poly1d(z)
    plt.plot(df_filled['Population'], p(df_filled['Population']), "r--")
    
    plt.tight_layout()
    plt.savefig('gdp_vs_population.png')
    plt.close()
    print("- Created scatter plot: gdp_vs_population.png")

print("\nAll visualizations have been saved as PNG files.")

# If Population column doesn't exist, create a sample scatter plot with two GDP years
if 'Population' not in df_filled.columns and len(year_columns) >= 2:
    plt.figure(figsize=(10, 6))
    plt.scatter(
        x=df_filled[year_columns[0]],
        y=df_filled[year_columns[-1]],
        alpha=0.6,
        c='green'
    )
    
    # Add labels and title
    plt.title(f'GDP Comparison: {year_columns[0]} vs {year_columns[-1]}', fontsize=14, pad=20)
    plt.xlabel(f'GDP in {year_columns[0]} (in Trillions USD)', fontsize=12)
    plt.ylabel(f'GDP in {year_columns[-1]} (in Trillions USD)', fontsize=12)
    
    # Add a reference line
    max_val = max(df_filled[year_columns[0]].max(), df_filled[year_columns[-1]].max())
    plt.plot([0, max_val], [0, max_val], 'r--')
    
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('gdp_comparison.png')
    plt.close()
    print("- Created GDP comparison scatter plot: gdp_comparison.png")