import json
import pandas as pd
import os

from src.faker.generator import *
from dotenv import load_dotenv

env = load_dotenv()


if __name__ == "__main__":
    # Get env
    catalog     = os.getenv("CATALOG")
    raw_schema  = os.getenv("RAW_SCHEMA")

    # generate transactions
    store_data          = generate_stores(20)
    customer_data       = generate_customers(100)
    staff_data          = generate_staffs(store_data, 12)
    product_data        = generate_products(35)
    transaction_data    = generate_transactions(
                            store_data, 
                            customer_data, 
                            staff_data, 
                            product_data, 
                            transaction_range=["2024-11-01", "2024-11-08"],
                            max_item_per_transaction=5,
                            max_quantity_per_item=2,
                            n=500
                        )
    

    # Volume paths
    volumn_json_files   = f"storage/uc_{catalog}/{raw_schema}/_volumes/json_files"
    volumn_txt_files    = f"storage/uc_{catalog}/{raw_schema}/_volumes/txt_files"
    parquet_files       = "source"

    
    pd.DataFrame(customer_data).to_csv(
        os.path.join(volumn_txt_files, "customer_data.csv"), 
        index=False
    )
    
    pd.DataFrame(staff_data).to_csv(
        os.path.join(volumn_txt_files, "staff_data.csv"),
        index=False
    )

    pd.DataFrame(store_data).to_csv(
        os.path.join(volumn_txt_files, "store_data.csv"),
        index=False
    )

    # Save product_data as Parquet
    pd.DataFrame(product_data).to_parquet(
        os.path.join(parquet_files, "product_data.parquet"), 
        index=False,
    )

    # Save transaction_data as JSON
    with open(os.path.join(volumn_json_files, 'transaction_data.json'), 'w') as json_file:
        json.dump(transaction_data, json_file, indent=4)
