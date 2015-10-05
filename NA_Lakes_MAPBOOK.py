###############
# MAKES A PDF MAPBOOK OF LARGE LAKES IN NORTH AMERICA SHAPEFILE
###################

folder_path = r"D:\Miret"
import arcpy
import math
import os

arcpy.env.workspace = folder_path
arcpy.env.overwriteOutput = True

Lakes = arcpy.GetParameterAsText(0)
Cities = arcpy.GetParameterAsText(1)
NA = arcpy.GetParameterAsText(2)

Lakes = "NA_Big_Lakes.shp"
NA = "North_America.shp"
Cities = "NA_Cities.shp"

desc = arcpy.Describe(Lakes)
shapeName = desc.ShapeFieldName

inRows = arcpy.SearchCursor(Lakes)

outDir = r"D:\Miret"
MapPDF_filename = outDir + r"\Miret_Mapbook.pdf"

if os.path.exists(outDir + r"\TempPages.pdf"):
    os.remove(outDir + r"\TempPages.pdf")

if os.path.exists(MapPDF_filename):
    os.remove(MapPDF_filename)

MapPDF= arcpy.mapping.PDFDocumentCreate(MapPDF_filename)

mxd = arcpy.mapping.MapDocument(outDir + r"\NALakes.mxd")

df = arcpy.mapping.ListDataFrames(mxd, "Layers") [0]

tot_area = 0
tot_count = 0

for lake in inRows:
    geom = lake.Shape
    tot_area+=lake.Area_km2
    tot_count+=1

meanLakes = tot_area/tot_count
titleElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[0]

titleElement.text = "North American Big Lakes" + '\n\r' + "Nancy Miret"+  '\n\r' + "Number of Lakes: 18" + '\n\r'+ "Total Area: " + str(tot_area) + "km2" + '\n\r'+ "Mean Area: " + str(meanLakes) + "km2"
map_text = "North American Big Lakes" + '\n\r' + "Nancy Miret"+  '\n\r' + "Number of Lakes: 18" + '\n\r'+ "Total Area: " + str(tot_area) + '\n\r'+ "Mean Area: " + str(meanLakes)

del titleElement

for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    if elm.text == "text":
        elm.text = map_text

arcpy.RefreshTOC()
arcpy.RefreshActiveView()

arcpy.mapping.ExportToPDF(mxd, outDir + r"\TempPages.pdf")

MapPDF.appendPages(outDir + r"\TempPages.pdf")

for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    if elm.text == map_text:
        elm.text = "text"

dflist = arcpy.mapping.ListDataFrames(mxd)
lyrlist = arcpy.mapping.ListLayers(mxd, "", dflist[0])
for lyr in lyrlist:
    if lyr.name == "NA_Cities":
        lyr.showLabels = True

inRows=arcpy.SearchCursor(Lakes)
lake_count = 0

titleElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[0]

for row in inRows:
    titleElement.text = "Lake FID: " + str(row.FID) + '\n\r' + "Area(km2): " + str(row.Area_km2)
    lake_count = lake_count + 1
    CITY_NAME = ""
    CNTRY_NAME = ""
    ADMIN_NAME = ""
    POP_CLASS = ""
    DISTANCE = 0
    XY = ""
    feature = row.getValue(shapeName)
    mapText = "Lake FID: " + str(row.FID) + '\n\r' + "Area(km2): " + str(row.Area_km2)
    print mapText

    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.text == "text":
            elm.text = mapText

    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()

    df.extent = feature.extent
    arcpy.mapping.ExportToPDF(mxd, outDir + r"\TempPages.pdf")

    MapPDF.appendPages(outDir + r"\TempPages.pdf")

    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.text == mapText:
            elm.text = "text"

MapPDF.updateDocProperties(pdf_open_view = "USE_THUMBS",
                                pdf_layout= "SINGLE_Page")
MapPDF.saveAndClose()


del titleElement, row, inRows, mxd, MapPDF

