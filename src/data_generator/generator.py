import uuid
from datetime import datetime, timedelta

from faker import Faker
from .custom_providers import *


faker = Faker(use_weighting=True)
faker.add_provider(GenderProvider)
faker.add_provider(MembershipProvider)
faker.add_provider(EmailDomainProvider)
faker.add_provider(EcommerceProvider)


def generate_stores(n=3):
    output = []
    for _ in range(n):
        store = dict()
        
        # storeid
        store["id"] = uuid.uuid4().hex

        # storename
        store['name'] = ' '.join(faker.words(nb=2)).strip('.').title()
        # address
        store['address'] = faker.street_address()
        # phone
        store['phone'] = faker.phone_number()
        # store
        store['email'] = faker.email()
        
        output.append(store)
    return output


def generate_customers(n=10):
    output = []
    for _ in range(n):
        customer = dict()
        # id
        customer['customer_id'] = uuid.uuid4().hex
        # gender
        gender = faker.gender()
        customer['gender'] = gender
        # name
        first_name = faker.first_name_male() if gender == 'male' else faker.first_name_female()
        last_name = faker.last_name_male() if gender == 'male' else faker.last_name_female()
        customer['first_name'] = first_name
        customer['last_name'] = last_name
        # email
        company = faker.company().split()[0].strip(',')
        customer['email'] = f"{first_name}_{last_name}@{company}.{faker.domain()}".lower()
        # yob
        customer['yob'] = faker.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y-%m-%d')
        # phone number
        customer['phone_number'] = faker.phone_number()
        # profile
        customer['job'] = faker.job()
        # address
        customer['address'] = faker.street_address()
        # first_transaction
        customer['first_transaction'] = faker.past_date(start_date='-14d').strftime('%Y-%m-%d')
        # membership
        customer['membership'] = faker.membership()

        output.append(customer)

    return output


def generate_staffs(store_data: dict, n=2):
    output = []
    for _ in range(n):
        staff = dict()
        # id
        staff['staff_id'] = uuid.uuid4().hex
        # gender
        gender = faker.gender()
        staff['gender'] = gender
        # name
        first_name = faker.first_name_male() if gender == 'male' else faker.first_name_female()
        last_name = faker.last_name_male() if gender == 'male' else faker.last_name_female()
        staff['first_name'] = first_name
        staff['last_name'] = last_name
        # store
        staff['store_id'] = random.choice([k["id"] for k in store_data])

        output.append(staff)
    
    return output


def generate_products(n=10):
    output = []
    for _ in range(n):
        product = dict()
        # id
        product['product_id'] = uuid.uuid4().hex
        # product name
        product['category'], product['product_name'] = faker.product_name()
        # product price
        product['unit_price'] = faker.product_price()

        output.append(product)

    return output


def generate_transactions(
        stores: list, 
        customers: list, 
        staffs: list, 
        products: list, 
        transaction_range: list,
        max_item_per_transaction: int = 2, 
        max_quantity_per_item: int = 2, 
        n: int =10,
    ):    
    def filter_dict(input_dict, filter_keys: list):
        """
        Filters a dictionary to include only specified keys.
        """
        return {key: input_dict[key] for key in filter_keys if key in input_dict}

    def append_to_transaction(transaction, source, selected_columns, key_mapping):
        """
        Updates the transaction with filtered data from a source.
        
        Args:
            transaction (dict): The transaction being built.
            source (list): The list to randomly choose an entry from.
            selected_columns (list): The columns to filter from the source.
            key_mapping (dict): Mapping of source keys to transaction keys.
        """
        data = filter_dict(random.choice(source), selected_columns)
        transaction.update({key_mapping[k]: v for k, v in data.items()})
        return transaction
    
    def random_timestamp(start: datetime, end: datetime):
        """
        Generates a random timestamp between two datetime objects.
        The end datetime is exclusive.
        """
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds() - 1))
        return start + timedelta(seconds=random_seconds)


    # Validate and parse the transaction_range
    if len(transaction_range) != 2 or not all(transaction_range):
        raise ValueError("transaction_range must be a list with two non-empty date strings [start_date, end_date].")

    try:
        start_date = datetime.strptime(transaction_range[0], "%Y-%m-%d")
        end_date = datetime.strptime(transaction_range[1], "%Y-%m-%d")
    except ValueError as e:
        raise ValueError("Dates in transaction_range must be in 'YYYY-MM-DD' format.")

    if start_date >= end_date:
        raise ValueError("Start date must be earlier than end date.")

    transactions = []
    
    for _ in range(n):
        transaction = {
            'transaction_id': uuid.uuid4().hex,
            "utc_dt": random_timestamp(start_date, end_date).isoformat()
        }

        # Append store details
        transaction = append_to_transaction(
            transaction,
            stores,
            selected_columns=["name"],
            key_mapping={"name": "store"}
        )

        # Append customer details
        transaction = append_to_transaction(
            transaction,
            customers,
            selected_columns=["customer_id"],
            key_mapping={"customer_id": "customer_id"}
        )

        
        # Append staff details
        transaction = append_to_transaction(
            transaction,
            staffs,
            selected_columns=["staff_id"],
            key_mapping={"staff_id": "staff_id"}
        )


        # Append product details
        items = []
        purchased_items_number = random.randint(1, max_item_per_transaction)

        for item_order in range(1, purchased_items_number + 1): # Start item_order from 1
            product = random.choice(products)
            data = filter_dict(product, ["product_id"])
            quantity = random.randint(1, max_quantity_per_item)

            item = {
                "item_order": item_order, 
                "item_id": data["product_id"],  # Only product_id is kept
                "quantity": quantity,  # Quantity purchased
            }

            items.append(item)

        transaction.update({
            "transaction_items": items,
        })

        transactions.append(transaction)

    return transactions