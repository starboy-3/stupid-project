from parse_catalog import get_json_response

SCRAPE_ME_URL = 'https://scrapeme.live/shop/'

if __name__ == '__main__':
    print(get_json_response(SCRAPE_ME_URL, True))  # Configure call
