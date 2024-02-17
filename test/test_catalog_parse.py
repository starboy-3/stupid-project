import unittest
from unittest.mock import patch
from parse_catalog import parse_catalog

class ParserTestCase(unittest.TestCase):
    @patch('parse.requests.get')
    def test_successful_parsing(self, mocked_get):
        with open('resources/ok_catalog_response.html', 'r') as file:
            mocked_get.return_value.ok = True
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.text = file.read()

        pokemons = parse_catalog("mock_url")
        pokemon_by_sku = dict()
        for pokemon in pokemons:
            pokemon_by_sku[pokemon.sku] = pokemon

        self.assertTrue(len(pokemons), 7)
        bulbasaur = pokemon_by_sku.get('4391')
        self.assertEqual("759", bulbasaur.id)
        self.assertEqual("Bulbasaur", bulbasaur.name)

    @patch('parse.requests.get')
    def test_failed_retrieval(self, mocked_get):
        mocked_get.return_value.ok = False
        mocked_get.return_value.status_code = 404

        result = parse_catalog("mock_url")
        self.assertEqual(0, len(result))

if __name__ == 'main':
    unittest.main()