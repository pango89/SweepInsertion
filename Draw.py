import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np


def plot_my_data(df):
    lat = df['latitude'].values
    lon = df['longitude'].values

    # determine range to print based on min, max lat and lon of the data
    margin = 2  # buffer to add to the range
    lat_min = min(lat) - margin
    lat_max = max(lat) + margin
    lon_min = min(lon) - margin
    lon_max = max(lon) + margin

    # create map using BASEMAP
    m = Basemap(llcrnrlon=lon_min, llcrnrlat=lat_min,
                urcrnrlon=lon_max,
                urcrnrlat=lat_max,
                lat_0=(lat_max - lat_min) / 2,
                lon_0=(lon_max - lon_min) / 2,
                projection='merc',
                resolution='h',
                area_thresh=10000.,
                )

    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color='white', lake_color='#46bcec')

    route_id = 1
    max_route_id = 2 # max(df['routeId'].values)

    depot_lat = 39.1972
    depot_long = -76.730867

    while route_id <= max_route_id:
        df_route = df.loc[df['routeId'] == route_id]

        lat_route = df_route['latitude'].values
        long_route = df_route['longitude'].values

        lat_route = np.concatenate([[depot_lat], lat_route, [depot_lat]])
        long_route = np.concatenate([[depot_long], long_route, [depot_long]])

        # convert lat and lon to map projection coordinates
        longs_route, lats_route = m(long_route, lat_route)

        # plot points as red dots
        # m.scatter(longs, lats, marker='o', color='r', zorder=5)
        m.plot(longs_route, lats_route, 'o-', linewidth=1, zorder=5)
        route_id += 1

    plt.title("Routes")
    plt.show()


def plot_my_data_1(df):
    y_pos = np.arange(len(df.index))
    x_pos = df['travelTime'].values

    x_labels = df['routeId'].values

    plt.bar(y_pos, x_pos, align='center', alpha=0.5)
    plt.xticks(y_pos, x_labels)
    plt.ylabel('Travel Time in Minutes')
    plt.xlabel('Route Number')
    plt.title('Route Level Information')

    plt.show()