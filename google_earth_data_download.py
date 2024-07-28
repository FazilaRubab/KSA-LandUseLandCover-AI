import ee
import os
import geemap
from dotenv import load_dotenv


def download_google_earth_image():
    # Load environment variables from .env file
    load_dotenv()

    # Authenticate and initialize the Earth Engine API
    ee.Initialize(project='animated-verve-430410-p5')

    try:
        # Define a region of interest (example coordinates for a specific area in Saudi Arabia)
        xMin, yMin, xMax, yMax = 39.1, 22.3, 39.2, 22.41
        scale = 30
        ksa_bounds = ee.Geometry.Rectangle([xMin, yMin, xMax, yMax])  # xMin

        # Select the updated Landsat Collection 2 image collection
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1') \
            .filterDate('2023-01-01', '2023-12-31') \
            .filterBounds(ksa_bounds) \
            .filterMetadata('CLOUD_COVER', 'less_than', 10)

        print(f"Collection type: {type(collection)}")
        if isinstance(collection, ee.ImageCollection):
            print(f"Number of images in collection: {collection.size().getInfo()}")

        # Create a median composite from the image collection
        composite = collection.median()

        # Enhance the image using visualization parameters
        viz_params = {
            'bands': ['B4', 'B3', 'B2'],  # RGB bands
            'min': 90,
            'max': 100,
            'gamma': [1.5]  # Adjust gamma to enhance the image
        }

        # Apply visualization parameters
        composite_visualized = composite.visualize(**viz_params)

        # Define the file path for the downloaded image
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{xMin}_{yMin}_{xMax}_{yMax}_{scale}.tif')

        # Download the image
        geemap.ee_export_image(composite_visualized, filename=output_path, scale=scale, region=ksa_bounds)

        # Print success messages
        print(f"Image successfully saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

