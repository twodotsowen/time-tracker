# time-tracker

track time based on category for prioritization analysis

## Setup Instructions
1. Fill out legend with the labels you want in the format {HOTKEY}:{label}:{colorR, colorB, colorG}
2. Create `subcategories` file and fill out lines with labels from the legend and then subcats, in the format {label}:{subCat0},{subCat1},...{subCatK}

## Usage 
- Run the program with `python time_track.py`, use the hotkeys to switch to new tasks as you start working on them
- see results for a given week with `report_time.py` and `plot_time.py`
