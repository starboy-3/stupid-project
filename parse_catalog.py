from typing import List, Any

import requests
import json
from bs4 import BeautifulSoup

from model.pokemon import Pokemon
from parse_pokemon import parse_pokemon


def parse_catalog(url, parse_individual_page=False) -> List[Pokemon]:
    response = requests.get(url)
    products_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.findAll('li', {'class': 'product'})
        unique_ids = set()
        for product in products:
            link_element = product.find('a', class_='woocommerce-LoopProduct-link')
            product_link = link_element['href'] if link_element else None

            if product_link is not None and parse_individual_page:
                pokemon = parse_pokemon(product_link)
                if pokemon is not None:
                    products_data.append(pokemon)
            else:
                pokemon = parse_poke_from_catalog(product, product_link)

            if pokemon.id not in unique_ids:
                unique_ids.add(pokemon.id)
                products_data.append(pokemon)
    else:
        print(f'Failed to retrieve webpage: Status code {response.status_code}')

    return products_data

def parse_poke_from_catalog(product, product_link):
    title_element = product.find('h2', class_='woocommerce-loop-product__title')
    title = title_element.get_text(strip=True) if title_element else ''

    price_element = product.find('span', class_='woocommerce-Price-amount')
    price = price_element.get_text(strip=True) if price_element else None

    sku_element = product.find('a', class_='add_to_cart_button')
    sku = sku_element['data-product_sku'] if sku_element and 'data-product_sku' in sku_element.attrs else None

    id_element = product.find('a', class_='add_to_cart_button')
    product_id = id_element['data-product_id'] if id_element and 'data-product_id' in id_element.attrs else None

    image_element = product.find('img')
    image_url = image_element['src'] if image_element and 'src' in image_element.attrs else None
    return Pokemon(
        id=product_id,
        name=title,
        price=price,
        sku=sku,
        image_url=image_url,
        product_link=product_link,
        stock=None,
        categories=[],
        tags=[]
    )

def get_json_response(url, parse_individual_page) -> Any:
    pokemons = parse_catalog(url, parse_individual_page)
    pokemons_data = [pokemon.to_dict() for pokemon in pokemons]
    return json.dumps(pokemons_data, ensure_ascii=False, indent=2)
