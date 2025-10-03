import ee
import json
import datetime

# Initialize Earth Engine with your project ID
ee.Initialize(project='bloomwatch-gee')

# Load regions
with open("regions.json") as f:
    regions = json.load(f)

# Date range
start_date = '2025-01-01'
end_date = '2025-01-31'

# Function to calculate NDVI
def add_ndvi(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return image.addBands(ndvi)

# Loop through all regions
for region_name, region_data in regions.items():
    print(f"Processing region: {region_name}")
    
    ee_region = ee.Geometry.Polygon(region_data['coordinates'])
    
    # Load Sentinel-2 images
    collection = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(ee_region) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(add_ndvi)
    
    ndvi_image = collection.select('NDVI').median()
    
    # Export to Drive
    task = ee.batch.Export.image.toDrive(
        image=ndvi_image,
        description=f'NDVI_{region_name}',
        folder='BloomWatch',
        fileNamePrefix=f'NDVI_{region_name}',
        region=ee_region.getInfo()['coordinates'],
        scale=10,
        crs='EPSG:4326'
    )
    task.start()
    print(f"NDVI export started for {region_name}. Check Google Drive -> BloomWatch folder.")
