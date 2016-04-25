import arcpy

def reproj():
	out_crs = arcpy.SpatialReference(102387)
	fcs = arcpy.ListFeatureClasses()
	for fc in fcs:
		out_fc = '{}_projected'.format(fc)
		arcpy.Project_management(fc, out_fc, out_crs)

def clean():
	fcs = arcpy.ListFeatureClasses()
	for fc in fcs:
		if not fc.endswith('_projected'):
			arcpy.Delete_management(fc)
		arcpy.Rename_management(fc, fc.split('_')[0])
	
def main():
	w = r'D:\Documents\GIS\English Ivy Habitat Model\Data\Working_Data.gdb'
	arcpy.env.workspace = w
	reproj()
	clean()

if __name__ == '__main__':
	main()