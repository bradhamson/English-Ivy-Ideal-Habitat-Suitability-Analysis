==============================================
English Ivy Ideal Habitat Suitability Analysis
==============================================

-----------
Description
-----------
English Ivy is an exotic invasive plant brought to the US as an ornamental ivy but has aggressivly spread
beyond its decrative purpose to choke out native species, create ivy deserts, and damage property and entire ecosystems. 

-------
Purpose
-------
This English Ivy Ideal Habitat Suitability Analysis seeks to identify areas within Baltimore, MD that may be ideal
english ivy habitats in order to create target areas for invasive removal efforts.

------
Method
------
Data was collected from a variety of sources to create the necessary surfaces to perform this analysis. These include
the MD state government, USGS, and the Baltimore city government. 

In order to proceed a model of the ideal habitat was created:

Ideal Habitat:

* Within 50ft of edge areas 
* Soil is not extremely wet
* Slightly sunny to shady light
* Surrounded by deciduous trees

Due to the number of datasources and their disparate schemas, normalization was necessary. This process
was automated using Python scripts and Raster reclassification.

A Fuzzy Overlay Analysis was used to discover areas ideal habitats since the ivasive species are not contained by discrete boundaries.

First an Aspect surface was generated using the 1m DEM. This was then reclassified to highlight shady and slightly sunny areas (North and North East facing).
Next a surface was generated higlighting areas within 50ft of paved roadways using the Euclidean Distance Tool.
After this the STATSGO Soils Coverage was converted 

-------
Results
-------

------------
Data Sources
------------

* MD Imap - Baltiore DEM
* Baltimore City - Boundary, Green Spaces, Roadways
* USDA - Mid Atlantic Soils
Soil Survey Staff, Natural Resources Conservation Service, United States Department of Agriculture. Web Soil Survey. `Available online at http://websoilsurvey.nrcs.usda.gov/`_. Accessed [4/22/2016].

-------
Contact
-------
* Stephanie Helms - Baltimore City Invasive Species Program Coordinator
* Brad Hamson - GIS Analys/Developer

* stephaniem.helms@gmail.com
* brad.hamson@gmail.com

-------
Licence
-------
GPL v3