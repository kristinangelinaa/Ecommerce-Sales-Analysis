"""
E-commerce Sales Data Generator
Generates realistic sales transaction data for analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate dates for 2 years of data
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Product categories and products
products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smart Watch'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Dress'],
    'Home & Garden': ['Blender', 'Vacuum Cleaner', 'Coffee Maker', 'Lamp', 'Bed Sheets'],
    'Books': ['Fiction Novel', 'Cookbook', 'Self-Help Book', 'Biography', 'Textbook'],
    'Sports': ['Yoga Mat', 'Dumbbells', 'Running Shoes', 'Tennis Racket', 'Bicycle']
}

# Price ranges for each category
price_ranges = {
    'Electronics': (50, 1500),
    'Clothing': (15, 150),
    'Home & Garden': (20, 300),
    'Books': (10, 50),
    'Sports': (25, 500)
}

# Customer segments
customer_segments = ['Premium', 'Regular', 'Budget']

# Generate transaction data
transactions = []
transaction_id = 1000

for date in date_range:
    # Seasonal variation in number of transactions
    month = date.month
    base_transactions = 100

    # More sales in Nov-Dec (holiday season)
    if month in [11, 12]:
        daily_transactions = np.random.randint(150, 250)
    # Summer sales (June-Aug)
    elif month in [6, 7, 8]:
        daily_transactions = np.random.randint(120, 180)
    else:
        daily_transactions = np.random.randint(80, 140)

    for _ in range(daily_transactions):
        category = random.choice(list(products.keys()))
        product = random.choice(products[category])

        # Generate price with some variation
        min_price, max_price = price_ranges[category]
        base_price = np.random.uniform(min_price, max_price)

        # Quantity (most people buy 1-3 items)
        quantity = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])

        # Customer segment affects discount
        segment = np.random.choice(customer_segments, p=[0.2, 0.5, 0.3])

        if segment == 'Premium':
            discount = np.random.uniform(0.05, 0.15)
        elif segment == 'Regular':
            discount = np.random.uniform(0, 0.10)
        else:  # Budget
            discount = np.random.uniform(0, 0.05)

        # Holiday discounts
        if month in [11, 12]:
            discount += np.random.uniform(0.05, 0.15)

        discount = min(discount, 0.40)  # Max 40% discount

        price_per_unit = base_price * (1 - discount)
        total_amount = price_per_unit * quantity

        # Payment method
        payment_method = np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'],
                                        p=[0.4, 0.3, 0.2, 0.1])

        # Shipping method
        shipping_method = np.random.choice(['Standard', 'Express', 'Next Day'],
                                         p=[0.6, 0.3, 0.1])

        # Country (primarily US, with some international)
        country = np.random.choice(['USA', 'Canada', 'UK', 'Germany', 'France'],
                                  p=[0.7, 0.1, 0.1, 0.05, 0.05])

        # Customer ID (repeat customers)
        customer_id = np.random.randint(1, 5000)

        transactions.append({
            'transaction_id': transaction_id,
            'date': date,
            'customer_id': customer_id,
            'customer_segment': segment,
            'category': category,
            'product_name': product,
            'quantity': quantity,
            'unit_price': round(base_price, 2),
            'discount_percent': round(discount * 100, 2),
            'total_amount': round(total_amount, 2),
            'payment_method': payment_method,
            'shipping_method': shipping_method,
            'country': country
        })

        transaction_id += 1

# Create DataFrame
df = pd.DataFrame(transactions)

# Save to CSV
df.to_csv('data/ecommerce_transactions.csv', index=False)

print(f"Generated {len(df)} transactions")
print(f"\nDataset Info:")
print(f"Date Range: {df['date'].min()} to {df['date'].max()}")
print(f"Total Revenue: ${df['total_amount'].sum():,.2f}")
print(f"Number of Unique Customers: {df['customer_id'].nunique()}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nDataset saved to 'data/ecommerce_transactions.csv'")
