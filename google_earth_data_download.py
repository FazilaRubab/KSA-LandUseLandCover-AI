import ee
import os
import geemap

# Authenticate and initialize the Earth Engine API
ee.Initialize(project='animated-verve-430410-p5')

# Define a region of interest (example coordinates for a specific area in Saudi Arabia)
#xMin, yMin, xMax, yMax= 39.104992, 22.300943, 39.132402, 22.323089 # Adjust coordinates as needed
xMin, yMin, xMax, yMax = 39.1, 22.3, 39.2, 22.41
scale = 30
ksa_bounds = ee.Geometry.Rectangle([xMin, yMin, xMax, yMax])  # xMin
# Select the updated Landsat Collection 2 image collection
collection = ee.ImageCollection('LANDSAT/LC08/C02/T1') \
    .filterDate('2023-01-01', '2023-12-31') \
    .filterBounds(ksa_bounds) \
    .filterMetadata('CLOUD_COVER', 'less_than', 10)

"""
collection1 = ee.ImageCollection('LANDSAT/LC08/C02/T1')
collection = collection1.filterDate('2023-01-01', '2023-12-31')
"""

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
output_path = os.path.join(output_dir, f'{xMin}_{yMin}_{xMax}_{yMax}_{scale}.tif')

# Download the image
out= geemap.ee_export_image(composite_visualized, filename=output_path,
                            scale=scale, region=ksa_bounds)
print(type(out))

print(f"Done")

