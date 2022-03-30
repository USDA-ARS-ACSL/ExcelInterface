# ExcelInterface
This version and input files work with 2DSOIL version 1.6.5 and Maizsim version 1.6.0 (uploaded 3/29/2022)

An excel based interface to create the input files needed for the crop models 
The input data are stored in an excel spreadsheet. A special Excel file contains VBA code to pull data from the spreadsheet and create the folder structure and input files needed to run maizsim. The VBA program generates grid1.bat files in each folder that will create the grid and soil files when run. Only the weather files are not created. 

Still need to upload wethar files for the Solar Corridor simulation
