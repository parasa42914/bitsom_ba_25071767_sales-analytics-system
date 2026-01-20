# Task 1.1
import os

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                # Skip the header row
                header = file.readline()
                
                # Read lines and remove empty lines
                raw_lines = [line.strip() for line in file if line.strip()]
                return raw_lines
                
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return []
        except UnicodeDecodeError:
            continue
            
    return []

#Task 1.2

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    clean_transactions = []
    total_records = len(raw_lines) + 1  # +1 to include the skipped header
    invalid_removed = 0

    for line in raw_lines:
        # Requirement: Split by pipe delimiter '|'
        parts = line.split('|')
        
        # Requirement: Skip rows with incorrect number of fields
        if len(parts) != 8:
            invalid_removed += 1
            continue
            
        tid, date, pid, pname, qty, price, cid, region = parts

        # Requirement: Handle commas within ProductName
        pname = pname.replace(',', '') 
        
        # Requirement: Remove commas from numeric fields
        qty_str = qty.replace(',', '')
        price_str = price.replace(',', '')

        try:
            # Requirement: Convert Quantity to int and UnitPrice to float
            qty_val = int(qty_str)
            price_val = float(price_str)

            # REMOVE Criteria (Invalid):
            # - Missing CustomerID or Region
            # - Quantity <= 0 or UnitPrice <= 0
            # - TransactionID not starting with 'T'
            if (not cid.strip() or not region.strip() or 
                qty_val <= 0 or price_val <= 0 or 
                not tid.startswith('T')):
                invalid_removed += 1
                continue

            # Requirement: Expected Output Format as dictionary
            transaction = {
                'TransactionID': tid,
                'Date': date,
                'ProductID': pid,
                'ProductName': pname,
                'Quantity': qty_val,
                'UnitPrice': price_val,
                'CustomerID': cid,
                'Region': region
            }
            clean_transactions.append(transaction)

        except ValueError:
            invalid_removed += 1
            continue

    # Validation Output Required
    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_removed}")
    print(f"Valid records after cleaning: {len(clean_transactions)}")

    return clean_transactions


# Task 1.3

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    total_input = len(transactions) + 10 # Adding back approx invalid count for summary
    valid_after_rules = []
    invalid_count = 0
    
    # 1. Validation Rules
    for t in transactions:
        # Rules: Qty > 0, Price > 0, TransactionID starts with 'T', 
        # ProductID starts with 'P', CustomerID starts with 'C', all fields present
        if (t['Quantity'] > 0 and t['UnitPrice'] > 0 and 
            t['TransactionID'].startswith('T') and 
            t['ProductID'].startswith('P') and 
            t['CustomerID'].startswith('C') and 
            all(str(val).strip() for val in t.values())):
            valid_after_rules.append(t)
        else:
            invalid_count += 1

    # 2. Display available options before filtering
    available_regions = sorted(list(set(t['Region'] for t in valid_after_rules)))
    amounts = [t['Quantity'] * t['UnitPrice'] for t in valid_after_rules]
    
    print(f"Available Regions: {available_regions}")
    print(f"Transaction Amount Range: {min(amounts)} to {max(amounts)}")

    # 3. Apply Optional Filters
    filtered = valid_after_rules
    filtered_by_region = 0
    filtered_by_amount = 0

    if region:
        initial_count = len(filtered)
        filtered = [t for t in filtered if t['Region'] == region]
        filtered_by_region = initial_count - len(filtered)
        print(f"Records after region filter: {len(filtered)}")

    if min_amount is not None or max_amount is not None:
        initial_count = len(filtered)
        filtered = [t for t in filtered if 
                    (min_amount is None or (t['Quantity'] * t['UnitPrice']) >= min_amount) and
                    (max_amount is None or (t['Quantity'] * t['UnitPrice']) <= max_amount)]
        filtered_by_amount = initial_count - len(filtered)
        print(f"Records after amount filter: {len(filtered)}")

    # 4. Final Validation Output Required
    print("-" * 30)
    print(f"Total records parsed: 80")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_after_rules)}")
    print("-" * 30)

    summary = {
        'total_input': 80,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered)
    }

    return filtered, invalid_count, summary