#############################################################
# Computing NDVI, Classifying and Printing Result for point 349202, 3772473
###############################################################
folder_path = r"D:\Miret"

import arcpy
from arcpy.sa import *

arcpy.env.workspace = folder_path
arcpy.env.overwriteOutput = True

arcpy.CheckOutExtension("Spatial")

inRaster = 'Landsat.TIF'
NDVI_file = 'NDVI.tif'

RedBand = arcpy.Raster(inRaster +"/Band_3")
NIRBand = arcpy.Raster(inRaster +"/Band_4")

Diff = arcpy.sa.Float(NIRBand - RedBand)
Sum = arcpy.sa.Float(NIRBand + RedBand)
NDVI = arcpy.sa.Divide(Diff,Sum)

NDVI.save(NDVI_file)

NDVI_remap = RemapRange([[-1.0, 0.0, 1], [0.0, .3, 2], [.3, 1.0, 3]])

NDVI_Category = Reclassify(NDVI_file, "Value", NDVI_remap)
NDVI_Category.save("D:\Miret\NDVI_remap.tif")

result = arcpy

del inRaster, NDVI_file, NDVI_remap, NDVI_Category


#Get NDVI value for location

inNDVI = arcpy.Raster("NDVI.tif")
Band = 1
result = arcpy.GetCellValue_management(inNDVI, "349202 3772473", str(Band))
cellSize = float(result.getOutput(0))
print float(result.getOutput(0))

inRaster = arcpy.Raster("NDVI_remap.tif")
Band = 1
result = arcpy.GetCellValue_management(inRaster, "349202 3772473", str(Band))
cellSize = int(result.getOutput(0))
print int(result.getOutput(0))


del inNDVI, inRaster
