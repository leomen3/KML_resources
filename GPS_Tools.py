#!/usr/bin/env python

# Implement several functions:

# (1) Parse NMEA to CSV/SQL for each second creating: time, lat, lon
# (2) Compare two SQLs for difference in time each second
# (3) Plot track to map

import pynmea2
import string
from geopy.distance import vincenty
import time

def pack_line(pos_args):
    (pos_time, pos_lon, pos_lat) = pos_args
    line = "%s,%s,%s\n" % (pos_time, pos_lon, pos_lat)
    return line


def unpack_line(line):
    [pos_time, pos_lon_str, pos_lat_str] = [i for i in string.split(line,",")]
    pos_lon = float(pos_lon_str)
    pos_lat = float(pos_lat_str)
    return [pos_time, pos_lon, pos_lat]


def parse_NMEA2db(filename):
    """Open the nmea file, from each GGA message extract:
    time, longitude, latitude and write to csv and SQL"""
    f_in = open(filename,"r")
    fname_out = file_name+".csv"
    f_out = open(fname_out, "w")
    reader = pynmea2.NMEAStreamReader(f_in,'ignore')
    msg = "Start"
    prev = None
    i = 0
    while i < 10:
        prev = msg
        for msg in reader.next():
            try:
                if msg.sentence_type == 'GGA':
                    pos_time = msg.timestamp
                    pos_lat = msg.lat
                    pos_lon = msg.lon
                    write_sentence = pack_line(pos_time, pos_lon, pos_lat)
                    f_out.write(write_sentence)
            except:
                pass
        if str(msg) == str(prev):
            i+=1
        else:
            i = 0
    f_out.close()
    f_in.close()
    print "Done"
    return None


def calculate_distance(pos_lon1, pos_lat1, pos_lon2, pos_lat2):
    """return distance between coordinates in meters using Vincenty formula"""
    dist = vincenty( (pos_lat1, pos_lon1), (pos_lat2, pos_lon2)).m
    return dist

def compare_position(file1, file2):
    """Receive two files, and for each round second time stamp, compare the distance between two points.
    In case position is not available in both files for specific timestamp, discard it. Collect the discarded
    timestamps to statistics. Print to csv file"""
    distance_diff = {}  # dictionary in form of timestamp: lon1, lat1, lon2, lat2, dist

    # fill distance_diff with file1
    with open(file1,"r") as f:
        for line in f:
            [pos_time, pos_lon1, pos_lat1] = unpack_line(line)
            distance_diff[pos_time] = [pos_lon1, pos_lat1]

    # fill distance_diff with file2 and calculate dist
    with open(file2, "r") as f:
        for line in f:
            [pos_time, pos_lon2, pos_lat2] = unpack_line(line)
            if distance_diff.has_key(pos_time):
                pos_lon1, pos_lat1 = distance_diff[pos_time]
                dist = calculate_distance(pos_lon1, pos_lat1, pos_lon2, pos_lat2)
                distance_diff[pos_time].append(pos_lon2, pos_lat2, dist)

    # fill distance_diff with dist, discard entries where there is missing a measurement
    out_fname = "dist"+time.asctime().replace(" ","_")+".csv"
    with open(out_fname,"w") as f:
        for key, value in distance_diff.iteritems():
            if len(value) < 5:
                distance_diff.pop(key)
            else:
                f.write(str(key)+" : "+str(value))
    return

if __name__ == '__main__':
    #file_name = "/home/leo/PycharmProjects/KML_resources/bak/Teseo.log"
    #file_name = "/home/leo/PycharmProjects/KML_resources/bak/Ground_Truth.log"
    #parse_NMEA2db(file_name)
    file_name1 = "/home/leo/PycharmProjects/KML_resources/bak/Teseo.log.csv"
    file_name2 = "/home/leo/PycharmProjects/KML_resources/bak/Ground_Truth.log.csv"
    compare_position(file_name1, file_name2)


