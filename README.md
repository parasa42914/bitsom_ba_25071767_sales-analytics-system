# Sales Analytics System
A modular Python-based data engineering pipeline designed to ingest raw sales data, validate and clean transaction records, enrich data using a REST API (DummyJSON), and generate comprehensive business intelligence reports.

## 🚀 Features
**1. Robust :** File Handling: Manages multiple file encodings (UTF-8, Latin-1, CP1252) with automatic error handling.

**2. Data Cleaning & Validation:** Strictly filters records based on business logic (e.g., Transaction ID formatting, positive quantity/price checks).

**3. API Integration:** Enriches local sales data with product categories and brands fetched from the DummyJSON API.

**4. Interactive CLI:** Allows users to view data ranges and apply custom filters for region or transaction amount before processing.

**5. Detailed Reporting:** Generates a formatted text report covering regional performance, customer trends, and product analysis.

# 📂 Project Structure
Plaintext

sales_analytics_project/
│
├── main.py                 # Entry point: Orchestrates the 10-step workflow
├── data/
│   ├── sales_data.txt      # Input: Raw pipe-delimited sales data
│   └── enriched_sales_data.txt # Output: API-enriched data file
│
├── output/
│   └── sales_report.txt    # Output: Final generated analysis report
│
├── utils/                  # Core logic modules
│   ├── file_handler.py     # File I/O and encoding management
│   ├── api_handler.py      # REST API requests and data mapping
│   ├── data_processor.py   # Validation, cleaning, and sales analytics
│   └── report_generator.py # Formatted text report generation
│
└── requirements.txt        # Project dependencies (requests)

# 🛠️ Installation & Setup
## 1.Clone the project:

```
Bash

mkdir sales_analytics_project
cd sales_analytics_project
```

## 2. Install dependencies: 
The project requires the ```requests``` library to communicate with the API.

```
Bash

python -m pip install requests
```

## Prepare Data: 
Ensure your raw data is placed in ```data/sales_data.txt``` using the pipe ```(|)``` delimiter.

# ⚙️ Data Pipeline Workflow
The system follows a 10-step execution logic as shown in the console:

**1. Ingestion:** Reads the source file while skipping headers and empty lines.

**2. Cleaning:** Removes rows with missing CustomerID, invalid TransactionIDs, or non-positive values.

**3. User Filtering:** Displays available regions and price ranges; prompts user for optional filtering.

**4. Analysis:** Calculates revenue metrics, daily trends, and identifies top-performing products.

**5. Enrichment:** Extracts numeric IDs from ProductID (e.g., P101 → 101) to match against API product records.

**6. Export:** Saves an enriched version of the dataset including API Category, Brand, and Rating.

**7. Reporting:** Produces the final sales_report.txt.

<br>

# 📊 Sample Output (sales_report.txt)
The generated report includes:

**1. Overall Summary:** Total revenue and date ranges.

**2. Region-Wise Performance:** Sales breakdown by territory.

**3. Top 5 Lists:** Ranking of highest-performing products and customers.

**4. Enrichment Summary:** Metrics on successful API data matching.

<br>

# ⚠️ Error Handling
The system is designed to be resilient:

**1. FileNotFound:** Alerts the user if the data source is missing rather than crashing.

**2. API Failure:** If the DummyJSON API is unreachable, the system continues processing local data and marks API fields as None.

**3. Global Catch:** All major operations are wrapped in try-except blocks to provide user-friendly error messages in the console.