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

# Clean rows containing NaN in geometry_coordinates
gdf_collisions_cleaned = gdf_collisions.dropna(subset=['geometry_coordinates'])

# Create BallTree for bike lanes
tree = BallTree(bike_lanes_gdf_cleaned['geometry_coordinates'].tolist(), metric='haversine')

# Find the distance to the nearest bike lane for each collision
distances, indices = tree.query(gdf_collisions_cleaned['geometry_coordinates'].tolist(), k=1)
gdf_collisions_cleaned['nearest_bike_lane_distance'] = distances

# # Merge bike lane information to the collisions DataFrame
# merged_collisions = gpd.sjoin(gdf_collisions, bike_lanes_gdf_cleaned, how="left", op="intersects")
#
# # Print the resulting DataFrame
# print(merged_collisions[['ACCNUM', 'nearest_bike_lane_distance', 'name']])

# # Save the merged data to a new CSV file
# merged_collisions.to_csv('merged_collisions.csv', index=False)

# 创建一个字典，将每个自行车道的geometry坐标和名称关联
bike_lane_dict = dict(zip(bike_lanes_gdf_cleaned['geometry_coordinates'], bike_lanes_gdf_cleaned['code']))

# 通过最近的自行车道的geometry坐标查找名称
gdf_collisions_cleaned['nearest_bike_lane_code'] = gdf_collisions_cleaned['geometry_coordinates'].map(bike_lane_dict)

# 打印包含最近自行车道名称的结果DataFrame
print(gdf_collisions_cleaned[['ACCNUM', 'nearest_bike_lane_distance', 'nearest_bike_lane_code']])

# 将结果保存为CSV文件
gdf_collisions_cleaned.to_csv('collisions_with_distances.csv', index=False)
