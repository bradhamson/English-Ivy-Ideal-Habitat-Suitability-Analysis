==================
Automated Analysis
==================

--------
Contents
--------
* json/remap.json
* pickles/algos.p
* reproject.py
* suitability_analysis.py

-----------
Description
-----------
This site suitability analysis has been completely automated using
the above scripts and resources.

The ``reproject.py`` script was initially used to reproject all of the 
source data to CRS: 102387. This is no longer needed since the 
``suitability_analysis.py`` script includes this functionality.

The ``suitability_analysis.py`` script has been developed to automate
the data management and analysis portions of this project. Reclassification is performed by reading from the ``remap.json`` file and feeding the values into ESRI's ``Remap`` objects instead of using their infotable methods. Make sure to keep this directory structure when running the analysis.

Source data is provided as shapefiles in the ``Data/Sources`` directory.

The script performs the following actions:

**Data Management**

* Creates an empty ``working_data.gdb`` file geodatabase
* Loads the data in ``Data/Sources`` into the fgdb
* Reprojects the data to the correct CRS
* Removes the old unprojected feature classes

**Analysis**

* Creates distance surfaces for the Streets and GreenSpaces features
* Rasterizes the Soils feature class
* Generates an Aspect Surface from the DEM
* Reclassifies the raster datasets
* Applies the correct Fuzzy Membership algorithms to the raster datasets
* Performs the Fuzzy Overlay Analysis using the rasters in the Fuzzy Membership set

---
Use
---
To use the script first download the Baltimore 1 meter DEM `here <https://www.dropbox.com/s/j7x2ips8donvpd2/BaltimoreCity_DEM_2015_0.7m.7z?dl=0>`_
and place it in the ``Data/Sources`` directory.

Then run the script from your shell and enter the source path when prompted.