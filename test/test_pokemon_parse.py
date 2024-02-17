import unittest
from unittest.mock import patch
from parse_pokemon import parse_pokemon


class TestParsePokemonPage(unittest.TestCase):
    @patch('parse_pokemon.requests.get')
    def test_successful_parse(self, mock_get):
        with open('resources/ok_pokemon_response.html', 'r', encoding='utf-8') as file:
            mock_get.return_value.ok = True
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = file.read()

        result = parse_pokemon("http://fakeurl.com/pokemon")

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Bulbasaur")
        self.assertEqual(result.sku, "4391")

    @patch('parse_pokemon.requests.get')
    def test_failed_parse(self, mock_get):
        mock_get.return_value.ok = False
        mock_get.return_value.status_code = 404
        result = parse_pokemon("http://fakeurl.com/nonexistent-pokemon")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
