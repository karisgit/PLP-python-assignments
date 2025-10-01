import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load our data into a pandas dataframe
df = pd.read_csv('car_sales_data.csv')

# show the first few rows
print(df.head())

# show basic statistics
print("\nBasic Statistics:")
print(df.describe())

# Get dataframe info
print("\nDataFrame Info:")
print(df.info())

# Display column names
print("\nColumn Names:")
print(df.columns.tolist())

# Check DataFrame dimensions
print("\n=== DataFrame Dimensions ===")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

# Check data types of each column
print("\n=== Data Types ===")
print(df.dtypes)

# Basic stats for numeric columns
print("\n=== Basic Statistics for numeric columns")
print(df.describe(include='number'))

# Additional stats
print("\nSummary for categorical columns")
print(df.describe(include=['object', 'category']))

# Check for missing values
print("\n=== Missing Values ===")
missing_values = df.isnull().sum()
print("Missing values per column:")
print(missing_values[missing_values > 0] if missing_values.sum() > 0 else "No missing values found in any column")

# Count cars by year of manufacture
yearly_counts = df['Year of manufacture'].value_counts().sort_index()

# Display the results
print("\n=== Number of Cars by Year of Manufacture ===")
print(yearly_counts)

#Show years with the most cars in descending order
yearly_counts = df['Year of manufacture'].value_counts().sort_values(ascending=False)
print("\n=== Years with Most Cars (Descending Order) ===")
print(yearly_counts)

# A detailed view including manufacturer
print("\n=== Top 10 Best Selling Car Models (with Manufacturer) ===")
top_cars_detailed = df.groupby(['Manufacturer', 'Model']).size().sort_values(ascending=False).head(10)
print(top_cars_detailed)


#--------------VISUALIZATIONS---------------------------------------------------------------------

# Plotting number of car sales over time
import matplotlib.pyplot as plt

# Count cars by year of manufacture
yearly_sales = df['Year of manufacture'].value_counts().sort_index()

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(yearly_sales.index, yearly_sales.values, marker='o', linestyle='-', linewidth=1)

# Customize the plot
plt.title('Number of Car Sales by Year', fontsize=14, fontweight='bold')
plt.xlabel('Year of Manufacture', fontsize=12)
plt.ylabel('Number of Cars Sold', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Ensure all years are shown on x-axis
plt.xticks(yearly_sales.index)

# Add data labels
for x, y in zip(yearly_sales.index, yearly_sales.values):
    plt.text(x, y, str(y), ha='center', va='bottom', fontsize=7)

plt.tight_layout()
plt.show()


# Create a horizontal bar chart of top 10 best-selling car models
top_models = df['Model'].value_counts().head(10).sort_values()

plt.figure(figsize=(12, 8))
colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(top_models)))

# Create horizontal bars
bars = plt.barh(top_models.index, top_models.values, color=colors, height=0.7)

# Add data labels on the bars
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.5,  # x position
             bar.get_y() + bar.get_height()/2,  # y position
             f'{int(width)}',  # text
             va='center',
             ha='left',
             fontsize=9)

# Customize the plot
plt.title('Top 10 Best-Selling Car Models', fontsize=14, fontweight='bold')
plt.xlabel('Number of Cars Sold', fontsize=12)
plt.ylabel('Car Model', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()

# Show and save the plot
plt.show()


# Create a scatter plot of Price vs Mileage with Engine size as color
plt.figure(figsize=(12, 7))

# Create the scatter plot with color mapping based on engine size
scatter = plt.scatter(
    x=df['Mileage'],
    y=df['Price'],
    c=df['Engine size'],  # Color points by engine size
    cmap='viridis',
    alpha=0.6,
    s=20  # Size of points
)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Engine Size (L)', rotation=270, labelpad=15)

# Customize the plot
plt.title('Car Prices vs Mileage (Colored by Engine Size)', fontsize=14, fontweight='bold')
plt.xlabel('Mileage (miles)', fontsize=12)
plt.ylabel('Price ($)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Add a trendline for better visualization of the relationship
z = np.polyfit(df['Mileage'], df['Price'], 1)
p = np.poly1d(z)
plt.plot(df['Mileage'], p(df['Mileage']), 'r--', linewidth=2)

plt.show()

# Calculate and print correlation coefficient
correlation = df['Price'].corr(df['Mileage'])
print(f"\nCorrelation between Price and Mileage: {correlation:.2f}")

# Create a box plot of Price by Fuel Type
plt.figure(figsize=(10, 6))
df.boxplot(column='Price', by='Fuel type', grid=False, vert=False)
plt.title('Price Distribution by Fuel Type', fontsize=14, fontweight='bold')
plt.suptitle('')  # Remove default title
plt.xlabel('Price ($)', fontsize=12)
plt.ylabel('Fuel Type', fontsize=12)
plt.tight_layout()
plt.show()
