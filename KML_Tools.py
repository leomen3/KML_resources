#!/usr/bin/env python

# Take a list of location pairs (Lat,Lon), convert to KML, and plot in Google earth.

import simplekml
import csv

def parse_csv(fName):
    kml = simplekml.Kml()
    with open(fName, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            kml.newpoint(name = row[3], coords=[(row[2],row[1])])
        kml.save(fName+".kml")
    return



def write_csv(f_name):
    with open(fName, 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['-19.9550', '-70.9496'])
        csv_writer.writerow(['-4.1546', '-132.7150'])
        csv_writer.writerow(['40.9181', '161.1426'])
    return

if __name__ == '__main__':
    fName = 'locations.csv'
    #write_csv(fName)
    parse_csv(fName)