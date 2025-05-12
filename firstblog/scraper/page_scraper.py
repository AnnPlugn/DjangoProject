import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Optional, Dict
from .constants import *

class PageScraper:
    def __init__(self):
        pass

    def _parse_offer_page(self, url: str) -> Optional[Dict]:
        try:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en'
            })
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            if "Captcha" in soup.text:
                print(f"CAPTCHA detected for {url}")
                return None

            data = {
                'floor': None,
                'floors_count': None,
                'rooms_count': None,
                'total_meters': None,
                'price': None,
                'year_of_construction': None,
                'living_meters': None,
                'kitchen_meters': None,
                'district': None,
                'street': None,
                'underground': None,
                'url': url
            }

            # Extract living area, total area, and kitchen area
            summary_items = soup.find_all('div', class_='a10a3f92e9--item--qJhdR')
            for item in summary_items:
                label = item.find('p', class_='a10a3f92e9--color_gray60_100--r_axa')
                value = item.find('p', class_='a10a3f92e9--color_text-primary-default--vSRPB')
                if label and value:
                    label_text = label.text.strip()
                    value_text = value.text.strip().replace('м²', '').replace(',', '.').replace('\xa0', '')
                    try:
                        if label_text == 'Жилая площадь':
                            data['living_meters'] = float(value_text)
                        elif label_text == 'Общая площадь':
                            data['total_meters'] = float(value_text)
                        elif label_text == 'Площадь кухни':
                            data['kitchen_meters'] = float(value_text)
                    except ValueError:
                        continue

            # Extract price
            price_tag = soup.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB',
                                  string=re.compile(r'\d+\s*\d*\s*₽'))
            if price_tag:
                price_text = price_tag.text.strip().replace('₽', '').replace('\xa0', '').replace(' ', '').strip()
                data['price'] = int(price_text)

            # Extract floor and total floors
            floor_info = soup.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB',
                                   string=re.compile(r'^\d+\s*из\s*\d+$'))
            if floor_info:
                floor_text = floor_info.text.strip()
                match = re.match(r'(\d+)\s*из\s*(\d+)', floor_text)
                if match:
                    data['floor'] = int(match.group(1))
                    data['floors_count'] = int(match.group(2))

            # Define rooms count
            def define_rooms_count(description):
                if "1-комн" in description or "Студия" in description:
                    rooms_count = 1
                elif "2-комн" in description:
                    rooms_count = 2
                elif "3-комн" in description or "евротрешка" in description:
                    rooms_count = 3
                elif "4-комн" in description:
                    rooms_count = 4
                elif "5-комн" in description:
                    rooms_count = 5
                else:
                    rooms_count = -1
                return rooms_count

            # Extract rooms count
            rooms_info = soup.find('h1', class_='a10a3f92e9--title--vlZwT')
            if rooms_info:
                rooms_text = rooms_info.text.strip()
                match = re.search(r'(\d+)-комн', rooms_text)
                if match:
                    data['rooms_count'] = int(match.group(1))
                else:
                    description = soup.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB')
                    if description:
                        description_text = description.text.strip()
                        data['rooms_count'] = define_rooms_count(description_text)
                    else:
                        data['rooms_count'] = -1
            else:
                rooms_info = soup.find('h1', class_='a10a3f92e9--title--mKRaW')
                if rooms_info:
                    rooms_text = rooms_info.text.strip()
                    match = re.search(r'(\d+)-комн', rooms_text)
                    if match:
                        data['rooms_count'] = int(match.group(1))
                    else:
                        description = soup.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB')
                        if description:
                            description_text = description.text.strip()
                            data['rooms_count'] = define_rooms_count(description_text)
                        else:
                            data['rooms_count'] = -1
                else:
                    data['rooms_count'] = -1

            # Extract year of construction
            year_label = soup.find('span', class_='a10a3f92e9--color_gray60_100--r_axa',
                                   string=re.compile(r'Год постройки|Год сдачи'))
            if year_label:
                year_info = year_label.find_next('span', class_='a10a3f92e9--color_text-primary-default--vSRPB')
                if year_info and re.match(r'^\d{4}$', year_info.text.strip()):
                    data['year_of_construction'] = int(year_info.text.strip())

            if data.get('year_of_construction') is None or data['year_of_construction'] >= 2026:
                completion_info = soup.find('div', class_='a10a3f92e9--text--eplgM')
                if completion_info:
                    status = completion_info.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB')
                    if status:
                        status_text = status.text.strip()
                        if status_text == 'Сдан':
                            data['is_completed'] = 1
                        else:
                            data['is_completed'] = 0
                            if data['year_of_construction'] is None:
                                data['year_of_construction'] = datetime.now().year
                    else:
                        data['is_completed'] = -1
                else:
                    data['is_completed'] = -1
            else:
                data['is_completed'] = 1

            # Extract address (district, street)
            address_items = soup.find_all('a', class_='a10a3f92e9--address--SMU25', attrs={'data-name': 'AddressItem'})
            if len(address_items) >= 4:
                data['district'] = address_items[2].text.strip()
                data['street'] = address_items[3].text.strip()

            # Extract metro and time to metro
            underground_item = soup.find('li', class_='a10a3f92e9--underground--pjGNr')
            if underground_item:
                underground_name = underground_item.find('a', class_='a10a3f92e9--underground_link--VnUVj')
                underground_time = underground_item.find('span', class_='a10a3f92e9--underground_time--YvrcI')
                if underground_name:
                    data['underground'] = underground_name.text.strip()
                if underground_time:
                    data['min_to_metro'] = underground_time.text.strip()

            return data

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None
        except Exception as e:
            print(f"Ошибка при парсинге {url}: {e}")
            return None