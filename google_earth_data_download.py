import ee
import os
import geemap
from dotenv import load_dotenv


def download_google_earth_image(coordinates, scale, collection_params, viz_params, output_dir):
    # Load environment variables from .env file
    load_dotenv()

    # Load the Earth Engine project key from environment variables
    project_key = os.getenv('EE_PROJECT_KEY')
    if not project_key:
        raise ValueError("The Earth Engine project key is not set. Please check your .env file.")

    # Authenticate and initialize the Earth Engine API
    ee.Initialize(project=project_key)

    try:
        # Define a region of interest
        xMin, yMin, xMax, yMax = coordinates['xMin'], coordinates['yMin'], coordinates['xMax'], coordinates['yMax']
        ksa_bounds = ee.Geometry.Rectangle([xMin, yMin, xMax, yMax])

        # Select the updated Landsat Collection 2 image collection
        collection = ee.ImageCollection(collection_params['collection_id']) \
            .filterDate(collection_params['start_date'], collection_params['end_date']) \
            .filterBounds(ksa_bounds) \
            .filterMetadata('CLOUD_COVER', 'less_than', collection_params['cloud_cover'])

        print(f"Collection type: {type(collection)}")
        if isinstance(collection, ee.ImageCollection):
            print(f"Number of images in collection: {collection.size().getInfo()}")

        # Create a median composite from the image collection
        collection = collection.median()

        # Apply visualization parameters
        collection = collection.visualize(**viz_params)

        # Define the file path for the downloaded image
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{xMin}_{yMin}_{xMax}_{yMax}_{scale}.tif')

        # Download the image
        geemap.ee_export_image(collection, filename=output_path, scale=scale, region=ksa_bounds)

        # Print success messages
        print(f"Image successfully saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
