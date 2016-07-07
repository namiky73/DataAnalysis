import sqlite3
import csv
from math import sin, cos, acos, radians
import matplotlib.pyplot as plt
import seaborn
import numpy as np
import sys


# 距離計算（参考:http://qiita.com/s-wakaba/items/e12f2a575b6885579df7）
def latlng_to_xyz(lat, lng):
    rlat, rlng = radians(lat), radians(lng)
    coslat = cos(rlat)
    return coslat*cos(rlng), coslat*sin(rlng), sin(rlat)

def dist_on_sphere(lat1,lng1,lat2,lng2):
    radious = 6378.137
    xyz1, xyz2 = latlng_to_xyz(lat1,lng1), latlng_to_xyz(lat2,lng2)
    return acos(sum(x * y for x, y in zip(xyz1, xyz2)))*radious


# sqliteから選択した駅のレストラン情報（score,lat,lng）を抽出
def select_from_db(station_name):
    con_from = sqlite3.connect("./data/tokyo_all.sqlite3",timeout=60.0)
    rows = con_from.execute('select score,lat,lng from stores where nearest_station = ?',(station_name,))
    station_restaurants = []
    for row in rows:
        station_restaurants.append({'score': row[0], 'lat': row[1], 'lng': row[2]})
    return station_restaurants


def select_from_csv(staition_name):
    f = open('./data/yamanote_lat_lng.csv', 'r')
    reader = csv.reader(f)
    stations = {}
    for r in reader:
        stations[r[0] + '駅'] = {'lat': r[1], 'lng': r[2]}
    f.close()
    return stations[staition_name]

def get_dist_score(station_name):
    station_restaurants = select_from_db(station_name)
    station_place = select_from_csv(station_name)
    dist_score_list = []
    for rst in station_restaurants:
        if (not rst['score'])  or (rst['lng'] == 0.0):
            continue
        dist = dist_on_sphere(float(rst['lat']), float(rst['lng']), float(station_place['lat']), float(station_place['lng']))
        dist_score_list.append([ rst['score'], dist])
    return dist_score_list


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('input one station name')
        quit()
    station = sys.argv[1]
    dist_score_list = np.array( get_dist_score(station) )
    plt.scatter(dist_score_list[: , 1], dist_score_list[: , 0])
    plt.show()
