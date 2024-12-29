import numpy as np
import geopandas as gpd
import tqdm
import networkx as nx

from jtlg_small_la.geo import distances


def bus_transfer_stops():
    stops = gpd.read_file("./data/StopServingLines1224.zip")
    lat, lon = np.array(stops.LAT), np.array(stops.LONG)
    d = distances(lat, lon, lat, lon)

    a, b = np.where(d < 50e-3)
    g = nx.Graph()
    g.add_nodes_from(np.arange(len(stops)))
    g.add_edges_from(np.array([a, b]).T)

    results = []
    for stop_idxs in tqdm.tqdm(list(nx.connected_components(g))):
        for_stop = stops.loc[list(stop_idxs)]
        lines = {
            line.split("-")[0]
            for line in np.array(
                for_stop[[x for x in stops if x.startswith("LINE")]]
            ).flatten()
            if line is not None
        }
        if len(lines) == 1:
            continue
        assert len(lines) > 0
        results.append(
            dict(
                name=for_stop.STOPNAME.iloc[0],
                lines=", ".join(sorted(lines)),
                geometry=for_stop.geometry.iloc[0],
            )
        )
    return gpd.GeoDataFrame(results)
