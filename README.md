# ExcelInterface
This version and input files work with 2DSOIL version 3.0.0 and Maizsim version 1.8.0 (uploaded 2/13/2023)

An excel based interface to create the input files needed for the crop models 
The input data are stored in an excel spreadsheet. 
A special Excel file contains VBA code to pull data from the spreadsheet and create the folder structure and input files needed to run maizsim. The VBA program generates grid1.bat files in each folder that will create the grid and soil files when run. Only the weather files are not created. 

the Models folder has the executables 
to run the model, use the root folder set in the excel interface.
let's say the root is d:/agmipet2 and under this are the data folders, run_01 and run_02
then the executables would go into the agmipet2 folder and you would run the model as
d:/agmipET2 > 2dmaizsim ./run_01/runrun01.dat
Still need to upload weathar files for the Solar Corridor simulation
