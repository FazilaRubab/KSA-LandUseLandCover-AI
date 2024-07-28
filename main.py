import json
from google_earth_data_download import download_google_earth_image

if __name__ == "__main__":
    # Load configuration
    with open('config.json') as config_file:
        config = json.load(config_file)

    # Define input parameters
    coordinates = {
        'xMin': 39.1,
        'yMin': 22.3,
        'xMax': 39.2,
        'yMax': 22.41
    }
    scale = 30

    collection_params = {
        'collection_id': 'LANDSAT/LC08/C02/T1',
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'cloud_cover': 10
    }

    viz_params = {
        'bands': ['B4', 'B3', 'B2'],  # RGB bands
        'min': 90,
        'max': 100,
        'gamma': [1.5]  # Adjust gamma to enhance the image
    }

    output_dir = config['output_folder']

    # Call the function with the provided parameters
    download_google_earth_image(coordinates, scale, collection_params, viz_params, output_dir)
