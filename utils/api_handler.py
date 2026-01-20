import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100" # Requirement: use limit=100
    
    try:
        # Requirement: Handle connection errors with try-except
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Requirement: Print status message (success)
        print("Successfully fetched products from API.")
        
        return data.get('products', [])
        
    except requests.exceptions.RequestException as e:
        # Requirement: Print status message (failure)
        print(f"Failed to fetch products: {e}")
        
        # Requirement: Return empty list if API fails
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    
    Parameters: api_products from fetch_all_products()
    Returns: dictionary mapping product IDs to info
    """
    # Expected Output Format: { id: {'title': ..., 'category': ...}, ... }
    product_mapping = {}
    
    for product in api_products:
        p_id = product.get('id')
        product_mapping[p_id] = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }
        
    return product_mapping


