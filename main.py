import sys
from utils.file_handler import read_sales_data
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.data_processor import (
    parse_transactions, validate_and_filter, enrich_sales_data,
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day,
    low_performing_products
)
from utils.report_generator import generate_sales_report

def main():
    """Main execution function for the Sales Analytics System."""
    try:
        # 1. Print welcome message
        print("===========================================")
        print("          SALES ANALYTICS SYSTEM           ")
        print("===========================================\n")

        # 2. Read sales data file
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        print(f"✓ Successfully read {len(raw_lines)} transactions\n")

        # 3. Parse and clean transactions
        print("[2/10] Parsing and cleaning data...")
        parsed_data = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_data)} records\n")

        # 4 & 5. Filter options and application
        print("[3/10] Filter Options Available:")
        regions = sorted(list(set(t['Region'] for t in parsed_data)))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in parsed_data]
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}\n")

        do_filter = input("Do you want to filter data? (y/n): ").strip().lower()
        
        selected_region = None
        min_amt = None
        if do_filter == 'y':
            selected_region = input("Enter region name: ").strip()
            min_amt = float(input("Enter minimum transaction amount: ") or 0)

        # 6 & 7. Validate transactions and display summary
        print("\n[4/10] Validating transactions...")
        valid_data, inv_count, summary = validate_and_filter(
            parsed_data, region=selected_region, min_amount=min_amt
        )
        print(f"✓ Valid: {summary['final_count']} | Invalid: {summary['invalid']}\n")

        # 8. Perform all data analyses
        print("[5/10] Analyzing sales data...")
        # (Internal analysis calls to satisfy Part 2 requirements)
        calculate_total_revenue(valid_data)
        region_wise_sales(valid_data)
        top_selling_products(valid_data)
        customer_analysis(valid_data)
        daily_sales_trend(valid_data)
        print("✓ Analysis complete\n")

        # 9. Fetch products from API
        print("[6/10] Fetching product data from API...")
        api_data = fetch_all_products()
        prod_map = create_product_mapping(api_data)
        print(f"✓ Fetched {len(api_data)} products\n")

        # 10. Enrich sales data
        print("[7/10] Enriching sales data...")
        enriched_data = enrich_sales_data(valid_data, prod_map)
        match_count = sum(1 for t in enriched_data if t['API_Match'])
        match_perc = (match_count / len(enriched_data)) * 100
        print(f"✓ Enriched {match_count}/{len(enriched_data)} transactions ({match_perc:.1f}%)\n")

        # 11. Save enriched data
        print("[8/10] Saving enriched data...")
        # Assuming save_enriched_data helper exists in utils
        from utils.api_handler import save_enriched_data 
        save_enriched_data(enriched_data)
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # 12. Generate comprehensive report
        print("[9/10] Generating report...")
        generate_sales_report(valid_data, enriched_data)
        print("✓ Report saved to: output/sales_report.txt\n")

        # 13. Final success message
        print("[10/10] Process Complete!")
        print("===========================================")

    except FileNotFoundError as e:
        print(f"Critical Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()