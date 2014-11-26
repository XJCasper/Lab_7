#Import modules...
import arcpy
import geopy
import TwitterSearch
from arcpy import env
from TwitterSearch import *
from geopy import geocoders

#Set workspace
env.workspace = "C:/Users/XJCasper/Desktop/MSGST_2015/Fall/TGIS_501/labs/lab_7/data"
env.overwriteOutput = True

#Geocoding details to be returned...
def geo(location):
    g = geocoders.GoogleV3()
    loc = g.geocode(location)
    return loc.latitude, loc.longitude

#Keyword search parameters 
try:
    #Create a TwitterSearchOrder object
    tso = TwitterSearchOrder()
    #Define keywords to search for:
    tso.set_keywords(["Mustang GT500"])
    #creates and breaks down parameters to include or not?
    tso.set_include_entities(False)
    
    #Keys, passwords, and tokens needed to run Twitter search API.
    ts = TwitterSearch(
        consumer_key = 'MTJKzFbdmjUwZRLmTSZhMpbQO',
        consumer_secret = '3KLZoDxQF4jZbFoqYgigtgrXkrQpb2JQ236Iwn0K18Jxff38CB',
        access_token = '2435257592-KSls0i3DhuQckFz0GD7Z69dAastpnwPprErjruB',
        access_token_secret = 'qHKsyRUQmu8aAsME2oOLOeGfVMIzvFZ1G8h0FGGqvCEjX'
     )

    #Step 3:  Create a shapefile from results and set coordinate projection
    spatial = arcpy.SpatialReference(4152)
    fc = "twitter.shp"
    outpath = "C:/Users/XJCasper/Desktop/MSGST_2015/Fall/TGIS_501/labs/Lab_7/data"
    arcpy.management.CreateFeatureclass(outpath, fc, "POINT", "", "DISABLED", "DISABLED", spatial)

    #Add fields for attribute table:
    arcpy.management.AddField(fc, "TWEETER", "TEXT", "", "", 30, "", "",)
    arcpy.management.AddField(fc, "USERNAME", "TEXT", "", "", 30, "", "")
    arcpy.management.AddField(fc, "DATE", "TEXT", "", "", 20, "", "")
    arcpy.management.AddField(fc, "TWITPOST", "TEXT", "", "", 80, "", "")
    arcpy.management.AddField(fc, "CITYSTATE", "TEXT", "", "", 30, "", "")
    arcpy.management.AddField(fc, "COORDINATS", "FLOAT", "", "", 40, "", "")
    cursor = arcpy.da.InsertCursor(fc, ["SHAPE@"])

    #Defines how and what informations is going to be returned from the search:
    for tweet in ts.search_tweets_iterable(tso):
        if tweet['place'] is not None:
        #Update attribute table
            update = arcpy.da.UpdateCursor(fc, ["TWEETER", "USERNAME", "DATE", "TWITPOST", "CITYSTATE", "COORDINATS"])
            coordinats = (tweet['coordinates'])
            cord = list(reduce(lambda x, y: x + y, coordinats.items()))
            xy = cord[3]
            cordlist = []
            cordup = xy[1], xy[0]
            cordlist.append(cordup)
            cursor.insertRow(cordlist)
            tweeter = (tweet['user']['name'])
            twitpost = (tweet['text'])
            username = (tweet['user']['screen_name'])
            citystate = (tweet['user']['location'])
            date = (tweet['created_at'])
            lat = xy[1]
            lng = xy[0]
            #(lat, lng) = geo(tweet['place']['full_name'])
 #           TweetList.append((float(lat), float(lng)))
            #print "Tweeted from: " + "(" + str(lat) + ", " + str(lng) + ")"
            for row in update:
                if row in update:
                    if row[0] == " ":
                        row[0] = tweeter
                        update.updateRow(row)
                    elif row[1] == " ":
                        row[1] = username
                        update.updateRow(row)
                    elif row[2] == " ":
                        row[2] = date
                        update.updateRow(row)
                    elif row[3] == " ":
                        row[3] = twitpost
                        update.updateRow(row)
                    elif row[4] == " ":
                        row[4] = citystate
                        update.updateRow(row)
                    elif row[5] == " ":
                        row[5] = coordinats
                        update.updateRow(row)
                        
##    #Create and define points
 ##                   point = arcpy.Point()
##                    pointlist = []
##                    for pt in TweetList:
##                        point.x = pt[0]
##                        point.y = pt[1]
##                        pointlist.append(arcpy.PointGeometry(point))
##                    arcpy.CopyFeatures_management(pointlist, fc)
##                    arcpy.DefineProjection_management(fc, spatial)
##
#Eliminates searched tweets that might come up or create errors.
except TwitterSearchException as e:
    print(e)
print "Shapefile finished"
