import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Open NDVI file
file_path = "bloomwatch/test_ndvi.tif"  
with rasterio.open(file_path) as src:
    ndvi = src.read(1)  # read first band

# Mask invalid values
ndvi = np.where(ndvi == src.nodata, np.nan, ndvi)

# Plot
plt.imshow(ndvi, cmap='RdYlGn')
plt.colorbar(label='NDVI')
plt.title("NDVI Map")
plt.show()
