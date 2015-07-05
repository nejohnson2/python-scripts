import geopandas as gp
import os
from geopandas.tools import sjoin  # this is still in development 

'''
	This script is designed to merge three shapefiles - PLUTO, NYC Census 
	Blocks and DSNY Sections.
	
	To Do:
	Same issue with outputing BBL.  Need to confirm everything is accurate
'''

dpath = './'
dsny_section_file = 'DSNY_Sections/DSNY_sections.shp'
census_blocks_file = 'nycb2010_15b/nycb2010.shp'
pluto_file = 'Update/NYC_PLUTO.shp'

print "Reading files..."
pluto = gp.GeoDataFrame.from_file(os.path.join(dpath, pluto_file))
dsny_sections = gp.GeoDataFrame.from_file(os.path.join(dpath, dsny_section_file))
census_blocks = gp.GeoDataFrame.from_file(os.path.join(dpath, census_blocks_file))
	
	
census_blocks.to_crs(dsny_sections.crs, inplace=True)
pluto.crs = dsny_sections.crs

pluto['geometry'] = pluto['geometry'].centroid

print "Begin spatial joins..."
census_pluto = sjoin(pluto, census_blocks, how="left", op="within")

census_pluto.drop(['geometry', 'CB2010_right', 'CT2010_right','Shape_Area','Shape_Leng','index_right'], axis=1, inplace=True)

# --
# Re-merge the old file to use the Polygon instead of the point
census_pluto = census_pluto.merge(census_blocks[['geometry', 'BCTCB2010']])

census_pluto['geometry'] = census_pluto['geometry'].centroid

dsny_pluto_census = sjoin(census_pluto, dsny_sections, how="left", op="within")

writePath = dpath + 'Output/'
writePathFile = writePath + 'nyc.shp'

dsny_pluto_census['AssessTot'] = dsny_pluto_census['AssessTot'].astype(str)
dsny_pluto_census['BBL'] = dsny_pluto_census['BBL'].astype('int32')

if not os.path.exists(writePath):
	os.makedirs(writePath)
	
print "Writing file..."
dsny_pluto_census.to_file(writePathFile)
print "Finished"