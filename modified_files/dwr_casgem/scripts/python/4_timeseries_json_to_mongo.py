#!/usr/bin/python
import sys, os, simplejson, pymongo, datetime, time

# Create list of files.
file_list = []

# Connect to mongodb
conn = pymongo.Connection("localhost",27017)

# Set path to list of files for input.
path = "../../database/geojson"


# Read each file in the directory.
for file in [doc for doc in os.listdir(path)

# Build list of file names in the directory.
if doc.endswith(".json")]:
    file_list.append(file)

def stringToFloat(val):
    if(val != "NULL"):
        if(val != ""):
            val = val.replace(",","")
            return float(val)
    else:
        return val
    
# Read file list.
for i in file_list:

    print "Processing file: " + path + i

    # Connect to mongo database
    db = conn.watertable
    # Connect to collection
    c = db.database
    # Open geoJSON file
    o = open(path + "/" + i)
    # Read into memory
    s = simplejson.load(o)
    o.close()  


    # Read the features part of the geoJSON document and insert into mongoDB.
    for x in s['features']:
        date = x['properties']['date']
        ts = datetime.datetime.strptime(date, '%m/%d/%Y')
        #isodate = datetime.datetime.fromtimestamp(ts, None)
        x['properties']['isodate'] = ts

        # Convert string values to floats or integers.
        if(x['properties']['gs_to_ws'] != "NULL"):
            x['properties']['gs_to_ws'] = stringToFloat(x['properties']['gs_to_ws'])
        if(x['properties']['rp_elevation'] != "NULL"):
            x['properties']['rp_elevation'] = stringToFloat(x['properties']['rp_elevation'])
        if(x['properties']['reading_ws'] != "NULL"):
            x['properties']['reading_ws'] = stringToFloat(x['properties']['reading_ws'])
        if(x['properties']['rp_to_ws'] != "NULL"):
            x['properties']['rp_to_ws'] = stringToFloat(x['properties']['rp_to_ws'])
        if(x['properties']['gs_elevation'] != "NULL"):
            x['properties']['gs_elevation'] = stringToFloat(x['properties']['gs_elevation'])
        if(x['properties']['reading_rp'] != "NULL"):
            x['properties']['reading_rp'] = stringToFloat(x['properties']['reading_rp'])
        if(x['properties']['wse'] != "NULL"):
            x['properties']['wse'] = stringToFloat(x['properties']['wse'])

        # Add well metadata to record
        for doc in db.wells.find({'properties.CASGEM_STATION_ID': x['id']}).limit(1):
            x['properties']['gw_basin_name'] = doc["properties"]["GW_BASIN_NAME"].encode('ascii')
            x['properties']['hydrologic_region'] = doc["properties"]["HYDROLOGIC_REGION"].encode('ascii')
            x['properties']['total_well_depth'] = doc["properties"]["TOTAL_WELL_DEPTH"]
            x['properties']['gw_basin_code'] = doc["properties"]["GW_BASIN_CODE"].encode('ascii')
            x['properties']['well_use'] = doc["properties"]["WELL_USE"].encode('ascii')
            x['properties']['county'] = doc["properties"]["COUNTY"].encode('ascii')
        c.insert(x)

print "Done."
sys.exit()


# Dump mongo database
# mongodump --collection database --db watertable --dbpath ~/htdocs/nwca_dropbox/Dropbox/data/data-water-table/mongodb
db.database.create_index([("geometry.coordinates", GEO2D)])
db.database.create_index([("properties.isodate", 1)])
db.database.create_index([("properties.county", 1)])

# db.database.ensureIndex({'geometry.coordinates': '2d'});
# db.database.ensureIndex({'properties.isodate': 1})
# db.database.ensureIndex({'properties.county': 1})