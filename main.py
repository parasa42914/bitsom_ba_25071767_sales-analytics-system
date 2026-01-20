import sys
import os
from utils.file_handler import read_sales_data
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.data_processor import (
    parse_transactions, validate_and_filter, enrich_sales_data,
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend
)
from utils.report_generator import generate_sales_report

def main():
    """Main execution function following the 13-step workflow."""
    try:
        # 1. Print welcome message
        print("===========================================")
        print("          SALES ANALYTICS SYSTEM           ")
        print("===========================================\n")

        # 2. Read sales data file (handle encoding)
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        if not raw_lines:
            print("Error: No data found.")
            return
        print(f"✓ Successfully read {len(raw_lines)} transactions\n")

        # 3. Parse and clean transactions
        print("[2/10] Parsing and cleaning data...")
        parsed_data = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_data)} records\n")

        # 4. Display filter options to user
        print("[3/10] Filter Options Available:")
        regions = sorted(list(set(t['Region'] for t in parsed_data)))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in parsed_data]
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}\n")

        # 5. Ask if user wants to filter and apply criteria
        do_filter = input("Do you want to filter data? (y/n): ").strip().lower()
        selected_region = None
        min_amt = None
        if do_filter == 'y':
            selected_region = input("Enter region to filter: ").strip()
            min_amt_input = input("Enter minimum transaction amount: ").strip()
            min_amt = float(min_amt_input) if min_amt_input else None

        # 6. Validate transactions & 7. Display validation summary
        print("\n[4/10] Validating transactions...")
        valid_data, inv_count, summary = validate_and_filter(
            parsed_data, region=selected_region, min_amount=min_amt
        )
        print(f"✓ Valid: {len(valid_data)} | Invalid: {inv_count}\n")

        # 8. Perform all data analyses (Part 2 functions)
        print("[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_data)
        reg_analysis = region_wise_sales(valid_data)
        top_prods = top_selling_products(valid_data)
        cust_stats = customer_analysis(valid_data)
        print("✓ Analysis complete\n")

        # 9. Fetch products from API
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products\n")

        # 10. Enrich sales data with API info
        print("[7/10] Enriching sales data...")
        prod_mapping = create_product_mapping(api_products)
        enriched_data = enrich_sales_data(valid_data, prod_mapping)
        enriched_count = sum(1 for t in enriched_data if t.get('API_Match'))
        perc = (enriched_count / len(enriched_data)) * 100 if enriched_data else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_data)} transactions ({perc:.1f}%)\n")

        # 11. Save enriched data to file
        print("[8/10] Saving enriched data...")
        # (The logic to save is inside the enrich_sales_data function as per image 3.2)
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # 12. Generate comprehensive report
        print("[9/10] Generating report...")
        generate_sales_report(valid_data, enriched_data)
        print("✓ Report saved to: output/sales_report.txt\n")

        # 13. Print success message with file locations
        print("[10/10] Process Complete!")
        print("===========================================")

    except Exception as e:
        # Error Handling: Wrap entire process in try-except
        print(f"\nCRITICAL ERROR: {str(e)}")
        print("The program encountered an issue and could not complete the process.")

if __name__ == "__main__":
    main()