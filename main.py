import json, os
from google_earth_data_download import download_google_earth_image
from google_earth_data_download import tif_to_numpy_and_resolution


if __name__ == "__main__":
    # Load configuration
    with open('config.json') as config_file:
        config = json.load(config_file)

    # Define input parameters
    coords = {
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
    tif_path = download_google_earth_image(coords, scale, collection_params,
                                viz_params=None, #viz_params,
                                output_dir=output_dir)

    tif_path = os.path.join(output_dir, f"{tif_path}.tif")

    # Convert TIFF to NumPy array and calculate resolution
    image_array, resolution = tif_to_numpy_and_resolution(tif_path)

    # Print the results
    print("Image array shape:", image_array.shape)
    print("Resolution (x_res, y_res):", resolution)