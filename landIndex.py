import ee
import numpy as np
import requests
import io
import cv2
from icecream import ic
# import folium
# from folium import plugins
from IPython.display import Image

def getIndex(lat, lon, startDate, endDate, landIndexDataset, indexName, scale=30, palette=['brown', 'white', 'green'], bufferZone=1e4):
    ## a collection of `ee.images`
    lst = ee.ImageCollection(landIndexDataset)

    # Selection of appropriate bands and dates for LST.
    lst = lst.select(indexName).filterDate(startDate, endDate)

    # Define the point of interest
    u_poi = ee.Geometry.Point(lon, lat)

    lst_urban_point = lst.mean().sample(u_poi, scale).first().get(indexName).getInfo()
    ic(lst_urban_point)
    # Define a region of interest with a buffer zone of 1000 km around Lyon.
    roi = u_poi.buffer(bufferZone)

    lst_img = lst.mean()

    # Create a URL to the styled image for a region around France.
    url = lst_img.getThumbUrl({
        'min': -1, 'max': 1, 'dimensions': 1024, 'region': roi,
        'palette': palette})
    print('\nPlease wait while the thumbnail loads, it may take a moment...')
    print(url)

    # Display the thumbnail land surface temperature in France.
    # Image(url=url)
    url = lst_img.getDownloadUrl({
        'bands': [indexName],
        'region': roi,
        'scale': scale,
        'format': 'NPY',
    })
    response = requests.get(url)
    data = np.load(io.BytesIO(response.content))
    cv2.imshow(indexName, data.astype(np.float32))
    cv2.waitKey(0)

    return url
