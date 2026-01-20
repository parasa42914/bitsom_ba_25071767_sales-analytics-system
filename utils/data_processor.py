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
    """Analyzes customer purchase patterns"""
    cust_stats = {}
    for t in transactions:
        cid = t['CustomerID']
        rev = t['Quantity'] * t['UnitPrice']
        pname = t['ProductName']
        
        if cid not in cust_stats:
            cust_stats[cid] = {'total_spent': 0.0, 'purchase_count': 0, 'products': set()}
        
        cust_stats[cid]['total_spent'] += rev
        cust_stats[cid]['purchase_count'] += 1
        cust_stats[cid]['products'].add(pname)
        
    final_stats = {}
    for cid, data in cust_stats.items():
        final_stats[cid] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(data['total_spent'] / data['purchase_count'], 2),
            'products_bought': sorted(list(data['products'])) # Requirement: Unique products
        }
        
    # Sort by total_spent descending
    return dict(sorted(final_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True))

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
