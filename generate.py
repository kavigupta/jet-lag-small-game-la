import fiona
import geopandas as gpd

from jtlg_small_la.game_region import (
    load_game_region,
    cutout,
    load_divisions,
)
from jtlg_small_la.stops import compute_stops
from jtlg_small_la.trains_roads import load_trains, load_buses

divisions = load_divisions()
game_region = load_game_region()
stops = compute_stops()
buses = load_buses()

fiona.supported_drivers["KML"] = "rw"
stops.to_file("processed/stops.kml", driver="KML")
with open("processed/stops.geojson", "w") as f:
    f.write(stops.to_json())


gpd.GeoDataFrame(geometry=[game_region]).to_file(
    "processed/game_region.kml", driver="KML"
)

with open("processed/cutout.geojson", "w") as f:
    f.write(gpd.GeoDataFrame(geometry=[cutout()]).to_json())

with open("processed/divisions.geojson", "w") as f:
    f.write(divisions.to_json())

with open("processed/train_lines.geojson", "w") as f:
    f.write(load_trains().to_json())

with open("processed/bus_lines.geojson", "w") as f:
    f.write(buses.to_json())
