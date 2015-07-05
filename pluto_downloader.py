import urllib2
import zipfile
import geopandas as gp
import pandas as pd
import numpy as np
import sys, getopt, os, glob

'''
	This script first download the five PLUTO shapefiles from the
	source links.  It then unzips the file and deletes the original
	zip file.  Then, it opens each file and subsets a bunch of columns
	to make the data more manageable.  Finally, it writes the new files
	to a new folder called "Update/".
	
	To do: 
		- There is something funny going on with the BBL column.  I cant seem
		to set the dtype correctly.  It changes the numbers to negative 
		values...
		- there is some issues with crs...as always.  The output file 
		doesnt seem to have a crs
	
'''

bx = 'http://www.nyc.gov/html/dcp/download/bytes/bx_mappluto_14v2.zip'
qn = 'http://www.nyc.gov/html/dcp/download/bytes/qn_mappluto_14v2.zip'
bk = 'http://www.nyc.gov/html/dcp/download/bytes/bk_mappluto_14v2.zip'
mn = 'http://www.nyc.gov/html/dcp/download/bytes/mn_mappluto_14v2.zip'
si = 'http://www.nyc.gov/html/dcp/download/bytes/si_mappluto_14v2.zip'

def main(directory):
	print "Current directory: ", directory
	sources = [mn, si]
	fileList = []
	
	# Download all source files
	for i in sources:
		print "Downloading from: ", i
		#downloadFile(i)
	
	allFiles = glob.glob(directory + "/*/*.shp")
	for i in allFiles:
		if i[-9:] == 'PLUTO.shp':
			fileList.append(i)
			
	print "Detected " + str(len(fileList)) + " files."
	print fileList
	
	df = gp.GeoDataFrame()
	df.crs = {}
	for i in fileList:
		data = readFiles(i, directory)
		df.crs = data.crs
		df = df.append(data, ignore_index=True)
	
	df.set_geometry(df.geometry, inplace=True)

	writeFile(df, directory)
	
# ---
# Write the final shapefile
# ---
def writeFile(data, directory):
	print "Writing master file..."
	# check if directory exists
	fileDestination = directory + '/Update'
	newFile = directory + '/Update/NYC_PLUTO.shp'
	if not os.path.exists(fileDestination):
		os.makedirs(fileDestination)
		
	print "New File Location: ", newFile

	data.to_file(newFile)
	
# --
# Open files and subset data
# -- 
def readFiles(inputfile, directory):
	print "Reading file..."
	print inputfile
	data = gp.GeoDataFrame.from_file(inputfile)
	cols = ['geometry','BBL','ZipCode','UnitsRes','Address','Borough','CD','AssessTot','Block','LandUse','ResArea','CT2010', 'CB2010']
	pluto = gp.GeoDataFrame(data, columns=cols)
	pluto.crs = data.crs
	
	# for some reason the file will not export unless the data types are set properly
	pluto['AssessTot'] = pluto['AssessTot'].astype(str)
	pluto['BBL'] = pluto['BBL'].astype('int32')
	
	return pluto

# --
# Download all five pluto shapefiles
# --
def downloadFile(captureUrl):
	data = urllib2.urlopen(captureUrl)
	outputFile = captureUrl[-20:]
	print outputFile
	output = open(outputFile,'wb')
	output.write(data.read())
	output.close()
	unzip(outputFile)

def unzip(zipFile):
	print "Extracting ", zipFile
	with zipfile.ZipFile(zipFile, "r") as z:
		z.extractall("")

	os.remove(zipFile) # remove .gz file	

if __name__ == "__main__":
	main(os.path.dirname(os.path.realpath(__file__)))
	print "Finished"