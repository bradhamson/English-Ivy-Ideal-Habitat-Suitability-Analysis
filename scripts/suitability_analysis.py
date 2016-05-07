import os
import time
import json
import pickle
import itertools
import arcpy
from arcpy.sa import (EucDistance, 
	Aspect, 
	RemapRange, 
	RemapValue, 
	Reclassify,
	FuzzyMembership,
	FuzzyLinear,
	FuzzySmall,
	FuzzyOverlay)

def list_objects():
	vectors = arcpy.ListFeatureClasses()
	rasters = arcpy.ListRasters()
	objects = itertools.chain(vectors, rasters)
	return objects

def switch_workspace(src, *args):
	if arcpy.env.workspace == src:
		arcpy.env.workspace = args[0]
	if not arcpy.env.workspace:
		arcpy.env.workspace = src

def create_output_gdb(src):
	output_dir = os.path.dirname(src)
	dest = os.path.join(output_dir, 'working_data.gdb')
	arcpy.CreateFileGDB_management(output_dir, 'working_data.gdb')
	add_to_gdb(src, dest)
	reproject()

def add_to_gdb(src, dest):
	switch_workspace(src)
	vector = arcpy.ListFeatureClasses()
	raster = arcpy.ListRasters()
	for fc in raster:
		arcpy.RasterToGeodatabase_conversion(fc, dest)
	for fc in vector:
		arcpy.CopyFeatures_management(fc, os.path.join(dest, 
			fc.split('.')[0]))
	switch_workspace(src, dest)

def clean_up():
	fcs = arcpy.ListFeatureClasses()
	for fc in fcs:
		desc = arcpy.Describe(fc)
		if not desc.spatialReference.factoryCode == 102387:
			arcpy.Delete_management(fc)
		if fc.endswith('_projected'):
			arcpy.Rename_management(fc, fc.split('_')[0])

def reproject():
	out_crs = arcpy.SpatialReference(102387)
	fcs = arcpy.ListFeatureClasses()
	for fc in fcs:
		desc = arcpy.Describe(fc)
		if not desc.spatialReference.factoryCode == 102387:
			out_fc = '{}_projected'.format(fc)
			arcpy.Project_management(fc, out_fc, out_crs)
	clean_up()

def distance(fc):
	output = os.path.join(arcpy.env.workspace, '{}_dist'.format(fc))
	distance = EucDistance(fc, "#", 63.9370612000003)
	# CopyRaster instead of distance.save() to set correct raster properties
	arcpy.CopyRaster_management(distance, output, '', '#', '', 'NONE',
		'NONE', '32_BIT_UNSIGNED')

def aspect(fc):
	output = os.path.join(arcpy.env.workspace, 'Aspect')
	desc = arcpy.Describe(fc)
	if desc.dataType == 'RasterDataset':
		aspect = Aspect(fc)
		aspect.save(output)

def rasterize(fc):
	output = os.path.join(arcpy.env.workspace, 'Soils')
	arcpy.FeatureToRaster_conversion(fc, 'Drainage', output, 63.3278848987445)

def reclassify(fcs):
	remap = json.load(open('json/remap.json', 'r+'))
	for key, value in remap.iteritems():
		for fc in fcs:
			output = os.path.join(arcpy.env.workspace, 
				'{}_reclass'.format(fc))
			if key != 'Soils' and key in fc:
				remap_range = RemapRange(value)
				rc = Reclassify(fc, 'Value', remap_range, 'NODATA')
				rc.save(output)
			if key == 'Soils' and key == fc:
				remap_value = RemapValue(value)
				rc = Reclassify(fc, 'Value', remap_value, 'NODATA')
				rc.save(output)

def add_members(fcs):
	algos = pickle.load(open('pickles/algos.p', 'rb'))
	for fc in fcs:
		if 'Streets' in fc:
			output = os.path.join(arcpy.env.workspace, '{}_fuzzy'.format(fc))
			fm = FuzzyMembership(fc, algos['linear'])
			fm.save(output)
		else:
			output = os.path.join(arcpy.env.workspace, '{}_fuzzy'.format(fc))
			fm = FuzzyMembership(fc, algos['small'])
			fm.save(output)
	members = [m for m in arcpy.ListRasters() if m.endswith('_fuzzy')]
	return members
	
def prepare_data():
	fcs = list_objects()
	for fc in fcs:
		if 'Streets' in fc or 'GreenSpaces' in fc: 
			distance(fc)
		if 'Soils' in fc:
			rasterize(fc)
		aspect(fc)
	reclassify(arcpy.ListRasters())
	data = [i for i in arcpy.ListRasters() if i.endswith('_reclass')]
	return data

def overlay():
	arcpy.env.compression = 'NONE'
	output = os.path.join(arcpy.env.workspace, 'SiteSuitability_Results')
	data = prepare_data()
	members = add_members(data)
	final_output = FuzzyOverlay(members, 'AND')
	final_output.save(output)

def main():
	arcpy.CheckOutExtension('spatial')
	source = raw_input('Path to Source Data Directory: ')
	create_output_gdb(source)
	overlay()
	arcpy.CheckInExtension('spatial')

if __name__ == '__main__':
	start_time = time.time()
	main()
	print '\nAnalysis Completed in {} seconds'.format(time.time() - start_time)
