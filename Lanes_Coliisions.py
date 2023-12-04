import geopandas as gpd
from shapely.wkt import loads
from shapely.geometry import Point, LineString, MultiLineString
from sklearn.neighbors import BallTree
import pandas as pd

# Load bike lanes and collisions data
bike_lanes = pd.read_csv('bikelanes_file.csv')
bike_lanes_gdf = gpd.GeoDataFrame(
    bike_lanes.loc[:, [c for c in bike_lanes.columns if c != "geometry"]],
    geometry=gpd.GeoSeries.from_wkt(bike_lanes["geometry"]),
    crs="epsg:4326",
)

collisions = pd.read_csv('Cyclists.csv')
collisions = collisions[collisions['YEAR'] >= 2018]

# Data cleaning
# bike_lanes_gdf['name'] = bike_lanes_gdf['name'].str.extract(r'([a-zA-Z\s]+)', expand=False).str.strip()
# collisions['STREET1'] = collisions['STREET1'].str.extract(r'([a-zA-Z\s]+)', expand=False).str.strip()
# collisions['STREET2'] = collisions['STREET2'].str.extract(r'([a-zA-Z\s]+)', expand=False).str.strip()

# Ensure all geometries in bike_lanes_gdf are Lines or MultiLines
def get_coordinates(geom):
    if isinstance(geom, LineString) or isinstance(geom, MultiLineString) or isinstance(geom, Point):
        centroid = geom.centroid
        return (centroid.x, centroid.y)
    else:
        return (0, 0)


# Clean rows containing NaN in geometry_coordinates
bike_lanes_gdf['geometry_coordinates'] = bike_lanes_gdf['geometry'].apply(get_coordinates)
bike_lanes_gdf_cleaned = bike_lanes_gdf.dropna(subset=['geometry_coordinates'])

bike_lanes_gdf_cleaned.to_csv('bike_lanes_gdf_cleaned.csv', index=False)

# Create GeoDataFrame for collisions
geometry_collisions = [Point(xy) for xy in zip(collisions['LONGITUDE'], collisions['LATITUDE'])]
gdf_collisions = gpd.GeoDataFrame(collisions, geometry=geometry_collisions, crs="EPSG:4326")
gdf_collisions['geometry_coordinates'] = gdf_collisions['geometry'].apply(get_coordinates)

gdf_collisions.to_csv('gdf_collisions_cleaned.csv', index=False)

# Create BallTree for bike lanes
tree = BallTree(bike_lanes_gdf_cleaned['geometry_coordinates'].tolist(), metric='haversine')

# Find the distance to the nearest bike lane for each collision
distances, indices = tree.query(gdf_collisions['geometry_coordinates'].tolist(), k=1)
# gdf_collisions['nearest_bike_lane_code'] = indices

# Get the corresponding bike lane information
nearest_bike_lane_info = bike_lanes_gdf_cleaned.iloc[indices.flatten()]

# Reset the index of both dataframes
collisions.reset_index(drop=True, inplace=True)
nearest_bike_lane_info.reset_index(drop=True, inplace=True)

# Merge the information back to the original collisions DataFrame
collisions_with_distances = pd.concat([collisions, nearest_bike_lane_info[['code', 'name']]], axis=1)

# Save the merged data to a new CSV file
collisions_with_distances.to_csv('collisions_with_distances.csv', index=False)

collisions_and_bikelanes = collisions_with_distances[['ACCNUM', 'name', 'code']]
collisions_and_bikelanes.to_csv('collisions_and_bikelanes.csv', index=False)
