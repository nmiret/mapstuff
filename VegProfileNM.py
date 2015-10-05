################################################
#Clip and Calculate Vegetation for Each Campsite
################################################

folder_path = r"C:\Users\rchen\Desktop\Miret"
import arcpy, os
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
print 'starting process'

env.workspace = folder_path
arcpy.env.overwriteOutput = 'True'


calveg = folder_path + "\Cal_Veg.shp"

campsites = folder_path + "\Campsites.shp"

campsiteCounter = 0

# Make a layer from the feature class
arcpy.MakeFeatureLayer_management(campsites, "lyr") 


campCursor = arcpy.SearchCursor(campsites) 

for site in campCursor:
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", '"FID" = ' + str(campsiteCounter) + '')
    print campsiteCounter
    tmpShp = folder_path + '\\' + str(campsiteCounter)
    arcpy.CopyFeatures_management("lyr", tmpShp)

    #clip features
    in_features = "Cal_Veg.shp"
    clip_features = "lyr"
    out_feature_class = folder_path + '\\' + str(campsiteCounter) +'clip.shp'
    xy_tolerance = ""

    # Execute Clip
    arcpy.Clip_analysis(in_features, clip_features, out_feature_class, xy_tolerance)



    #Polygon to Raster
    inFeatures = folder_path + '\\' + str(campsiteCounter) +'clip.shp'
    valField = "WHRNAME"
    outRaster = folder_path + '\\' + str(campsiteCounter) +'site.tif'


    # Execute Polygon To Raster
    arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster)

    
    # Zonal Statistics Table
    inZoneData = folder_path + '\\' + str(campsiteCounter) +'site.tif'
    zoneField = "WHRNAME"
    inValueRaster = folder_path + '\\' + str(campsiteCounter) +'site.tif'
    outTable = folder_path + '\\' + str(campsiteCounter) +'site.dbf'


    # Execute ZonalStatisticsAsTable
    outZSaT = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable, "DATA", "MAJORITY")

    #Add field for "PERCENT"
    arcpy.AddField_management(outTable, "PERCENT", "DOUBLE") 

    #Populate "PERCENT" field
    vegcount = 0
    vegtotal = 0

    tableCursor = arcpy.SearchCursor(outTable)
    for row in tableCursor:
        vegcount += 1
        vegtotal += row.COUNT
        
    percenttable = arcpy.UpdateCursor(outTable)
    for row in percenttable:
        vegpercent = (float(row.COUNT)/vegtotal)*100
        row.PERCENT = vegpercent
        percenttable.updateRow(row)
   
    del row
    del percenttable
    
    
    campsiteCounter = campsiteCounter+1



print "Done"
