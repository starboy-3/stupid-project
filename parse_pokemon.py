from typing import Optional

import requests
from bs4 import BeautifulSoup

from model.pokemon import Pokemon

def parse_pokemon(product_link) -> Optional[Pokemon]:
    response = requests.get(product_link)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find('h1').text.strip()
    price = soup.find(class_='woocommerce-Price-amount').text.strip()

    stock_info = soup.find(text=lambda x: "in stock" in x.lower())
    stock = int(''.join(filter(str.isdigit, stock_info))) if stock_info else 0

    sku = soup.find('span', class_='sku').text.strip()

    categories = [a.text for a in soup.find('span', class_='posted_in').find_all('a')]

    tags = [a.text for a in soup.find('span', class_='tagged_as').find_all('a')]

    product_div = soup.find('div', id=lambda x: x and x.startswith('product-'))
    product_id = product_div['id'].split('-')[1] if product_div and '-' in product_div['id'] else None

    description_div = soup.find('div', class_='woocommerce-Tabs-panel--description')
    description = ""
    if description_div:
        description_p = description_div.find('p')
        if description_p:
            description = description_p.get_text(strip=True)

    return Pokemon(
        id=product_id,
        name=name,
        price=price,
        stock=stock,
        sku=sku,
        categories=categories,
        tags=tags,
        description=description,
        product_link=product_link
    )