import geopandas as gpd
import pandas as pd
from shapely import Point

from jtlg_small_la.game_region import load_game_region
from jtlg_small_la.geo import compute_dlon, distances
from jtlg_small_la.bus_transfer_stops import bus_transfer_stops

km_in_mi = 1.60934
hiding_radius_km = 0.25 * km_in_mi


def compute_stops():
    game_region = load_game_region()
    bts = bus_transfer_stops()
    trains = gpd.read_file("data/230711_All_MetroRail_Stations.zip")
    trains = trains.copy()
    trains = trains.rename(columns={"STOP_NAME": "name"})
    trains["lines"] = "train"
    trains = trains[["name", "lines", "geometry"]].copy()
    bts = bts[
        ~(
            distances(
                trains.geometry.y, trains.geometry.x, bts.geometry.y, bts.geometry.x
            )
            < hiding_radius_km
        ).any(-1)
    ].copy()

    trains["is_train"] = 1
    bts["is_train"] = 0

    new_row = {
            "name": "Metrolink Glendale",
            "lines": "train",
            "geometry": gpd.GeoSeries(
                Point(-118.25909547330987, 34.12357314654583), crs="EPSG:4326"
            ),
            "is_train": 1,
        }
    new_row = pd.DataFrame(new_row)

    stops = pd.concat([trains, bts, new_row])
    game_region_unbuffered = game_region.buffer(-compute_dlon(hiding_radius_km))
    stops = stops[stops.geometry.apply(game_region_unbuffered.contains)]
    stops = stops.reset_index(drop=True)
    stops.name = stops.name.apply(remove_stop_suffix)

    return gpd.GeoDataFrame(stops)

def remove_stop_suffix(x):
    suffix = " Station"
    if x.endswith(suffix):
        return x[:-len(suffix)]
    return x
