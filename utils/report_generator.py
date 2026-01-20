from datetime import datetime
import os

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report following the exact order
    and formatting requirements specified in Task 3.3.
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Helper function for currency formatting (e.g., ₹15,45,000.00)
    def fmt_curr(val):
        return f"₹{val:,.2f}"

    with open(output_file, 'w', encoding='utf-8') as f:
        # 1. HEADER
        f.write("===========================================\n")
        f.write("          SALES ANALYTICS REPORT           \n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {len(transactions)}\n")
        f.write("===========================================\n\n")

        # 2. OVERALL SUMMARY
        total_rev = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
        dates = [datetime.strptime(t['Date'], '%Y-%m-%d') for t in transactions]
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue:      {fmt_curr(total_rev)}\n")
        f.write(f"Total Transactions: {len(transactions)}\n")
        f.write(f"Average Order Value: {fmt_curr(total_rev / len(transactions))}\n")
        f.write(f"Date Range:         {min(dates).date()} to {max(dates).date()}\n\n")

        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Region':<10} {'Sales':<15} {'% of Total':<12} {'Transactions'}\n")
        
        reg_stats = {}
        for t in transactions:
            r = t['Region']
            rev = t['Quantity'] * t['UnitPrice']
            reg_stats[r] = reg_stats.get(r, {'s': 0, 'c': 0})
            reg_stats[r]['s'] += rev
            reg_stats[r]['c'] += 1
        
        # Sorted by sales amount descending
        for r, s in sorted(reg_stats.items(), key=lambda x: x[1]['s'], reverse=True):
            perc = (s['s'] / total_rev) * 100
            f.write(f"{r:<10} {fmt_curr(s['s']):<15} {perc:>6.2f}% {s['c']:>12}\n")
        f.write("\n")

        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Rank':<5} {'Product Name':<15} {'Qty Sold':<10} {'Revenue'}\n")
        
        p_stats = {}
        for t in transactions:
            name = t['ProductName']
            p_stats[name] = p_stats.get(name, {'q': 0, 'r': 0})
            p_stats[name]['q'] += t['Quantity']
            p_stats[name]['r'] += (t['Quantity'] * t['UnitPrice'])
            
        top_p = sorted(p_stats.items(), key=lambda x: x[1]['q'], reverse=True)[:5]
        for i, (name, data) in enumerate(top_p, 1):
            f.write(f"{i:<5} {name:<15} {data['q']:<10} {fmt_curr(data['r'])}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Rank':<5} {'Customer ID':<15} {'Total Spent':<15} {'Order Count'}\n")
        
        c_stats = {}
        for t in transactions:
            cid = t['CustomerID']
            c_stats[cid] = c_stats.get(cid, {'s': 0, 'c': 0})
            c_stats[cid]['s'] += (t['Quantity'] * t['UnitPrice'])
            c_stats[cid]['c'] += 1
            
        top_c = sorted(c_stats.items(), key=lambda x: x[1]['s'], reverse=True)[:5]
        for i, (cid, data) in enumerate(top_c, 1):
            f.write(f"{i:<5} {cid:<15} {fmt_curr(data['s']):<15} {data['c']}\n")
        f.write("\n")

        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Date':<12} {'Revenue':<15} {'Trans':<8} {'Unique Customers'}\n")
        
        d_stats = {}
        for t in transactions:
            d = t['Date']
            rev = t['Quantity'] * t['UnitPrice']
            d_stats[d] = d_stats.get(d, {'r': 0, 't': 0, 'u': set()})
            d_stats[d]['r'] += rev
            d_stats[d]['t'] += 1
            d_stats[d]['u'].add(t['CustomerID'])
            
        for d in sorted(d_stats.keys()):
            data = d_stats[d]
            f.write(f"{d:<12} {fmt_curr(data['r']):<15} {data['t']:<8} {len(data['u'])}\n")
        f.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 40 + "\n")
        peak_day = max(d_stats.items(), key=lambda x: x[1]['r'])[0]
        low_p = [n for n, d in p_stats.items() if d['q'] < 10]
        
        f.write(f"Best selling day: {peak_day}\n")
        f.write(f"Low performing products (<10 units): {', '.join(low_p) if low_p else 'None'}\n")
        
        # Avg transaction per region
        for r, s in reg_stats.items():
            f.write(f"Average transaction value ({r}): {fmt_curr(s['s']/s['c'])}\n")
        f.write("\n")

        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 40 + "\n")
        matches = [t for t in enriched_transactions if t.get('API_Match')]
        failed = list(set([t['ProductName'] for t in enriched_transactions if not t.get('API_Match')]))
        
        success_rate = (len(matches) / len(enriched_transactions)) * 100
        f.write(f"Total products enriched: {len(matches)}\n")
        f.write(f"Success rate percentage: {success_rate:.2f}%\n")
        f.write(f"List of products that couldn't be enriched: {', '.join(failed) if failed else 'None'}\n")