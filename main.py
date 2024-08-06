import json, os
from mapbox_data_download import download_mapbox_highres, ground_resolution, numpy_resolution
from dotenv import load_dotenv


if __name__ == "__main__":

    # Load environment variables from .env file
    load_dotenv()

    lat = 22.3185  # Latitude for KAUST
    lon = 39.1056  # Longitude for KAUST
    zoom = 19  # Zoom level
    map_style = 'mapbox/satellite-v9'  # Map style


    # Load the Mapbox project key from environment variables
    project_key = os.getenv('MAPBOX_KEY')

    # Download high-resolution image
    highres_image = download_mapbox_highres(lat, lon, zoom, map_style, project_key)

    # Save the image
    output_dir = 'mapbox_output'
    os.makedirs(output_dir, exist_ok=True)
    fname = f"mapbox_highres_{lat}_{lon}_zoom{zoom}"
    output_path = os.path.join(output_dir, f'{fname}.tif')
    highres_image.save(output_path)
    print(f"High-resolution image saved as {output_path}")

    # Calculate and print spatial resolution
    resolution = ground_resolution(lat, zoom, 512)
    print(f"Spatial resolution at latitude {lat}, zoom level {zoom}: {resolution:.2f} meters per pixel")

    # Convert to NumPy array and calculate resolution
    image_array, resolution = numpy_resolution(output_path)

    # Print the results
    print("Image array shape:", image_array.shape)
    print("Resolution (x_res, y_res):", resolution)

