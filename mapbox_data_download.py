import math
import requests, rasterio
from PIL import Image
from io import BytesIO

def download_tile(x, y, z, map_style, api_key):
    url = f"https://api.mapbox.com/styles/v1/{map_style}/tiles/{z}/{x}/{y}?access_token={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception(f"Failed to retrieve tile: {response.status_code}")

def stitch_tiles(tiles, num_x, num_y, tile_size):
    width = num_x * tile_size
    height = num_y * tile_size
    stitched_image = Image.new('RGB', (width, height))

    for x in range(num_x):
        for y in range(num_y):
            stitched_image.paste(tiles[x][y], (x * tile_size, y * tile_size))

    return stitched_image

def download_mapbox_highres(lat, lon, zoom, map_style, api_key, num_tiles= 4, tile_size=512 ):
    # Convert latitude and longitude to tile coordinates
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x_tile = int((lon + 180.0) / 360.0 * n)
    y_tile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)

    # Download tiles
    tiles = []
    for x in range(x_tile, x_tile + num_tiles):
        tile_row = []
        for y in range(y_tile, y_tile + num_tiles):
            tile_row.append(download_tile(x, y, zoom, map_style, api_key))
        tiles.append(tile_row)

    # Stitch tiles
    stitched_image = stitch_tiles(tiles, num_tiles, num_tiles, tile_size)
    return stitched_image

def ground_resolution(latitude, zoom_level, tile_size=512):
    # Earth's equatorial circumference in meters
    equatorial_circumference = 40075016.686
    # Calculate ground resolution in meters per pixel
    resolution = (equatorial_circumference * math.cos(math.radians(latitude))) / (tile_size * 2 ** zoom_level)
    return resolution

def numpy_resolution(tif_path):
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
