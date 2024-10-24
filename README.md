# ExcelInterface
This version and input files work with 2DSOIL version 3.1.0.0 and Maizsim version 1.8.0 (uploaded 2/23/2023)

An excel based interface to create the input files needed for the crop models 
The input data are stored in an excel spreadsheet. 
A special Excel file contains VBA code to pull data from the spreadsheet and create the folder structure and input files needed to run maizsim. The VBA program generates grid1.bat files in each folder that will create the grid and soil files when run. Only the weather files are not created. 

the Models folder has the executables 

Working examples include data for Kansas dryland (paper in progress), Maryland Eastern Shore (published in Kim et al., 2012) 
and AgmipET2 from a paper by Kimball et al, now in press

Newly added are the input and output files for maizsim where we published tests of the CO2 model in Geoderma

To run the model, use the root folder set in the excel interface.
let's say the root is d:/agmipet2 and under this are the data folders, run_01 and run_02
then the executables would go into the agmipet2 folder and you would run the model as
d:/agmipET2 > 2dmaizsim ./run_01/runrun01.dat

if you use the folder structure in this repository:
Y:\ExcelInterface
you would run the model as:
2dmaizsim ./"Example input/agmipET2/run_01/runrun_01.dat"
Your files would be set up this way in the interface:
Input excel file:	Y:\ExcelInterface\Example input\AgmipET2\AGMIPET2Sim.xlsx
Root Path:	Y:\ExcelInterface\Example input\AgmipET2
MaizsimPath	Y:\ExcelInterface
CreateSoils	Y:\ExcelInterface\CreateSoilFIles
ExcelInterface	Y:\ExcelInterface\ExcelInterface
Weather CSV File Folder	Y:\ExcelInterface\Example input\AgmipET2
