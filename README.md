# Solar Farm Site Suitability Analysis
## Maricopa County, Arizona | ArcGIS Pro

![GIS](https://img.shields.io/badge/Software-ArcGIS%20Pro-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## Project Overview
A complete GIS site suitability analysis identifying optimal locations 
for utility-scale solar farm development in Maricopa County, Arizona. 
This project follows industry-standard weighted overlay methodology 
used by solar developers, environmental consultants, and government 
planners.

**Study Area:** Maricopa County, Arizona  
**Software:** ArcGIS Pro 3.x  
**Coordinate System:** NAD83 / UTM Zone 12N (WKID: 26912)  
**Cell Size:** 30 meters  

---

## Methodology

### Criteria & Weights
| Criterion | Weight | Justification |
|-----------|--------|---------------|
| Solar Irradiance (GHI) | 40% | Directly determines energy output and revenue |
| Terrain Slope | 25% | Primary construction cost driver |
| Transmission Line Proximity | 25% | Largest variable development cost |
| Road Proximity | 10% | Access for construction and maintenance |

### Hard Exclusion Layers
- Wetlands — Protected under Clean Water Act
- Riparian Areas — Environmentally sensitive corridors
- Protected Areas (PAD-US) — National parks, BLM wilderness, monuments

---

## Data Sources
All datasets are free and publicly available from US government sources.

| Dataset | Source | Link |
|---------|--------|------|
| County Boundary | US Census TIGER/Line 2023 | [Download](https://www.census.gov/cgi-bin/geo/shapefiles/index.php) |
| DEM (Elevation) | USGS National Map | [Download](https://apps.nationalmap.gov/downloader) |
| Land Cover (NLCD) | MRLC | [Download](https://www.mrlc.gov/data) |
| Transmission Lines | USGS ScienceBase | [Download](https://www.sciencebase.gov/catalog/item/54383f29e4b08a816ca6376a) |
| Roads | US Census TIGER/Line 2023 | [Download](https://www.census.gov/cgi-bin/geo/shapefiles/index.php) |
| Wetlands | USFWS NWI | [Download](https://www.fws.gov/program/national-wetlands-inventory/wetlands-mapper) |
| Protected Areas | PAD-US via ProtectedLands.net | [Download](https://www.protectedlands.net/how-to-get-pad-us) |
| Solar Irradiance | NREL NSRDB TMY-2024 | [Download](https://nsrdb.nrel.gov/data-viewer) |

---

## Workflow Summary
```
1. Download & clip all 8 datasets to Maricopa County boundary
2. Mosaic DEM tiles → derive Slope
3. Process 1,249 NREL solar CSV files with Python → IDW interpolation
4. Run Euclidean Distance on transmission lines and roads
5. Reclassify all layers to 1-9 suitability scale
6. Weighted Overlay → combine all criteria
7. Apply exclusion mask (wetlands, protected areas)
8. Export final suitability map
```

---

## Reclassification Scheme

### Slope
| Range (degrees) | Score | Meaning |
|----------------|-------|---------|
| 0 - 2 | 9 | Flat — ideal for solar |
| 2 - 5 | 7 | Gentle — very buildable |
| 5 - 8 | 5 | Moderate — added cost |
| 8 - 12 | 3 | Steep — significant grading |
| 12 - 15 | 2 | Very steep — expensive |
| 15 - 90 | 1 | Not viable |

### Transmission Line Distance
| Range (meters) | Score |
|---------------|-------|
| 0 - 500 | 9 |
| 500 - 1,500 | 8 |
| 1,500 - 3,000 | 6 |
| 3,000 - 5,000 | 4 |
| 5,000 - 10,000 | 2 |
| 10,000+ | 1 |

### Solar Irradiance (Maricopa actual range)
| Range (W/m²) | Score |
|-------------|-------|
| 246 - 251 | 9 |
| 243 - 246 | 7 |
| 240 - 243 | 5 |
| 237 - 240 | 3 |
| 234 - 237 | 1 |

---

## Python Automation
Solar irradiance data from NREL is delivered as 1,000+ individual 
hourly CSV files. A Python script was developed to automate processing:
- Loops through all CSV files
- Extracts latitude, longitude, and averages 8,760 hourly GHI readings
- Outputs a single clean CSV ready for ArcGIS Pro XY import

See [`Solar_GHI_Processor.py`](Solar_GHI_Processor.py) for the full script.

---

## Key Findings
- Highest suitability areas follow transmission line corridors 
  through flat Sonoran Desert terrain
- Maricopa County shows uniformly high solar irradiance 
  (234-250 W/m²) confirming excellent solar potential county-wide
- Northeast corner (Tonto National Forest) scores lowest due to 
  steep terrain, remoteness, and protected status
- Phoenix metro core scores low due to existing urban development

---

## Files in this Repository
| File | Description |
|------|-------------|
| `README.md` | Project overview and methodology |
| `Solar_GHI_Processor.py` | Python script for processing NREL solar CSV files |
| `methodology.md` | Detailed step-by-step workflow |
| `data_sources.md` | Verified working government data links |

---

## Skills Demonstrated
- GIS site suitability analysis
- Weighted overlay methodology
- Raster analysis (Slope, Euclidean Distance, IDW Interpolation, Reclassify)
- Python automation with ArcPy
- Government data acquisition and troubleshooting
- Multi-criteria decision analysis
- ArcGIS Pro map layout and cartography

---

## Author
**Isai Montes**  
GIS Analyst  
[GitHub](https://github.com/Isai-Montes)
