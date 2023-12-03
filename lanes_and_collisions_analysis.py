import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.wkt import loads
from shapely.geometry import Point, LineString, MultiLineString

def set_empty_name(row):
    return 'others' if row['accident_count'] < 5 else row['name']

# Set pandas display options
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

collisions_and_bikelanes = pd.read_csv('collisions_and_bikelanes.csv')
bikelanes = pd.read_csv('bike_lanes_gdf_cleaned.csv')

# Group by 'name' column and calculate the number of accidents for each street
accidents_by_street = collisions_and_bikelanes.groupby('name').size().reset_index(name='accident_count')
accidents_by_bikelane = collisions_and_bikelanes.groupby('code').size().reset_index(name='accident_count')

def merging():
    merged_df = pd.merge(accidents_by_bikelane, bikelanes, on='code', how='left')
    merged_df = merged_df.sort_values(by='accident_count', ascending=False)

    # Parse the strings in the 'geometry' column into Shapely geometry objects
    merged_df['geometry'] = merged_df['geometry'].apply(loads)
    # Create a GeoDataFrame
    geo_df = gpd.GeoDataFrame(merged_df, geometry='geometry', crs="EPSG:4326")
    # Save as a shapefile
    geo_df.to_file('bikelanes_with_accidents.shp')

def plotting():
    accidents_by_street = collisions_and_bikelanes.groupby('name').size().reset_index(name='accident_count')
    # Randomly shuffle the order of streets
    accidents_by_street_random = accidents_by_street.iloc[np.random.permutation(len(accidents_by_street))]
    # Apply a function to the data frame
    accidents_by_street_random['name'] = accidents_by_street_random.apply(set_empty_name, axis=1)

    # Plot a bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(accidents_by_street_random['name'], accidents_by_street_random['accident_count'], color='skyblue')
    plt.xlabel('Street Name')
    plt.ylabel('Accident Count')
    plt.title('Accident Count by Street')

    # Rotate X-axis labels
    plt.xticks(rotation=45, ha='right')

    plt.show()


def pieing():
    accidents_by_street = collisions_and_bikelanes.groupby('name').size().reset_index(name='accident_count')
    # Sort by the number of accidents in descending order
    accidents_by_street = accidents_by_street.sort_values(by='accident_count', ascending=False)
    # Calculate the total number of accidents
    total_accidents = accidents_by_street['accident_count'].sum()

    # Calculate the percentage
    accidents_by_street['percentage'] = accidents_by_street['accident_count'] / total_accidents * 100

    # Mark streets with less than 10% as "other"
    accidents_by_street.loc[accidents_by_street['percentage'] < 2.2, 'name'] = 'other'
    accidents_by_street = accidents_by_street.groupby('name').sum().reset_index()

    # Plot a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(accidents_by_street['accident_count'], labels=accidents_by_street['name'], autopct='%1.1f%%', startangle=90)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    # Display the plot
    plt.show()


def plot_bikelanes_with_accidents_on_map(input_collisions_file, input_bikelanes_file, basemap_file):
    # Read collision, bikelane, and basemap data
    collisions_and_bikelanes = pd.read_csv(input_collisions_file)
    bikelanes = pd.read_csv(input_bikelanes_file)
    basemap = gpd.read_file(basemap_file)
    basemap = basemap.to_crs('EPSG:4326')
    # Group by 'code' and calculate the number of accidents for each bikelane
    accidents_by_bikelane = collisions_and_bikelanes.groupby('code').size().reset_index(name='accident_count')
    # Merge accident count and bikelane data
    merged_df = pd.merge(accidents_by_bikelane, bikelanes, on='code', how='left')
    # Convert strings in the 'geometry' column to LINESTRING objects
    merged_df['geometry'] = merged_df['geometry'].apply(loads)
    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(merged_df, geometry='geometry')
    # Plot the map and data
    fig, ax = plt.subplots(figsize=(12, 12))
    # Plot the basemap
    basemap.plot(ax=ax, color='lightgrey', edgecolor='white')
    # Plot bikelanes and accident data
    gdf.plot(ax=ax, column='accident_count', cmap='OrRd', legend=True, legend_kwds={'label': "Accident Count"}, markersize=merged_df['accident_count']*100)
    # Set title and axis labels
    plt.title('Bikelanes with Accident Count on Basemap')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    # Display legend
    plt.show()

# Execute the functions
merging()
plot_bikelanes_with_accidents_on_map('collisions_and_bikelanes.csv', 'bike_lanes_gdf_cleaned.csv', 'bikeway_network.shp')
