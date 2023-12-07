# CME538 Fall 2023 Data Detectives Big Project

## Objective 
* Temporal analysis of trends and patterns of collisions involving cyclists in Toronto;
* Geospatial exploration of collisions involving cyclists to reveal spatial distributions and correlations in Toronto;
* Analysis of collision patterns concerning Toronto neighborhood characteristics for correlations or trends;
* Analysis of weather conditions to determine instances where collision likelihood increases; and
* Assessment of the relationship between cycling infrastructures and collision occurrences to understand potential influences.

## Dataset (datasets can be found in the [datasets](https://github.com/yuqiaochen-code/data_detectives_CME538/tree/e734f5feef779a45d4507c9a1abcbefd4a78e9a4/datasets) folder)

* **Toronto Collision Map** is provided by [Toronto Police Service Public Safety Data Portal](https://data.torontopolice.on.ca/pages/cyclists) and contained traffic-related serious and fatal collisions involving cyclists from 2006 to 2022. Columns within the dataset are used in this data analysis are listed as follows.
  * `INDEX_`: unique identifier of each collision.
  * `DATE`: dates of collisions. Note this column is not in  datetime  format and needs to be converted to `datetime` format before conducting analysis.
  * `TIME`: time collision occurred.
  * `DISTRICT`: district where the collision happened, including Scarborough, Toronto and East York, North York, and Etobicoke York
  * `ACCLOC`: location where the collisions occurred (e.g. intersections, bridges, etc.).
  * `TRAFFCTL`: types of traffic controls present at collisions (e.g. traffic signals, traffic controller, stop sign, etc.).
  * `LIGHT`: light conditions at the scene of collisions.
  * `INVAGE`: age groups of party involved.
  * `INVTYPE`: involvement type.
  * `NEIGHBOURH`: neighbourhoods where the collisions happened
  * `geometry`: coordinates of the collisions. This column is used for plotting maps in this data analysis.
  * `INJURY`: Severity of injury.
  
  Note: There are two columns in the cyclist collision data, `INDEX_` (unique identifier) and `ACCNUM` (accident number). According to the data [documentation](https://ago-item-storage.s3.amazonaws.com/c0b17f1888544078bf650f3b8b04d35d/PSDP_Open_Data_Documentation.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIEz1X2KcVaSeTcG46NOF1EoAvrN4I%2Fb1kDezKXuSYAdYAiEAiNoPkAXcZx1ljR33lLyDftCEBddeO4QgZ8Z5q6EIUN0qswUITBAAGgw2MDQ3NTgxMDI2NjUiDCNr9DGiZp9J77IN5SqQBd4YpzfSczx6p2L%2FiTU79Po%2BjD05%2F8M3U2k%2F1s5vowY8joGkoTQ4DmdypI3LVDdRdeB2EVXBdozcOOE5LWRrwEMPKQJ5v31uo%2BhSR%2BmlyiISrK%2F5O15iSNrEjvI8Pz8mSkVZoy8v9CEEQvMYdSdgyOoiFX254fM%2BCtsbjcVZtOKOpV9QYkwqkanDB71GQtMidDQE27rGflkzlX%2BQJ%2BkArtG8XX6QGHILcu52jI6rVhUxSvzb%2FotvN8zAWCULFBoneG3OilCn%2BDvZTA3Tv8PxX2rlJvEVboS7tyy7smvHUAkPz%2FNyU5X8m3QJr6HMhJuvU4jnvsuOadg57sVBmbNrCmygBL64O2b6o1MR7tNizKzx40%2F3AVxT1%2FgLBR0gOhbkKnIoiZYU12bzVGZwZMetXoy5WFfWc7RqBLD1UE9UXNWL0QbF3pojiu%2F0uxURa78YKYv6OgV7ofhiGOq07GbZrqKwtxw6YKnxxKIVOWIj23OTe8wq4HQKWLy40tT6htwGFdNoApJr5Ku8mNjd%2F37EM7S%2B8yWAdy8Kg8t%2BHfKL8My7D%2FW0jvCOQ2FTmwxNZSlISvjcSHLRqI7xk0OD8voCH2479lze5pHx2aTahfkST8WaExgZFeo%2F4PXeaLGm3kgMZviZOYAc5Df0zu%2BKsx4raEI%2Bvsi39KYNHCE2vy0ZLeNPoijL%2BgvlsgRNaSoF22xJqw8DAxgqDQaNersT3Ru26tkCro5FBgsjkYZJQGhcBX4R4pxGIxiogYbVnTa0AvMD6gCFFRRlj4u3Ozwn7eotPGi%2B4B4L3K409PhFz2BeFGfwsMlOux45UtWnRnW3xBoKMvkIZMgANkm6iaL6cwNTnvCDDPtN7QNqj2quDF3tBnyhMK%2BYs6sGOrEBy7bcsAUiOovgjpH%2FWBdscsPEiS9pUGsc8Zdnn4AtylZtvOxkEnGOT7hbs9CM9BIVn2OVZlIqQzU9fs3lWOqqicXM1%2FVvtLwzBUakgSzFhUS0BKuEF5l8zb%2FBAp29%2Fnli8ho92T%2F2N2FtHdIVALcxvhb%2Fi4z3UkiG3%2BPaWPaJkiA327WvcensUf01IRl6DLy2y1m0E%2B%2Fz5XUbGRfjNuc7BjaG2PIOoRYRhvthhTD1SyQ5&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231203T200010Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAYZTTEKKE7K7VYYU5%2F20231203%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=a8a9f2d11e3202d38659ec2bcb67cb9df6d6eafb33684271a228d9b624420392), account numbers could be used repeatedly year after year and are not unique, `INDEX_` was used for grouping by certain columns and counting the number of collisions for each group.

* **[Toronto Neighbourhoods Map](https://github.com/yuqiaochen-code/data_detectives_CME538/blob/66e05653a912a5a1b7ce3b187a17b586e546442e/toronto_neighbourhoods.shp)** This is a `shp` file and can be plotted directly using its `geometry` column. Only `FIELD_8` and `geometry` columns are used in this geometry. `FIELD_8` is the name of the neighbourhoods.
  
* **Toronto neighbourhoods profiles** data provided by Toronto Open Data portal, [Neighbourhood profiles](https://open.toronto.ca/dataset/neighbourhood-profiles/) This dataset come from Census of Population held across Canada every 5 years and has data about age and sex, families and households, language, immigration and internal migration, ethnocultural diversity, Aboriginal peoples, housing, education, income, and labour.

  This is an Excel file and the first column of the dataframe should be the column names. Therefore, the dataframe was transposed and adjusted before analysis. Columns used from this dataset in this analysis are `Neighbourhood Name` and `Total - Age groups of the population - 25% sample data`, which the one fourth of the populations. In this analysis, total population is used in calculations. Therefore, the numbers in the column `Total - Age groups of the population - 25% sample data` are multiplied by four.
  
* **Toronto weather data**, obtained from Government of Canada website: [Toronto historial weather data](https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=51459). Columns within this dataset that are used in this data analysis are listed as follows.
  * `Date/Time`: the year, month, day and time when it occurred
  * `Temp (°C)`: recorded temperature
  * `Dew Point Temp (°C)`: Dew Point Temperature (°C) is a meteorological parameter that represents the temperature at which air becomes saturated with moisture and dew begins to form.
  * `Rel Hum (%)`:  relative humidity in percentage.
  * `Wind Dir (10s deg)`: wind direction in tens of degrees.
  * `Wind Spd (km/h) `: wind speed in kilometers per hour. 
  * `Visibility (km)`:  the horizontal visibility in kilometers.
  * `Hmdx `: humidex.
  * `Wind Chill`: quantify the cooling effect of the wind on the perceived temperature.
  * `Precip. Amount (mm)`: the amount of precipitation.
  * `Weather`: indicates different weather conditions.

    `Date/Time` column needs to be converted to datetime variable and localized to 'EST' timezone.

    There are a number of columns containing only the word Flag. These columns can be removed since they only contain overlapping information.

    There are columns that contain `NaN` or `M`. According to Environment and Climate Change Canada, `M` represents 'missing', which means the data is unretrievable or unavailable. The missing values in `Hmdx` and `Wind Chill` should not be modified because the `Hmdx` values are only reported if: (1) air temperature is greater than or equal to 20 degrees celsius and, (2) the `Hmdx` is at least 1 degree greater than the air temperature. Similarily, wind chill is only calculated if the air temperature is less than or equal to 0 degrees celsius. Additionally, the Weather column is the visual observation of the weather environment and appears to be important. The missing values in this column means a clear weather. So missing values should be assigned with Clear.
The weather data was sampled every hour, so it is reasonable to input missing values based on the time-adjacent valid observations, except columns `Hmdx`, `Wind Chill`, and `Weather`. All other columns will have missing values filled using linear interpolation between valid observations.

 * **[Cycling Network](https://open.toronto.ca/dataset/cycling-network/)**: This dataset illustrates the existing cycling network across the city, including both shared and dedicated bikeways. There is a column in this dataset called `route_type`. Only data with bike lane as `route_type` were used for this analysis. The dataset is a `shp` file. Columns in the dataset are listed as follows:
   * `name`: name of the street/road/avenue the bikelane located at
   * `route_type`: the type of the route. in this project, they are all 'bike lane'
   * `length`: the length of the bike lane
   * `geometry`: geometry data, containing the grometric information of the bike lane. LINESTRING


## Results and key findings
* Data cleaning and analysis code:
  [Temporal and geospatial analysis](https://github.com/yuqiaochen-code/data_detectives_CME538/blob/eeaed84ebd72642f740602bad175d584e1c82799/code/Correlation%20between%20the%20cyclist%20collisIon%20severity%20and%20weather_Hongxiang%20Gong.ipynb)
  
  [weather-related analysis](https://github.com/yuqiaochen-code/data_detectives_CME538/blob/eeaed84ebd72642f740602bad175d584e1c82799/code/Correlation%20between%20the%20cyclist%20collisIon%20severity%20and%20weather_Hongxiang%20Gong.ipynb)
  
  [Cycling infrastructure-related analysis](https://github.com/yuqiaochen-code/data_detectives_CME538/blob/eeaed84ebd72642f740602bad175d584e1c82799/code/Correlation%20between%20the%20cyclist%20collisIon%20severity%20and%20weather_Hongxiang%20Gong.ipynb)

  
* Figures
  Figures in the `figure` folder can all be reproduced using the code as shown in the links above.
  
* Medium article link
  For more details of our findings, as well as our interpretations, please visit our [Medium ariticle](https://medium.com/@yuqiaoc.chen/toronto-cyclists-collision-data-analysis-8896f317116d).


