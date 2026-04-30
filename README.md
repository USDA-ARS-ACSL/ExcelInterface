# ExcelInterface

## What Is This For?

This repository provides an **Excel-based interface for creating input files for agricultural crop simulation models**. It simplifies the process of setting up and running simulations with:
- **2DSOIL** - A two-dimensional soil water, heat, and nutrient transport model
- **Maizsim** - A maize (corn) crop growth simulation model

### How It Works

The input data for your agricultural simulations are stored in an Excel spreadsheet. A special Excel file (`ExcelInterface/read plant files*.xlsm`) contains VBA macros that:
1. Read experimental data from your spreadsheet
2. Create the folder structure needed for model runs
3. Generate all required input files for Maizsim
4. Create batch files (`grid1.bat`) to generate grid and soil files

This version and input files work with 2DSOIL version 3.1.2.0 and Maizsim version 1.8.1 (uploaded 9/23/2025) 

### Repository Contents

| Folder | Description |
|--------|-------------|
| `ExcelInterface/` | VBA-enabled Excel files and supporting tools for creating input files |
| `CreateSoilFiles/` | Executables for generating soil property files (uses Rosetta model) |
| `Variable Documentation/` | Excel files documenting input variables and their meanings |
| `Example input/` | Working examples with real experimental data |
| `Models.zip` | Model executables (extract to use) |

### Working Examples

The `Example input/` folder contains published and in-progress examples:
- **Kansas** - Dryland maize (paper in progress)
- **MDEasternShore** - Maryland Eastern Shore (published in Kim et al., 2012)
- **AgmipET2** - From Kimball et al., https://doi.org/10.1016/j.agrformet.2023.109396
- **CO2_Respiration_CaseStudy1 & 2** - Tests of the CO2 model published in Geoderma (5/23/2024)
- **Tropical_Temperate_Study** - Comparison of maizsim for tropical and temperate locations (paper in review, 1/30/2026)

### Running the Model

To run the model, use the root folder set in the Excel interface.

**Example 1:** If your root is `d:/agmipet2` with data folders `run_01` and `run_02`:
- Place executables in the `agmipet2` folder
- Run: `d:/agmipET2 > 2dmaizsim ./run_01/runrun01.dat`

**Example 2:** Using the folder structure in this repository (`Y:\ExcelInterface`):
```
2dmaizsim ./"Example input/agmipET2/run_01/runrun_01.dat"
```

### Excel Interface Configuration

Your Excel interface paths would be configured as follows:
| Setting | Example Path |
|---------|--------------|
| Input Excel File | `Y:\ExcelInterface\Example input\AgmipET2\AGMIPET2Sim.xlsx` |
| Root Path | `Y:\ExcelInterface\Example input\AgmipET2` |
| MaizsimPath | `Y:\ExcelInterface` |
| CreateSoils | `Y:\ExcelInterface\CreateSoilFIles` |
| ExcelInterface | `Y:\ExcelInterface\ExcelInterface` |
| Weather CSV File Folder | `Y:\ExcelInterface\Example input\AgmipET2` |
