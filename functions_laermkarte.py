def map_func(uhrzeit):
    import plotly.express as px
    import pandas as pd
    import folium
    import geopandas as gpd
    import numpy as np
    from shapely.geometry import Polygon
    import time
    from datetime import datetime
    import serial
    from folium.plugins import TimeSliderChoropleth
    import branca

    # PLZ
    addr_fp = r"C:\Users\nopa9\Documents\Universität\Master - HTW\3. Semester\Wissensmanagement\data\plz.shp\plz.shp"
    plz_db = r"C:\Users\nopa9\Documents\Universität\Master - HTW\3. Semester\Wissensmanagement\data\plz_db.csv"

    # LOR
    lor_shap = r"C:\Users\nopa9\Documents\Universität\Master - HTW\3. Semester\Wissensmanagement\data\lor_planungsraeume_2021.shp\lor_planungsraeume_2021.shp"
    lor_db_data = r"C:\Users\nopa9\Documents\Universität\Master - HTW\3. Semester\Wissensmanagement\data\lor_db.csv"

    # Streets
    str_shap = r"C:\Users\nopa9\Documents\Universität\Master - HTW\3. Semester\Wissensmanagement\data\Detailnetz-Strassenabschnitte.shp\Detailnetz-Strassenabschnitte.shp"
    str_db_data = r"C:\Users\nopa9\Documents\Universität\Master - HTW\3. Semester\Wissensmanagement\data\str_db.csv"

    # Read data from files
    # DB data
    db = pd.read_csv(plz_db, sep=';')
    lor_db = pd.read_csv(lor_db_data, sep=';', dtype={'lor': object})
    str_db = pd.read_csv(str_db_data, sep=';', encoding='latin-1', dtype={'str': object})
    # Shap data
    ad = gpd.read_file(addr_fp)
    lor = gpd.read_file(lor_shap)
    str = gpd.read_file(str_shap)

    if(uhrzeit != ""):
        # Time subset for flask app
        db = db[db['zeit'] == uhrzeit]
        lor_db = lor_db[lor_db['zeit'] == uhrzeit]
        str_db = str_db[str_db['zeit'] == uhrzeit]


    # Re-project to WGS84
    # Copy of the identifier for index
    ad['geometry'] = ad['geometry'].to_crs(epsg=4326)
    ad['plz'] = ad['plz'].astype(np.int64)
    lor['geometry'] = lor['geometry'].to_crs(epsg=4326)
    #lor['PLR_ID'] = lor['PLR_ID'].astype(np.int64)
    str['geometry'] = str['geometry'].to_crs(epsg=4326)
    #str['strassencode'] = str['strassensc'].astype(np.int64)
    #db['plz'] = db['plz_id']

    # Join db-data onto shap file
    ad = ad.merge(db, left_on='plz', right_on='plz', how='left')
    #ad = ad.drop(['plz_x', 'plz_y', 'plz_id'], axis=1)

    lor = lor.merge(lor_db, left_on='PLR_ID', right_on='lor', how='left')
    #lor = lor.drop(['plr', 'lor'], axis=1)

    str = str.merge(str_db, left_on='strassensc', right_on='str', how='left')
    #str = str.drop(['str'], axis=1)

    # Sample data for every street
    str['db'] = np.random.randint(30, 100, str.shape[0])
    # Convert shap overlay into .jason format
    temp = ad.to_json()
    lor_json = lor.to_json()
    str_json = str.to_json()

    #########################################
    ########################################
    # Create a Map instance
    m = folium.Map(location=[52.49, 13.3], tiles=None,
                   zoom_start=11, control_scale=True)
    folium.TileLayer("OpenStreetMap").add_to(m)
    folium.TileLayer("stamentoner", show=False).add_to(m)
    # folium.PolyLine(lon_lat_list, tooltip="Lärmampel Hallisches Tor").add_to(m)

    chor = folium.Choropleth(
        geo_data=temp,
        name="Lärmkarte",
        data=db,
        columns=["plz", "db"],
        key_on="feature.properties.plz",
        fill_color="Reds",
        fill_opacity=0.6,
        nan_fill_color='light grey',
        nan_fill_opacity=0.05,
        line_opacity=0.1,
        legend_name="Lärmaufkommen in DB",
    ).add_to(m)
    chor.geojson.add_child(
        folium.features.GeoJson(temp, name="Postleitzahlen",
                                style_function=lambda feature: {
                                    "fillColor": "#ebe8e4",
                                    "fillOpacity": "0.0005",
                                    "color": "grey",
                                    "weight": "1.3"
                                }, control=False,
                                tooltip=folium.features.GeoJsonTooltip(
                                    fields=['plz', 'db'],
                                    aliases=["PLZ:", "DB:"],
                                    localize=False,
                                    sticky=False,
                                    labels=True,
                                    style=(
                                        "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                                    max_width=800,
                                ))
    )
    chor_lor = folium.Choropleth(
        geo_data=lor_json,
        name="Lärmkarte: LOR",
        data=lor_db,
        columns=["lor", "db"],
        key_on="feature.properties.PLR_ID",
        fill_color="Reds",
        fill_opacity=0.6,
        nan_fill_color='light grey',
        nan_fill_opacity=0.05,
        line_opacity=0.1,
        show=False
    ).add_to(m)
    chor_lor.geojson.add_child(
        folium.features.GeoJson(lor_json, name="LOR",
                                style_function=lambda feature: {
                                    "fillColor": "#ebe8e4",
                                    "fillOpacity": "0.0005",
                                    "color": "grey",
                                    "weight": "1.3"
                                }, control=False,
                                tooltip=folium.features.GeoJsonTooltip(
                                    fields=['PLR_NAME', 'db'],
                                    aliases=["LOR:", "DB:"],
                                    localize=False,
                                    sticky=False,
                                    labels=True,
                                    style=(
                                        "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                                    max_width=800,
                                ))
    )
    chor_str = folium.Choropleth(
        geo_data=str_json,
        name="Lärmkarte: Strassen",
        data=str_db,
        columns=["str", "db"],
        key_on="feature.properties.strassensc",
        fill_color="Reds",
        fill_opacity=7,
        nan_fill_color='light grey',
        nan_fill_opacity=0.000005,
        line_opacity=0.001,
        show=False
    ).add_to(m)
    chor_str.geojson.add_child(
        folium.features.GeoJson(str_json, name="Strassen",
                                style_function=lambda feature: {
                                    "fillColor": "#ebe8e4",
                                    "fillOpacity": "0.000005",
                                    "color": "grey",
                                    "weight": "0.85"
                                }, control=False,
                                tooltip=folium.features.GeoJsonTooltip(
                                    fields=['strassenna', 'db'],
                                    aliases=["Name:", "DB:"],
                                    localize=False,
                                    sticky=False,
                                    labels=True,
                                    style=(
                                        "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                                    max_width=800,
                                ))
    )
    for key in chor_lor._children:
        if key.startswith('color_map'):
            branca_color_map = chor_lor._children[key]
            del (chor_lor._children[key])
    for key in chor_str._children:
        if key.startswith('color_map'):
            branca_color_map = chor_str._children[key]
            del (chor_str._children[key])

    folium.LayerControl().add_to(m)
    m.show_in_browser()
    return
def hist_map_func():
    import plotly.express as px
    import pandas as pd
    import folium
    import geopandas as gpd
    import numpy as np
    from shapely.geometry import Polygon
    import time
    from datetime import datetime
    import serial
    from folium.plugins import TimeSliderChoropleth
    import branca

    # PLZ
    addr_fp = r"C:\Users\nopa9\Documents\Universität\Master - HTW\3. Semester\Wissensmanagement\data\plz.shp\plz.shp"
    plz_db = r"C:\Users\nopa9\Documents\Universität\Master - HTW\3. Semester\Wissensmanagement\data\plz_db.csv"

    # Read data from files
    # DB data
    db = pd.read_csv(plz_db, sep=';')
    # Shap data
    ad = gpd.read_file(addr_fp)

    # Re-project to WGS84
    # Copy of the identifier for index
    ad['geometry'] = ad['geometry'].to_crs(epsg=4326)
    ad['plz'] = ad['plz'].astype(np.int64)

    # Join db-data onto shap file
    ad = ad.merge(db, left_on='plz', right_on='plz', how='left')

    # Convert shap overlay into .jason format
    temp = ad.to_json()

    styledict = {
        '150': {
            '1694908800': {'color': '#ff5252', 'opacity': 0.5},
            '1694822400': {'color': '#ff7b7b', 'opacity': 0.5},
            '1694736000': {'color': '#913B4B', 'opacity': 0.5},
            '1694649600': {'color': '#D9483E', 'opacity': 0.5},
            '1694563200': {'color': '#EDA25C', 'opacity': 0.5},
        },
        '160': {
            '1694908800': {'color': '#D9483E', 'opacity': 0.5},
            '1694822400': {'color': '#913B4B', 'opacity': 0.5},
            '1694736000': {'color': '#FBFCD1', 'opacity': 0.5},
            '1694649600': {'color': '#EDA25C', 'opacity': 0.5},
            '1694563200': {'color': '#F9DF8F', 'opacity': 0.5},
        },
        '170': {
            '1694908800': {'color': '#FBFCD1', 'opacity': 0.5},
            '1694822400': {'color': '#EDA25C', 'opacity': 0.5},
            '1694736000': {'color': '#D9483E', 'opacity': 0.5},
            '1694649600': {'color': '#F9DF8F', 'opacity': 0.5},
            '1694563200': {'color': '#913B4B', 'opacity': 0.5},
        },
        '180': {
            '1694908800': {'color': '#D9483E', 'opacity': 0.5},
            '1694822400': {'color': '#ff7b7b', 'opacity': 0.5},
            '1694736000': {'color': '#F9DF8F', 'opacity': 0.5},
            '1694649600': {'color': '#913B4B', 'opacity': 0.5},
            '1694563200': {'color': '#FBFCD1', 'opacity': 0.5},
        },
        '130': {
            '1694908800': {'color': '#913B4B', 'opacity': 0.5},
            '1694822400': {'color': '#FBFCD1', 'opacity': 0.5},
            '1694736000': {'color': '#D9483E', 'opacity': 0.5},
            '1694649600': {'color': '#EDA25C', 'opacity': 0.5},
            '1694563200': {'color': '#F9DF8F', 'opacity': 0.5},
        },
        '110': {
            '1694908800': {'color': '#913B4B', 'opacity': 0.5},
            '1694822400': {'color': '#D9483E', 'opacity': 0.5},
            '1694736000': {'color': '#FBFCD1', 'opacity': 0.5},
            '1694649600': {'color': '#EDA25C', 'opacity': 0.5},
            '1694563200': {'color': '#F9DF8F', 'opacity': 0.5},
        },
    }

    m = folium.Map(location=[52.49, 13.3], tiles=None,
                   zoom_start=11, control_scale=True)
    folium.TileLayer("OpenStreetMap").add_to(m)
    folium.TileLayer("stamentoner", show=False).add_to(m)
    # folium.PolyLine(lon_lat_list, tooltip="Lärmampel Hallisches Tor").add_to(m)

    TimeSliderChoropleth(
        temp,
        styledict=styledict,
    ).add_to(m)
    colormap = branca.colormap.linear.YlOrRd_09.scale(40, 90)
    colormap = colormap.to_step(index=[40, 50, 60, 70, 80, 90])
    colormap.caption = 'DB'
    colormap.add_to(m)
    folium.LayerControl().add_to(m)
    m.show_in_browser()
    return