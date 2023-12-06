import geopandas as gpd
from shapely.wkt import loads
from shapely.geometry import Point, LineString, MultiLineString
from sklearn.neighbors import BallTree, _kd_tree
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap

def load_and_clean_bike_lanes(file_path):
    bike_lanes = pd.read_csv(file_path)
    bike_lanes_gdf = gpd.GeoDataFrame(
        bike_lanes.loc[:, [c for c in bike_lanes.columns if c != "geometry"]],
        geometry=gpd.GeoSeries.from_wkt(bike_lanes["geometry"]),
        crs="epsg:4326",
    )

    # Data cleaning
    bike_lanes_gdf['geometry_coordinates'] = bike_lanes_gdf['geometry'].apply(get_coordinates)
    bike_lanes_gdf_cleaned = bike_lanes_gdf.dropna(subset=['geometry_coordinates'])

    bike_lanes_gdf_cleaned.to_csv('bike_lanes_gdf_cleaned.csv', index=False)

    return bike_lanes_gdf_cleaned

def load_and_clean_collisions(file_path):
    collisions = pd.read_csv(file_path)
    collisions = collisions[collisions['YEAR'] >= 2018]

    geometry_collisions = [Point(xy) for xy in zip(collisions['LONGITUDE'], collisions['LATITUDE'])]
    gdf_collisions = gpd.GeoDataFrame(collisions, geometry=geometry_collisions, crs="EPSG:4326")
    gdf_collisions['geometry_coordinates'] = gdf_collisions['geometry'].apply(get_coordinates)

    gdf_collisions.to_csv('gdf_collisions_cleaned.csv', index=False)

    return gdf_collisions

def find_nearest_bike_lanes(bike_lanes_gdf_cleaned, gdf_collisions):
    tree = BallTree(bike_lanes_gdf_cleaned['geometry_coordinates'].tolist(), metric='haversine')

    distances, indices = tree.query(gdf_collisions['geometry_coordinates'].tolist(), k=1)

    nearest_bike_lane_info = bike_lanes_gdf_cleaned.iloc[indices.flatten()]

    collisions_with_distances = pd.concat([gdf_collisions, nearest_bike_lane_info[['code', 'name']]], axis=1)

    collisions_with_distances.to_csv('collisions_with_distances.csv', index=False)

    return collisions_with_distances[['ACCNUM', 'name', 'code']]

def create_toronto_map(collisions, map_type='marker'):
    toronto_map = folium.Map(location=[43.70, -79.42], zoom_start=11)

    if map_type == 'heatmap':
        heat_data = [[row['LATITUDE'], row['LONGITUDE']] for _, row in collisions.iterrows()]
        HeatMap(heat_data, radius=15, blur=10, max_zoom=13).add_to(toronto_map)
        toronto_map.save('toronto_collisions_heatmap.html')
    elif map_type == 'marker':
        marker_cluster = MarkerCluster().add_to(toronto_map)
        for _, row in collisions.iterrows():
            folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=f"Collision {row['ACCNUM']}").add_to(marker_cluster)
        toronto_map.save('toronto_collisions_marker_map.html')

# Load and clean bike lanes data
bike_lanes_gdf_cleaned = load_and_clean_bike_lanes('bikelanes_file.csv')

# Load and clean collisions data
gdf_collisions = load_and_clean_collisions('Cyclists.csv')

# Find nearest bike lanes for each collision
collisions_and_bikelanes = find_nearest_bike_lanes(bike_lanes_gdf_cleaned, gdf_collisions)

# Create Toronto map with either heatmap or marker cluster
create_toronto_map(collisions_and_bikelanes, map_type='marker')
