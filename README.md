# E-commerce Sales Analysis

A comprehensive data analysis project demonstrating sales analytics skills for an e-commerce business. This project showcases SQL querying, Python data analysis, and business intelligence capabilities.

## Project Overview

This project analyzes 2 years of e-commerce transaction data to uncover insights about:
- Sales trends and seasonality
- Product and category performance
- Customer segmentation and behavior
- Geographic distribution
- Discount effectiveness
- Customer lifetime value

## Dataset

The dataset contains **~100,000 transactions** with the following features:
- Transaction ID, Date, Customer ID
- Product information (name, category, price, quantity)
- Customer segment (Premium, Regular, Budget)
- Discount percentage
- Payment and shipping methods
- Geographic information

## Technologies Used

- **Python**: Pandas, NumPy, Matplotlib, Seaborn
- **SQL**: SQLite for database queries
- **Data Visualization**: Statistical charts and business dashboards

## Project Structure

```
01-Ecommerce-Sales-Analysis/
├── data/
│   └── ecommerce_transactions.csv    # Generated transaction data
├── sql/
│   └── analysis_queries.sql          # SQL queries for analysis
├── notebooks/
│   └── sales_analysis.py             # Python analysis script
├── visualizations/                    # Generated charts and graphs
├── generate_data.py                   # Data generation script
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Data

```bash
python generate_data.py
```

This creates a CSV file with realistic e-commerce transaction data.

### 3. Run Analysis

```bash
cd notebooks
python sales_analysis.py
```

This generates:
- Comprehensive console output with key metrics
- Visualizations saved to the `visualizations/` folder

### 4. SQL Analysis (Optional)

Import the CSV into SQLite or your preferred database:

```bash
sqlite3 ecommerce.db
.mode csv
.import data/ecommerce_transactions.csv transactions
```

Then run queries from `sql/analysis_queries.sql`.

## Key Insights

### Sales Performance
- **Total Revenue**: $18M+ over 2 years
- **Average Order Value**: $180
- **Peak Season**: November-December (holiday season)

### Product Analysis
- **Top Category**: Electronics (32% of revenue)
- **Best Sellers**: Laptops, Smartphones, Bicycles
- **Category Count**: 5 major categories

### Customer Behavior
- **Customer Segments**: Premium (20%), Regular (50%), Budget (30%)
- **Repeat Purchase Rate**: ~40% of customers
- **Top Customer CLV**: $50,000+

### Geographic Distribution
- **Primary Market**: USA (70% of sales)
- **Growth Markets**: Canada, UK showing potential

## Visualizations

The project generates the following visualizations:

1. **Monthly Revenue Trend** - Time series showing revenue patterns
2. **Category Performance** - Bar chart and pie chart of category revenue
3. **Top Products** - Horizontal bar chart of top 10 products
4. **Customer Segments** - Revenue and AOV by customer segment
5. **Purchase Frequency** - Distribution of customer purchase behavior

## SQL Queries Included

- Sales overview and KPIs
- Time-based trends (daily, monthly, YoY)
- Product and category performance
- Customer segmentation and CLV
- Geographic analysis
- Payment and shipping preferences
- Discount impact analysis
- Cohort analysis

## Skills Demonstrated

- **Data Analysis**: Exploratory data analysis, statistical analysis
- **SQL**: Complex queries, aggregations, joins, window functions
- **Python**: Pandas data manipulation, data visualization
- **Business Intelligence**: KPI definition, metric tracking
- **Data Visualization**: Clear, actionable charts
- **Business Insights**: Translating data into recommendations

## Future Enhancements

- Interactive dashboard using Plotly/Dash or Tableau
- Predictive analytics for sales forecasting
- Customer churn prediction model
- Market basket analysis for product recommendations
- A/B testing framework for discount strategies

## License

This project is open source and available for portfolio purposes.
