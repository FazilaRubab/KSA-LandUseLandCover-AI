import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

output_folder = config['output_folder']
google_maps_config = config['google_maps']

def download_google_maps_image(lat, lon, zoom, width, height):
    url = google_maps_config['url_template'].format(
        lat=lat, lng=lon, zoom=zoom, width=width, height=height, api_key=google_maps_api_key
    )

    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(output_folder, f"google_maps_{lat}_{lon}_{zoom}.png")
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved: {file_path}")
    else:
        print(f"Failed to download image from Google Maps for coordinates ({lat}, {lon}) at zoom {zoom}")
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Example coordinates
coordinates = [
    (24.7136, 46.6753),  # Riyadh
    (21.4858, 39.1925),  # Jeddah
    (24.6877, 46.7219)   # Example coordinate
]

# Download images for each coordinate
for lat, lon in coordinates:
    download_google_maps_image(lat, lon, 12, 600, 600)
