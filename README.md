# CME538 Fall 2023 Data Detectives Big Project

## Objective 
* Temporal analysis of trends and patterns of collisions involving cyclists in Toronto;
* Geospatial exploration of collisions involving cyclists to reveal spatial distributions and correlations in Toronto;
* Analysis of collision patterns concerning Toronto neighborhood characteristics for correlations or trends;
* Analysis of weather conditions to determine instances where collision likelihood increases; and
* Assessment of the relationship between cycling infrastructures and collision occurrences to understand potential influences

## Dataset

* **Toronto Collision Map** is provided by [Toronto Police Service Public Safety Data Portal](https://data.torontopolice.on.ca/pages/cyclists) and contained traffic-related serious and fatal collisions involving cyclists from 2006 to 2022. Columns within the dataset are used in this data analysis are listed as follows.
  * `INDEX_`: unique identifier of each collision
  * `DATE`: date of collision. Note this is not in datetime format, and needed to be converted to datetime format before conducting analysis.  
  * `DISTRICT`: district where the collision happened, including Scarborough, Toronto and East York, North York, and Etobicoke York)
  * `ACCLOC`: location where the collisions occurred.
  * `TRAFFCTL`: types of traffic controls present at collisions (e.g. traffic signals, traffic controller, stop sign, etc.)
  * `LIGHT`: light conditions at the scene of collisions
  * `INVAGE`: age groups of party involved
  * `INVTYPE`: involvement type
  * `NEIGHBOURH`: neighbourhood where the collisions happened
  * `geometry`: latitude and longitude where the collisions happened. This column is used for plotting maps in this data analysis.

Note: There are two columns in the cyclist collision data, `INDEX_` (unique identifier) and `ACCNUM` (accident number). According to the data documentation (link), account numbers could be used repeatedly year after year and are not unique, `INDEX_` was used for grouping by certain columns and counting the number of collisions for each group.

* [Toronto Neighbourhoods Map](https://github.com/yuqiaochen-code/data_detectives_CME538/blob/66e05653a912a5a1b7ce3b187a17b586e546442e/toronto_neighbourhoods.shp) This is a shp file and can be plotted directly using its `geometry` column. Only `FIELD_8` and `geometry` columns are used in this geometry. `FIELD_8` is the name of the neighbourhoods.
  
* Toronto neighbourhoods profiles data provided by Toronto Open Data portal: [Neighbourhood profiles](https://open.toronto.ca/dataset/neighbourhood-profiles/) This dataset come from Census of Population held across Canada every 5 years and has data about age and sex, families and households, language, immigration and internal migration, ethnocultural diversity, Aboriginal peoples, housing, education, income, and labour.

  This is an Excel file and the first column of the dataframe should be the column names. Therefore, the dataframe was transposed and adjusted before analysis. Columns used from this dataset in this analysis are `Neighbourhood Name` and `Total - Age groups of the population - 25% sample data`, which the one fourth of the populations.
  

* Toronto weather data, obtained from Government of Canada website: [Toronto historial weather data](https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=51459)
* [Cycling Network](https://open.toronto.ca/dataset/cycling-network/): The Toronto bikeways dataset illustrates the existing cycling network across the city, including both shared and dedicated bikeways


## Results and key findings
* Data analysis notebooks:
* Figures and tables: 
* Medium article link:

## Future directions

