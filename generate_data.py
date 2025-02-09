import json
import pandas as pd
import os
import yaml
from pathlib import Path

from src.utils import parse_yaml
from src.data_generator.generator import (
    generate_stores,
    generate_customers,
    generate_staffs,
    generate_products,
    generate_transactions
)
from dotenv import load_dotenv

# Load environment variables
env = load_dotenv()


if __name__ == "__main__":
    config = parse_yaml("config", "generate_data.yaml")


    # Generate data using configuration from YAML file
    store_data = generate_stores(n=config['store']['number_of_records'])
    customer_data = generate_customers(n=config['customer']['number_of_records'])
    staff_data = generate_staffs(store_data, n=config['staff']['number_of_records'])
    product_data = generate_products(n=config['product']['number_of_records'])
    transaction_data = generate_transactions(
        store_data,
        customer_data,
        staff_data,
        product_data,
        transaction_range=config['transaction']['transaction_range'],
        max_item_per_transaction=config['transaction']['max_item_per_transaction'],
        max_quantity_per_item=config['transaction']['max_quantity_per_item'],
        n=config['transaction']['number_of_records']
    )
    

    # Volume paths
    data_folder          = "data_files"
    os.makedirs(data_folder, exist_ok=True)

    
    pd.DataFrame(customer_data).to_csv(
        os.path.join(data_folder, "customer_data.csv"), 
        index=False
    )
    
    pd.DataFrame(staff_data).to_csv(
        os.path.join(data_folder, "staff_data.csv"),
        index=False
    )

    pd.DataFrame(store_data).to_csv(
        os.path.join(data_folder, "store_data.csv"),
        index=False
    )

    # Save product_data as Parquet
    pd.DataFrame(product_data).to_parquet(
        os.path.join(data_folder, "product_data.parquet"), 
        index=False,
    )

    # Save transaction_data as JSON
    with open(os.path.join(data_folder, 'transaction_data.json'), 'w') as json_file:
        json.dump(transaction_data, json_file, indent=4)

    print("Data generation completed!.")
