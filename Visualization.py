import folium
from folium.plugins import MarkerCluster, HeatMap
import geopandas as gpd
import pandas as pd

pd.set_option('display.width', 130)
pd.set_option('display.max_columns', 130)
pd.set_option('display.max_colwidth', 130)

# Load collisions data
collisions = pd.read_csv('Cyclists.csv')
collisions = collisions[collisions['YEAR'] >= 2018]

# Create a map centered around Toronto (adjust the coordinates as needed)
toronto_map = folium.Map(location=[43.70, -79.42], zoom_start=11)

def heatmap():
    # Create a HeatMap layer for collisions
    heat_data = [[row['LATITUDE'], row['LONGITUDE']] for index, row in collisions.iterrows()]
    HeatMap(heat_data, radius=15, blur=10, max_zoom=13).add_to(toronto_map)
    # Save the map as an HTML file
    toronto_map.save('toronto_collisions_heatmap.html')

def marker():
    marker_cluster = MarkerCluster().add_to(toronto_map)
    for index, row in collisions.iterrows():
        folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=f"Collision {row['ACCNUM']}").add_to(marker_cluster)
        # Save the map as an HTML file
        toronto_map.save('toronto_collisions_marker_map.html')

marker()