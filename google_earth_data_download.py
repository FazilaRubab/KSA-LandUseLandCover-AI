import ee, os, json
import numpy, rasterio
import geemap
from dotenv import load_dotenv


def download_google_earth_image(coordinates, scale,
                                collection_params,
                                sort_by_cloud_cover:bool = True,
                                filter_cloud_cover:bool = False,
                                viz_params=None,
                                output_dir=''):
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

        fname = f'{xMin}_{yMin}_{xMax}_{yMax}_{scale}'

        # Select the updated Landsat Collection 2 image collection
        collection = ee.ImageCollection(collection_params['collection_id']) \
            .filterDate(collection_params['start_date'], collection_params['end_date']) \
            .filterBounds(ksa_bounds)

        if sort_by_cloud_cover:
            collection = collection.sort("CLOUD_COVER")
            collection = collection.first()
            fname += '_scc'
        elif filter_cloud_cover:
            collection = collection.filterMetadata('CLOUD_COVER', 'less_than', collection_params['cloud_cover'])
            fname += '_mcc'
        else:
            collection= collection.first()

        print(f"Collection type: {type(collection)}")
        if isinstance(collection, ee.ImageCollection):
            print(f"Number of images in collection: {collection.size().getInfo()}")

            # Create a median composite from the image collection
            collection = collection.median()
            fname += '_median'

        if viz_params is not None:
            # Apply visualization parameters
            collection = collection.visualize(**viz_params)
            fname += '_vizparams'

        # Define the file path for the downloaded image
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{fname}.tif')

        # Download the image
        geemap.ee_export_image(collection, filename=output_path, scale=scale, region=ksa_bounds)

        # Print success messages
        print(f"Image successfully saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return fname
def tif_to_numpy_and_resolution(tif_path):
    """
    Convert a TIFF image to a NumPy array and calculate its resolution.

    Parameters:
    tif_path (str): Path to the TIFF image file.

    Returns:
    tuple: A tuple containing the NumPy array of the image and its resolution (x_res, y_res).
    """

    with rasterio.open(tif_path) as src:
        # Read the image into a NumPy array
        image_array = src.read(1)  # Read the first band into a 2D array

        # Get the resolution (pixel size)
        x_res, y_res = src.res


    return image_array, (x_res, y_res)

    """
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
    """

