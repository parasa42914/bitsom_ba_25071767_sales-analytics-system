#Task 2.1

def calculate_total_revenue(transactions):
    """Calculates total revenue from all transactions"""
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    """Analyzes sales by region"""
    total_revenue = calculate_total_revenue(transactions)
    stats = {}
    
    for t in transactions:
        reg = t['Region']
        rev = t['Quantity'] * t['UnitPrice']
        if reg not in stats:
            stats[reg] = {'total_sales': 0.0, 'transaction_count': 0}
        stats[reg]['total_sales'] += rev
        stats[reg]['transaction_count'] += 1
        
    for reg in stats:
        stats[reg]['percentage'] = round((stats[reg]['total_sales'] / total_revenue) * 100, 2)
        
    # Sort by total_sales descending
    return dict(sorted(stats.items(), key=lambda x: x[1]['total_sales'], reverse=True))

def top_selling_products(transactions, n=5):
    """Finds top n products by total quantity sold"""
    product_stats = {}
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        rev = qty * t['UnitPrice']
        if name not in product_stats:
            product_stats[name] = [0, 0.0] # [TotalQty, TotalRev]
        product_stats[name][0] += qty
        product_stats[name][1] += rev
        
    # Convert to list of tuples and sort
    result = [(name, stats[0], stats[1]) for name, stats in product_stats.items()]
    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]

def customer_analysis(transactions):
    """Updated to ensure product list is unique and sorted correctly"""
    stats = {}
    for t in transactions:
        cid = t['CustomerID']
        rev = t['Quantity'] * t['UnitPrice']
        if cid not in stats:
            stats[cid] = {'total_spent': 0.0, 'purchase_count': 0, 'products': set()}
        stats[cid]['total_spent'] += rev
        stats[cid]['purchase_count'] += 1
        stats[cid]['products'].add(t['ProductName'])
    
    # Requirement: Sort by total_spent descending
    sorted_customers = sorted(stats.items(), key=lambda x: x[1]['total_spent'], reverse=True)
    
    result = {}
    for cid, data in sorted_customers:
        result[cid] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(data['total_spent'] / data['purchase_count'], 2),
            'products_bought': sorted(list(data['products'])) # Requirement: unique list
        }
    return result

# Task 2.2

def daily_sales_trend(transactions):
    """Analyzes sales trends by date, sorted chronologically."""
    trend = {}
    for t in transactions:
        d = t['Date']
        rev = t['Quantity'] * t['UnitPrice']
        if d not in trend:
            trend[d] = {'revenue': 0.0, 'transaction_count': 0, 'customers': set()}
        trend[d]['revenue'] += rev
        trend[d]['transaction_count'] += 1
        trend[d]['customers'].add(t['CustomerID'])
    
    for d in trend:
        trend[d]['unique_customers'] = len(trend[d].pop('customers'))
        
    return dict(sorted(trend.items())) # Sort chronologically

def find_peak_sales_day(transactions):
    """Identifies the date with highest revenue."""
    trend = daily_sales_trend(transactions)
    peak_date = max(trend, key=lambda x: trend[x]['revenue'])
    return (peak_date, trend[peak_date]['revenue'], trend[peak_date]['transaction_count'])

# Task 2.3

def low_performing_products(transactions, threshold=10):
    """Identifies products with total quantity < threshold"""
    p_stats = {}
    for t in transactions:
        p = t['ProductName']
        if p not in p_stats: p_stats[p] = [0, 0.0]
        p_stats[p][0] += t['Quantity']
        p_stats[p][1] += (t['Quantity'] * t['UnitPrice'])
    
    # Filter by threshold and sort ascending
    result = [(name, q, r) for name, (q, r) in p_stats.items() if q < threshold]
    return sorted(result, key=lambda x: x[1])

# Task 3.2
import os
import re

def enrich_sales_data(transactions, product_mapping):
    """Enriches transaction data with API product information"""
    enriched_list = []
    
    for t in transactions:
        # Requirement: Extract numeric ID (P101 -> 101)
        numeric_id_match = re.search(r'\d+', t['ProductID'])
        p_id = int(numeric_id_match.group()) if numeric_id_match else None
        
        # Enrichment Logic
        if p_id in product_mapping:
            info = product_mapping[p_id]
            t.update({
                'API_Category': info['category'],
                'API_Brand': info['brand'],
                'API_Rating': info['rating'],
                'API_Match': True
            })
        else:
            # Handle ID doesn't exist
            t.update({
                'API_Category': None,
                'API_Brand': None,
                'API_Rating': None,
                'API_Match': False
            })
        enriched_list.append(t)
    
    # Save back to file
    save_enriched_data(enriched_list)
    return enriched_list

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """Saves enriched transactions back to file in pipe-delimited format"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName", "Quantity", 
        "UnitPrice", "CustomerID", "Region", "API_Category", "API_Brand", 
        "API_Rating", "API_Match"
    ]
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Include new columns in header
        f.write("|".join(headers) + "\n")
        
        for t in enriched_transactions:
            # Handle None values appropriately
            row = [
                str(t.get(h, "None")) for h in headers
            ]
            f.write("|".join(row) + "\n")