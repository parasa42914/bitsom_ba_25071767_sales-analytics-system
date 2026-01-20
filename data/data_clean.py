import pandas as pd
import io

def clean_transaction_data(raw_text):
    # Step 1: Parse the data using '|' delimiter
    df = pd.read_csv(io.StringIO(raw_text), sep='|')
    total_parsed = len(df)
    
    # Step 2: CLEAN and KEEP formatting
    # Remove commas in ProductName
    df['ProductName'] = df['ProductName'].str.replace(',', ' ')
    
    # Remove commas in UnitPrice and convert to float
    df['UnitPrice'] = df['UnitPrice'].astype(str).str.replace(',', '').astype(float)
    
    # Step 3: Identify REMOVE (Invalid) criteria
    # Missing CustomerID or Region
    mask_missing = (df['CustomerID'].isna() | (df['CustomerID'].astype(str).str.strip() == '') | 
                    df['Region'].isna() | (df['Region'].astype(str).str.strip() == ''))
    
    # Quantity <= 0 or UnitPrice <= 0
    mask_qty_price = (df['Quantity'] <= 0) | (df['UnitPrice'] <= 0)
    
    # TransactionID not starting with 'T'
    mask_tid = ~df['TransactionID'].str.startswith('T', na=False)
    
    # Combine all removal masks
    invalid_mask = mask_missing | mask_qty_price | mask_tid
    
    # Final dataframes
    df_valid = df[~invalid_mask].copy()
    invalid_count = invalid_mask.sum()
    valid_count = len(df_valid)
    
    # Validation Output Required
    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {valid_count}")
    
    return df_valid

# Example usage:
# cleaned_data = clean_transaction_data(your_raw_text_string)