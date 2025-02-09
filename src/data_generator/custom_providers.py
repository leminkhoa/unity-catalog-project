'''
This file contains custom providers for the Faker library. The providers are used to generate fake data for the data generator script. The `GenderProvider` class generates
'''

import os
import random
from pathlib import Path
from faker.providers import BaseProvider
from src import utils


class GenderProvider(BaseProvider):
    choices = ['male', 'female']
    prob = [0.5, 0.5]

    def gender(self):
        """
        Select a membership type based on predefined probabilities.

        Returns:
            str: The selected membership type.
        """
        return random.choices(self.choices, self.prob)[0]


class MembershipProvider(BaseProvider):
    choices = ['standard', 'gold', 'platinum', 'diamond']
    prob = [0.4, 0.3, 0.2, 0.1]

    def membership(self):
        """
        Select a membership type based on predefined probabilities.

        Returns:
            str: The selected membership type.
        """
        return random.choices(self.choices, self.prob)[0]


class EmailDomainProvider(BaseProvider):
    choices = ['com', 'org', 'gov']

    def domain(self):
        """
        Select a random email domain.

        Returns:
            str: The selected email domain.
        """
        return random.choice(self.choices)


class EcommerceProvider(BaseProvider):
    product_data = utils.parse_yaml(
                    folder=str(Path(os.path.dirname(__file__)) / 'config'),
                    file='ecommerce_provider.yml')
    
    def product_name(self):
        """
        Generate a fake product name and category.

        Returns:
            str: The generated product name.
        """
        category_pool = self.product_data['category'].keys()
        category = self.random_element(category_pool)
        product = self.random_element(self.product_data['category'][category])
        adjective = self.random_element(self.product_data['adjective'])
        material = self.random_element(self.product_data['material'])
        color = self.random_element(self.product_data['color'])

        choices = [
            " ".join([adjective, product]),
            " ".join([material, product]),
            " ".join([color, product]),
            " ".join([adjective, color, material, product]),
        ]

        return category, random.choices(choices, k=1)[0]

    def product_price(self, as_int: bool = True):
        n = self.random_int(min=10, max=500)
        return round(n, 2) if as_int else n / 100
