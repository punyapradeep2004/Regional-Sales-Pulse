Regional Sales Pulse

1. Project Overview

Regional Sales Pulse is an interactive business analytics dashboard developed using Python and Streamlit. The project analyzes sales performance, regional profitability, product performance, monthly trends, yearly performance, and the impact of discounts.

Using the Sample Superstore dataset, this project aims to identify business trends, understand profitability, and provide data-driven recommendations.

2. Business Objectives

- Analyze overall sales and profit performance.
- Compare sales and profitability across regions.
- Identify profitable and loss-making product categories and sub-categories.
- Analyze monthly sales trends.
- Evaluate year-wise sales and profit performance.
- Understand the relationship between discounts and profitability.
- Generate meaningful business insights and recommendations.

3. Tools and Technologies Used

- Python
- Pandas
- NumPy
- Streamlit
- Matplotlib
- Plotly
- Excel
- Jupyter Notebook

4. Key Performance Indicators (KPIs)

- Total Sales
- Total Profit
- Profit Margin (%)
- Total Records
- Total Orders

5. Key Features

- Interactive dashboard filters.
- Regional sales and profit analysis.
- Category-wise performance analysis.
- Sub-category-wise profitability analysis.
- Monthly sales trend analysis.
- Year-wise sales and profit analysis.
- Customer segment analysis.
- Discount impact on profitability.
- Business insights and recommendations.

6. Key Business Questions

1. Which product sub-categories generate losses, and how much?
2. At what discount levels do orders start generating losses on average?
3. Which region has the highest sales but the lowest profit margin?
4. How do monthly sales trends change over time?
5. How does sales and profit performance vary across years?

7. Excel Pivot Table Analysis and Data Validation

Excel Pivot Tables were created to independently verify the Python analysis.

The following analyses were performed using Excel:

- Region-wise Sales and Profit Analysis.
- Category-wise Sales and Profit Analysis.
- Sub-Category-wise Sales and Profit Analysis.
- Monthly Sales Analysis.
- Year-wise Sales and Profit Analysis.

The corresponding results from Excel Pivot Tables were compared with the Python analysis outputs to check consistency and accuracy.

Key calculations and dashboard values were also cross-checked against the original dataset.

8. Business Insights and Recommendations

The dashboard presents five key business insights supported by numerical findings.

It also provides five business recommendations to identify improvement opportunities and support data-driven decision-making.

9. Project Files

- "APP.py" – Streamlit dashboard application.
- "Sample - Superstore.csv" – Dataset used for analysis.
- "Regional_Sales_Analysis.ipynb" – Data cleaning, exploration, and analysis.
- "requirements.txt" – Required Python libraries.
- ".gitignore" – Files excluded from version control.
- "screenshots/" – Dashboard screenshots.

10. How to Run the Project

Step 1: Clone the Repository

git clone https://github.com/punyapradeep2004/Regional-Sales-Pulse.git

Step 2: Open the Project Folder

cd Regional-Sales-Pulse

Step 3: Install Required Libraries

pip install -r requirements.txt

Step 4: Run the Streamlit Application

python -m streamlit run APP.py

The dashboard will open in your web browser.

Make sure the dataset "Sample - Superstore.csv" is available in the project folder.

11. What I Verified and What I Changed by Hand

What I Verified

- Compared region-wise sales and profit results between Excel and Python.
- Verified category-wise and sub-category-wise performance.
- Compared monthly sales trends.
- Checked year-wise sales and profit results.
- Cross-checked key dashboard calculations against the original dataset.

What I Changed by Hand

- Reviewed and cleaned the dataset before analysis.
- Improved the dashboard layout and visual presentation.
- Reviewed charts to avoid unnecessary duplication.
- Organized business insights and recommendations for better understanding.

12. Conclusion

Regional Sales Pulse demonstrates how Python, Excel, and interactive visualization can be used to analyze business performance, identify profitability issues, understand sales trends, evaluate discount impact, and support informed business decisions.