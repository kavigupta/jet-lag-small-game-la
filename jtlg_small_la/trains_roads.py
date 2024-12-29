

import zipfile

import geopandas as gpd
import numpy as np
import pandas as pd

from jtlg_small_la.stops import compute_stops

def load_trains():
    layers = {
        "220909_Crenshaw Shapes": "K",
        "801_Metro_A_Line_Post_Regional_Connector": "A",
        "802_805_Track_0316": "B/D",
        "803_Track_0316": "C",
        "804_Metro_E_Line_Post_Regional_Connector": "E",
    }
    results = []
    for layer in layers:
        table = gpd.read_file("data/202307-All-Rail-Lines-Combined.zip", layer=layer)
        table["line"] = layers[layer]
        table = table.to_crs("epsg:4326")
        results.append(table)
    return gpd.GeoDataFrame(pd.concat(results))

def load_buses():
    stops = compute_stops()
    def preferred_direction(t):
        counts = t.groupby(t.VAR_DIREC).count().VAR_ROUTE
        return counts.index[np.argmax(counts)]


    lines = [
        x.filename.replace(".shp", "")
        for x in zipfile.ZipFile("data/Individuals1224.zip").filelist
        if x.filename.endswith(".shp")
    ]
    tables = [gpd.read_file("data/Individuals1224.zip", layer=line) for line in lines]
    tables = [t[t.VAR_DIREC == preferred_direction(t)] for t in tables]
    line_shp = pd.concat(tables)
    valid_lines = {
        str(x)
        for xs in stops[stops.is_train == 0].lines.apply(
            lambda x: [int(t) for t in x.split(", ")]
        )
        for x in xs
    }
    line_shp = line_shp[line_shp.VAR_ROUTE.isin(valid_lines)]
    return line_shp