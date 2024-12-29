
import geopandas as gpd
import pandas as pd

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
