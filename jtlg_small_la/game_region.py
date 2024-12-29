from functools import lru_cache
import geopandas as gpd
import tqdm
import pandas as pd
from shapely.geometry import Polygon, mapping

from jtlg_small_la.geo import compute_dlon


def load_raw_game_region():
    boundary = gpd.read_file("data/JLTG Home Game Los Angeles - Small.kml")
    boundary = boundary.iloc[0].geometry
    game_region = Polygon(mapping(boundary)["coordinates"])
    return game_region


def load_game_region():
    game_region = load_raw_game_region()
    divisions = load_divisions()
    game_region = game_region.intersection(divisions.unary_union)
    return Polygon(game_region.buffer(compute_dlon(5e-3)).exterior)


def cutout():
    game_region = load_game_region()
    pad = 0.1

    box = bounding_box(game_region, pad)

    return box.difference(game_region)


def bounding_box(game_region, pad):
    min_x, min_y, max_x, max_y = game_region.bounds
    min_x -= pad
    min_y -= pad
    max_x += pad
    max_y += pad

    box = Polygon(
        [(min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y), (min_x, min_y)]
    )

    return box


def load_raw_divisions():
    places = gpd.read_file("data/ca_places.zip").to_crs("epsg:4326")
    places = places[places.NAMELSAD != "Los Angeles city"]
    places["is_la"] = 0
    neighborhoods = gpd.read_file("data/LA_Times_Neighborhood_Boundaries.geojson")
    neighborhoods["is_la"] = 1
    divisions = gpd.GeoDataFrame(
        pd.concat(
            [
                places[["NAME", "geometry", "is_la"]].rename(columns={"NAME": "name"}),
                neighborhoods[["name", "geometry", "is_la"]],
            ]
        )
    )
    divisions = divisions.reset_index(drop=True)
    return divisions


def load_raw_divisions_with_non_cdp():
    divisions = load_raw_divisions()
    all_divs = divisions.geometry.unary_union
    missing = bounding_box(all_divs, 0).difference(all_divs)
    missings = [
        x.intersection(missing)
        for x in tqdm.tqdm(missing.geoms)
        if x.bounds != all_divs.bounds
    ]
    divisions = gpd.GeoDataFrame(
        pd.concat(
            [divisions, pd.DataFrame(dict(name="No CDP", geometry=missings, is_la=2))]
        )
    )
    divisions = divisions[divisions.area > 1e-5]
    return divisions

@lru_cache(None)
def load_divisions():
    game_region = load_raw_game_region()
    divisions = load_raw_divisions_with_non_cdp()
    divisions_covering = divisions[
        divisions.geometry.intersects(game_region.buffer(-compute_dlon(100e-3)))
    ]
    divisions_covering.geometry = divisions_covering.intersection(game_region)
    return divisions_covering
