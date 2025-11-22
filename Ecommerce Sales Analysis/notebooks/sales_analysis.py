"""
E-commerce Product Sales Analysis
Analyzes product-level monthly sales data across categories
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 6)

# Create visualizations directory if it doesn't exist
os.makedirs('../visualizations', exist_ok=True)

print("=" * 80)
print("E-COMMERCE PRODUCT SALES ANALYSIS")
print("=" * 80)

# Load data
df = pd.read_csv('../../Ecommerce Sales Analysis Dataset.csv')

print("\nDataset Overview:")
print(f"Total Products: {len(df):,}")
print(f"Categories: {df['category'].nunique()}")

# ============================================
# 1. DATA PREPARATION
# ============================================

# Get sales month columns
sales_months = [col for col in df.columns if col.startswith('sales_month_')]

# Calculate total sales per product
df['total_sales'] = df[sales_months].sum(axis=1)
df['avg_monthly_sales'] = df[sales_months].mean(axis=1)
df['total_revenue'] = df['total_sales'] * df['price']

print("\n" + "=" * 80)
print("KEY METRICS")
print("=" * 80)

total_units_sold = df['total_sales'].sum()
total_revenue = df['total_revenue'].sum()
avg_price = df['price'].mean()

print(f"\nTotal Units Sold: {total_units_sold:,.0f}")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Average Product Price: ${avg_price:.2f}")
print(f"Average Monthly Sales per Product: {df['avg_monthly_sales'].mean():.0f} units")

# ============================================
# 2. CATEGORY ANALYSIS
# ============================================

print("\n" + "=" * 80)
print("CATEGORY PERFORMANCE")
print("=" * 80)

category_performance = df.groupby('category').agg({
    'product_id': 'count',
    'total_sales': 'sum',
    'total_revenue': 'sum',
    'price': 'mean',
    'review_score': 'mean'
}).round(2)

category_performance.columns = ['num_products', 'total_units', 'total_revenue', 'avg_price', 'avg_review']
category_performance = category_performance.sort_values('total_revenue', ascending=False)
category_performance['revenue_pct'] = (category_performance['total_revenue'] / category_performance['total_revenue'].sum() * 100).round(2)

print("\nCategory Performance:")
print(category_performance)

# Visualize category performance
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

category_performance['total_revenue'].plot(kind='bar', ax=axes[0], color='#2E86AB')
axes[0].set_title('Revenue by Category', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Revenue ($)')
axes[0].set_xlabel('Category')
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', alpha=0.3)

axes[1].pie(category_performance['total_revenue'], labels=category_performance.index,
           autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'))
axes[1].set_title('Revenue Distribution by Category', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/category_performance.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved: category_performance.png")

# ============================================
# 3. TOP PERFORMING PRODUCTS
# ============================================

print("\n" + "=" * 80)
print("TOP PERFORMING PRODUCTS")
print("=" * 80)

top_products_revenue = df.nlargest(10, 'total_revenue')[['product_name', 'category', 'price', 'total_sales', 'total_revenue', 'review_score']]
print("\nTop 10 Products by Revenue:")
print(top_products_revenue)

plt.figure(figsize=(12, 8))
top_10 = df.nlargest(10, 'total_revenue')
plt.barh(range(len(top_10)), top_10['total_revenue'], color='#06A77D')
plt.yticks(range(len(top_10)), top_10['product_name'])
plt.xlabel('Total Revenue ($)')
plt.title('Top 10 Products by Revenue', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('../visualizations/top_products.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved: top_products.png")

# ============================================
# 4. MONTHLY SALES TRENDS
# ============================================

print("\n" + "=" * 80)
print("MONTHLY SALES TRENDS")
print("=" * 80)

monthly_sales = df[sales_months].sum()
monthly_sales.index = [f'Month {i}' for i in range(1, 13)]

print("\nMonthly Sales (Units):")
print(monthly_sales)

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

monthly_sales.plot(kind='line', marker='o', ax=axes[0], color='#E63946', linewidth=2)
axes[0].set_title('Monthly Sales Trend (Units)', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Units Sold')
axes[0].set_xlabel('Month')
axes[0].grid(alpha=0.3)

monthly_revenue = pd.Series([
    df[f'sales_month_{i}'].dot(df['price']) for i in range(1, 13)
], index=[f'Month {i}' for i in range(1, 13)])

monthly_revenue.plot(kind='line', marker='o', ax=axes[1], color='#2A9D8F', linewidth=2)
axes[1].set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Revenue ($)')
axes[1].set_xlabel('Month')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('../visualizations/monthly_trends.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved: monthly_trends.png")

# ============================================
# 5. PRICE VS SALES ANALYSIS
# ============================================

print("\n" + "=" * 80)
print("PRICE VS SALES ANALYSIS")
print("=" * 80)

correlation = df['price'].corr(df['total_sales'])
print(f"\nCorrelation between Price and Sales: {correlation:.3f}")

plt.figure(figsize=(12, 6))
for i, category in enumerate(df['category'].unique()):
    cat_data = df[df['category'] == category]
    plt.scatter(cat_data['price'], cat_data['total_sales'], alpha=0.6, label=category)
plt.xlabel('Price ($)')
plt.ylabel('Total Sales (Units)')
plt.title('Price vs Total Sales by Category', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizations/price_vs_sales.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved: price_vs_sales.png")

# ============================================
# 6. REVIEW SCORE ANALYSIS
# ============================================

print("\n" + "=" * 80)
print("REVIEW SCORE IMPACT")
print("=" * 80)

review_correlation = df['review_score'].corr(df['total_sales'])
print(f"\nCorrelation between Review Score and Sales: {review_correlation:.3f}")

df['review_bin'] = pd.cut(df['review_score'], bins=[0, 2, 3, 4, 5], labels=['Poor (0-2)', 'Fair (2-3)', 'Good (3-4)', 'Excellent (4-5)'])
review_analysis = df.groupby('review_bin', observed=True)['total_sales'].mean().sort_index()

print("\nAverage Sales by Review Score:")
print(review_analysis)

plt.figure(figsize=(10, 6))
review_analysis.plot(kind='bar', color='#F4A261')
plt.title('Average Sales by Review Score', fontsize=14, fontweight='bold')
plt.ylabel('Average Total Sales')
plt.xlabel('Review Score Range')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizations/review_impact.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved: review_impact.png")

# ============================================
# 7. KEY INSIGHTS
# ============================================

print("\n" + "=" * 80)
print("KEY BUSINESS INSIGHTS")
print("=" * 80)

top_category = category_performance.index[0]
top_category_rev_pct = category_performance.iloc[0]['revenue_pct']
best_month = monthly_sales.idxmax()
worst_month = monthly_sales.idxmin()

print(f"""
1. CATEGORY INSIGHTS
   - {top_category} is the top category with ${category_performance.iloc[0]['total_revenue']:,.2f} ({top_category_rev_pct:.1f}% of revenue)
   - Total categories: {len(category_performance)}
   - Products per category avg: {category_performance['num_products'].mean():.0f}

2. SEASONALITY
   - Best month: {best_month} with {monthly_sales.max():,.0f} units
   - Weakest month: {worst_month} with {monthly_sales.min():,.0f} units
   - Seasonal variation: {((monthly_sales.max() - monthly_sales.min()) / monthly_sales.mean() * 100):.1f}%

3. PRICING INSIGHTS
   - Price-sales correlation: {correlation:.3f}
   - {'Lower prices drive higher volume' if correlation < 0 else 'Premium pricing possible'}

4. REVIEW SCORE IMPACT
   - Review-sales correlation: {review_correlation:.3f}
   - {'Higher rated products sell better' if review_correlation > 0.2 else 'Moderate review impact'}

5. RECOMMENDATIONS
   - Focus marketing on {top_category} category
   - Prepare inventory for {best_month} peak season
   - Improve products with review scores < 3.0
   - Analyze pricing strategy based on correlation
   - Monitor seasonal trends for better forecasting
""")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
