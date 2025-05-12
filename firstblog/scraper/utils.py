import re
from .page_scraper import PageScraper
from .constants import BASE_URL, METRO_STATIONS, DEFAULT_POSTFIX_PATH

scraper = PageScraper()

def is_valid_url(url):
    """Check if the input is a valid URL."""
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def extract_property_data(url):
    """Extract property data from the URL."""
    data = scraper._parse_offer_page(url)
    return data

def build_url(deal_type: str, start_page: int, rooms: list[int], metro_stations: list[str] = None) -> str:
    """Build a URL for querying real estate listings."""
    location_id = 1  # Moscow region ID (replace with actual value)

    url = f"{BASE_URL}{DEFAULT_POSTFIX_PATH}"
    params = {
        'deal_type': deal_type,
        'offer_type': 'flat',
        'region': location_id,
        'p': start_page,
        'with_neighbors': 0,
        'engine_version': 2
    }

    for room in rooms:
        params[f'room{room}'] = 1

    if metro_stations:
        for i, station_name in enumerate(metro_stations):
            station_id = None
            for city_stations in METRO_STATIONS.values():
                for station in city_stations:
                    if station[0].lower() == station_name.lower():
                        station_id = station[1]
                        break
                if station_id:
                    break
            if station_id:
                params[f'metro[{i}]'] = station_id

    return f"{url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"