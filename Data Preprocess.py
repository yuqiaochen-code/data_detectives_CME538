import os
import json
import requests
import geopandas as gpd
import pandas as pd
import folium
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from geopy.distance import distance as geopy_distance
import pickle

# Set pandas options to fit pycharm
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

def load_bikeshare_data():
    # get bike station information
    response = requests.get('https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information')
    bikeshare_stations = pd.DataFrame(json.loads(response.content)['data']['stations'])[['station_id', 'name', 'lat', 'lon', 'capacity']].astype({'station_id': 'int'})
    bikeshare_stations = bikeshare_stations.rename(columns={'station_id': 'Station Id', 'name': 'Station Name'})
    bikeshare_stations_gdf = gpd.GeoDataFrame(bikeshare_stations, geometry=gpd.points_from_xy(bikeshare_stations['lon'], bikeshare_stations['lat']))
    bikeshare_stations_gdf.crs = {'init': 'epsg:4326'}

    # get bikelanes information
    bike_lanes = gpd.read_file('bikeway_network.shx')
    bike_lanes = bike_lanes[['LF_NAME', 'SEG_TYPE', 'length', 'geometry']]
    bike_lanes = bike_lanes.rename(columns={'LF_NAME': 'name', 'SEG_TYPE': 'route_type'})
    bike_lanes = bike_lanes[bike_lanes['route_type'] == 'bike lane']
    bike_lanes = bike_lanes.to_crs(epsg=4326)

    # get Toronto neighbourhoods information
    neighbourhoods = gpd.read_file('toronto_neighbourhoods.shp')
    neighbourhoods = neighbourhoods[['geometry', 'FIELD_8']]
    neighbourhoods = neighbourhoods.rename(columns={'FIELD_8': 'name'})
    neighbourhoods['name'] = neighbourhoods['name'].str.replace(r'\s\(\d+\)', '', regex=True)
    neighbourhoods['area'] = neighbourhoods.geometry.area * 1e4
    target_crs = 'EPSG:26917'
    neighbourhoods = neighbourhoods.to_crs(target_crs)
    bikeshare_stations_gdf = bikeshare_stations_gdf.to_crs(target_crs)
    bike_lanes = bike_lanes.to_crs(target_crs)

    return bikeshare_stations_gdf, bike_lanes, neighbourhoods

def visualize_data(neighbourhoods, bike_lanes, bikeshare_stations_gdf):
    # visualization
    fig, ax = plt.subplots(figsize=(10, 10))
    neighbourhoods.plot(ax=ax, color='lightgray', edgecolor='k', label='Neighbourhoods')
    bike_lanes.plot(ax=ax, color='blue', linewidth=2, label='Bike Lanes')
    plt.show()

    # calculate numbers and density of each neighbourhood
    neighbourhoods['stations'] = neighbourhoods.apply(lambda neighborhood: len(bikeshare_stations_gdf[bikeshare_stations_gdf.within(neighborhood['geometry'])]), axis=1)
    neighbourhoods = neighbourhoods.sort_values(by='stations', ascending=False)
    neighbourhoods['station_density'] = neighbourhoods['stations'] / neighbourhoods['area']
    neighbourhoods = neighbourhoods.sort_values(by='station_density', ascending=False)

    # distribute bike stations to neighbourhoods
    bikeshare_stations_gdf['neighbourhood'] = None
    for _, neighborhood in neighbourhoods.iterrows():
        stations_within_neighborhood = bikeshare_stations_gdf[bikeshare_stations_gdf.geometry.within(neighborhood['geometry'])]
        bikeshare_stations_gdf.loc[stations_within_neighborhood.index, 'neighbourhood'] = neighborhood['name']

def create_graph(bikeshare_stations_gdf, bike_lanes):
    # initialize a graph
    G = nx.Graph()

    # bike station nodes
    for index, station in bikeshare_stations_gdf.iterrows():
        G.add_node(station['Station Id'], type='station', name=station['Station Name'], geometry=station['geometry'])

    # bieklane nodes
    threshold_distance = 200
    for index, lane in bike_lanes.iterrows():
        G.add_node(index, type='bike_lane', name=lane['name'], length=lane['length'], geometry=lane['geometry'])

    # adding edges
    for _, station in bikeshare_stations_gdf.iterrows():
        for _, lane in bike_lanes.iterrows():
            if station['geometry'].distance(lane['geometry']) < threshold_distance:
                G.add_edge(station['Station Id'], index)

    return G

def visualize_graph(G):
    # visualization
    pos = {node: (data['geometry'].x, data['geometry'].y) if data['geometry'].geom_type == 'Point' else (data['geometry'].centroid.x, data['geometry'].centroid.y) for node, data in G.nodes(data=True)}

    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(G, pos, node_size=10, node_color='blue', alpha=0.5)
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.2)
    plt.title('图可视化')
    plt.show()

def add_graph_features(G, bikeshare_stations_gdf, bike_lanes, pos, distance_function):
    # add node features
    for node, data in G.nodes(data=True):
        data['x'] = pos[node][0]
        data['y'] = pos[node][1]

        if 'type' in data and data['type'] == 'station':
            station_info = bikeshare_stations_gdf[bikeshare_stations_gdf['Station Id'] == node].iloc[0]
            data['capacity'] = station_info['capacity']

        if 'type' in data and data['type'] == 'bike_lane':
            lane_info = bike_lanes.iloc[node]
            data['length'] = lane_info['length']

    # add edge features
    for u, v, data in G.edges(data=True):
        data['edge_type'] = 'station_bike_lane' if 'type' in G.nodes[u] and G.nodes[u]['type'] == 'station' else 'bike_lane_station'
        data['distance'] = distance_function(G.nodes[u]['x'], G.nodes[u]['y'], G.nodes[v]['x'], G.nodes[v]['y'])

    # add graph features
    G.graph['density'] = nx.density(G)
    G.graph['average_degree'] = np.mean([deg for _, deg in G.degree()])

    return G

def calculate_distance(x1, y1, x2, y2):
    # geospatial distance
    coords1 = (y1, x1)  # 注意顺序：纬度在前，经度在后
    coords2 = (y2, x2)
    return geopy_distance(coords1, coords2).meters

def main():
    # load data
    bikeshare_stations_gdf, bike_lanes, neighbourhoods = load_bikeshare_data()

    # visualize
    visualize_data(neighbourhoods, bike_lanes, bikeshare_stations_gdf)

    # create a graph
    G = create_graph(bikeshare_stations_gdf, bike_lanes)

    # visualize it
    visualize_graph(G)

    # add features
    pos = {node: (data['geometry'].x, data['geometry'].y) if data['geometry'].geom_type == 'Point' else (data['geometry'].centroid.x, data['geometry'].centroid.y) for node, data in G.nodes(data=True)}
    G = add_graph_features(G, bikeshare_stations_gdf, bike_lanes, pos, calculate_distance)

    # save path
    save_path = 'Big Project'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # save
    with open(os.path.join(save_path, 'bike_graph.pkl'), 'wb') as f:
        pickle.dump(G, f)



if __name__ == "__main__":
    main()
