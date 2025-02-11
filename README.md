# Jet Lag Home Game Los Angeles Map

Designed by Kavi and Avery for the Jet Lag Home Game, small gamemode.

[![Map](https://raw.githubusercontent.com/kavigupta/jet-lag-small-game-la/main/print_map.png)](https://raw.githubusercontent.com/kavigupta/jet-lag-small-game-la/main/print_map.png)

## Resources

- [Zoomable SVG map](https://raw.githubusercontent.com/kavigupta/jet-lag-small-game-la/main/print-map.svg)
- [Printable PDF map](https://raw.githubusercontent.com/kavigupta/jet-lag-small-game-la/main/print_map.pdf). This
    map should be printed on two side-by-side 8.5x11 sheets of paper, each in portrait mode.
- [Google My Maps](https://www.google.com/maps/d/edit?mid=1BKx9rX0BonyyMdFFSdzmTasXtM5NeZE&usp=sharing)

## Design Choices

We decided to include all train stops, as well as Metro bus stops with at least two distinct lines that are not within a train station hiding zone.
For the prefecture/canton equivalent, we use neighborhoods in Los Angeles and CDPs outside it. There are a few areas that are neither neighborhoods nor CDPs,
which are given the special name "No CDP", which should be treated as their name. All 3 regions should be treated as distinct for the purpose of the "Same prefecture/canton"
question.


## Shapefile sources

Boundary (JLTG Home Game Los Angeles - Small.kml): Avery hand drew this boundary.

CA CDPs (ca_places.zip): https://data.ca.gov/dataset/ca-geographic-boundaries
LA neighborhoods (LA_Times_Neighborhood_Boundaries.geojson): https://geohub.lacity.org/maps/la-times-neighborhood-boundaries

Bus stops serving lines (StopsServingLines1224.zip): https://developer.metro.net/gis-data/
Train stops (230711_All_MetroRail_Stations.zip): https://developer.metro.net/gis-data/

Train lines (202307-All-Rail-Lines-Combined.zip): https://developer.metro.net/gis-data/
Bus lines (Individuals1224.zip) https://developer.metro.net/gis-data/
Roads (tl_2018_06037_roads.zip): https://catalog.data.gov/dataset/tiger-line-shapefile-2018-county-los-angeles-county-ca-all-roads-county-based-shapefile
