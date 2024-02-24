import requests
from bs4 import BeautifulSoup
import math
import folium
from folium.plugins import HeatMap
from secretsKeys import GOOGLE_MAPS_API_KEY


def extract_flat_data(url):
    flat_data = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        listings = soup.find_all('div', class_='col-sm-8 card_body')

        for listing in listings:
            flat_info = {}
            title_element = listing.find(class_='truncate_title noprint')
            rent_element = listing.find(class_='col-xs-3')
            meter_element = listing.find(class_='col-xs-3 text-right')
            location_element = listing.find('div', class_='col-xs-11').find('span')

            if title_element:
                title = title_element.text.strip()
                flat_info['title'] = title
            else:
                flat_info['title'] = "N/A"

            if rent_element and meter_element:
                rent = int(rent_element.text.strip().replace("€", "").strip())
                meter = int(meter_element.text.strip().split(" ")[0])  # delete m²
                if meter != 0:  # avoid division by zero
                    rent_per_meter = rent / meter
                    flat_info['rent_per_meter'] = str(rent_per_meter)

                else:
                    flat_info['rent_per_meter'] = "N/A"
            else:
                flat_info['rent_per_meter'] = "N/A"

            if location_element:
                location_text = location_element.text.strip()
                location_parts = location_text.split('|')
                if len(location_parts) > 1:
                    location = location_parts[2].strip()
                else:
                    location = "N/A"
                flat_info['location'] = location
            else:
                flat_info['location'] = "N/A"

            flat_data.append(flat_info)
    else:
        print("Bad request")
    return flat_data


def geocode_location(location):
    api_key = GOOGLE_MAPS_API_KEY
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location + " Dortmund"}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            return lat, lng
    print(f"Geocoding failed for {location}")
    return None, None


def create_heatmap(flat_data):
    dortmund_map = folium.Map(location=[51.5136, 7.4653], zoom_start=12)
    data = []
    for flat in flat_data:
        if flat.get('location') and flat.get('rent_per_meter'):
            location = flat['location']
            rent_per_meter_str = flat['rent_per_meter']
            try:
                rent_per_meter = float(rent_per_meter_str)
                if not math.isnan(rent_per_meter):
                    latitude, longitude = geocode_location(location)
                    if latitude is not None and longitude is not None:
                        # markers
                        folium.Marker([latitude, longitude], popup=f"Rent per meter: {rent_per_meter}").add_to(dortmund_map)
                        data.append([latitude, longitude, rent_per_meter])
            except ValueError:
                print(f"Ignoring flat with invalid rent per meter: {flat}")

    HeatMap(data).add_to(dortmund_map)
    dortmund_map.save("dortmund_heatmap.html")
    return dortmund_map


if __name__ == "__main__":
    url = ("https://www.wg-gesucht.de/1-zimmer-wohnungen-in-Dortmund.26.1.1.0.html?offer_filter=1&city_id=26"
           "&sort_order=0&noDeact=1&categories%5B%5D=1&rent_types%5B%5D=2")
    flats = extract_flat_data(url)
    create_heatmap(flats)
