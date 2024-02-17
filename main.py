import json
import os

from parse_catalog import get_json_response

SCRAPE_ME_URL = 'https://scrapeme.live/shop/'

def write_json_to_file(data, filename='result.json'):
    if os.path.exists(filename):
        base, extension = os.path.splitext(filename)
        i = 1
        new_filename = f"{base}_{i}{extension}"

        while os.path.exists(new_filename):
            i += 1
            new_filename = f"{base}_{i}{extension}"

        filename = new_filename

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    response_data = get_json_response(url=SCRAPE_ME_URL, parse_individual_page=True)
    write_json_to_file(response_data)
