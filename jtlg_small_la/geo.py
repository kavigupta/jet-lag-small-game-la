import numpy as np


r_earth = 6378.1370
lat_la = 34.0549


def distances(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = (
        np.array(lat1),
        np.array(lon1),
        np.array(lat2),
        np.array(lon2),
    )
    dlon = lon1 - lon2[:, None]
    dlat = lat1 - lat2[:, None]
    dy = r_earth * np.deg2rad(dlat)
    dx = r_earth * np.cos(np.deg2rad(lat_la)) * np.deg2rad(dlon)
    d = (dy**2 + dx**2) ** 0.5
    return d


def compute_dlon(distance_x_km):
    return np.rad2deg(distance_x_km / r_earth / np.cos(np.deg2rad(lat_la)))
