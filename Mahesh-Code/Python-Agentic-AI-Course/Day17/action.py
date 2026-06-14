import json
import os
FILE_NAME = "products.json"

# Create the json file if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'w') as f:
        json.dump([], f)


def read_products():
    with open(FILE_NAME, 'r') as f:
        return json.load(f)
    
def write_products(products):
    with open(FILE_NAME, 'w') as f:
        json.dump(products, f, indent=4)