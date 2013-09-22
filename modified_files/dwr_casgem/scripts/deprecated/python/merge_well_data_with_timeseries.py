#!/usr/bin/python
import sys, os, datetime, time, pymongo, simplejson, json, ast


# Connect to mongodb
conn = pymongo.Connection("localhost",27017)

# Connect to mongo database
db = conn.watertable
# Connect to collection
c = db.database
w = db.wells
t = db.timeseries


# load each well
# find each record in the database
# append subbasin and well depth
# remove redundant fields

well_count = 0
count = 0
for doc in db.wells.find({}):
  well_id = doc["properties"]["CASGEM_STATION_ID"]
  well_count = well_count + 1
  for time in db.database.find({"id": well_id}):
      time_mongo_id = time["_id"]
      time['properties']['GW_BASIN_NAME'] = doc["properties"]["GW_BASIN_NAME"]
      time['properties']['HYDROLOGIC_REGION'] = doc["properties"]["HYDROLOGIC_REGION"]
      time['properties']['TOTAL_WELL_DEPTH'] = doc["properties"]["TOTAL_WELL_DEPTH"]
      time['properties']['GW_BASIN_CODE'] = doc["properties"]["GW_BASIN_CODE"]
      time['properties']['WELL_USE'] = doc["properties"]["WELL_USE"]
      time['properties']['COUNTY'] = doc["properties"]["county"]
      # del time['properties']['']

      db.database.save(time);
      count = count + 1
      ##db.database.update({'_id':time["_id"]}, {"$set": time}, upsert=false)
    
print "done. wells:" + str(well_count) + " timeseries records:" + str(count)