# Detailed Methodology

## Step 0: Project Setup
- Folder structure: RawData\ and SolarAnalysis.gdb
- Coordinate system: NAD83 / UTM Zone 12N (WKID: 26912)
- Cell size: 30 meters throughout

## Step 1: Maricopa County Boundary
- Downloaded Arizona counties from Census TIGER/Line 2023
- Select by Attribute: NAME = 'Maricopa'
- Exported to SolarAnalysis.gdb as Maricopa_Boundary

## Step 2: DEM Processing
- Downloaded USGS 1 arc-second elevation tiles covering Maricopa County
- Mosaic to New Raster: Pixel Type 32-bit float, 1 band
- Output: DEM_Mosaic → clipped to DEM_Maricopa

## Step 3: Solar Irradiance Processing
- Downloaded NREL NSRDB TMY-2024 GHI data
- Received 1,249 individual hourly CSV files
- Processed with Solar_GHI_Processor.py:
  - Extracted lat/lon from row 2 of each file
  - Averaged 8,760 hourly GHI readings per location
  - Output: Solar_GHI_Points.csv (21 unique grid points)
- Imported to ArcGIS Pro via XY Table to Point (GCS WGS 1984)
- IDW Interpolation: Z field = Avg_GHI, cell size = 30m
- Output: Solar_Maricopa

## Step 4: Clip All Layers to Maricopa Boundary
All layers clipped using Clip Raster (rasters) and Clip (vectors).
Critical setting: "Use Input Features for Clipping Geometry" checked.
Snap Raster environment set to DEM before all processing.

| Input | Output | Tool |
|-------|--------|------|
| DEM_Mosaic | DEM_Maricopa | Clip Raster |
| NLCD national | NLCD_Maricopa | Clip Raster |
| Solar IDW | Solar_Maricopa | Clip Raster |
| Transmission Lines | Trans_Maricopa | Clip |
| AZ_Wetlands | Wetlands_Maricopa | Clip |
| AZ_Riparian | Riparian_Maricopa | Clip |
| PAD-US Combined | Protected_Maricopa | Clip |

## Step 5: Derive Slope
- Tool: Slope
- Input: DEM_Maricopa
- Output measurement: Degree
- Z Factor: 1 (DEM and coordinate system both in meters)
- Output: Slope_Maricopa

## Step 6: Euclidean Distance
- Tool: Distance Accumulation
- Run twice:
  - Trans_Maricopa → Dist_Trans_Maricopa (max ~51,639m)
  - Roads → Dist_Roads_Maricopa (max ~91,773m)
- Cell size: 30m both runs

## Step 7: Reclassification
All layers converted to 1-9 suitability scale using Reclassify tool.

### Slope (Reclass_Slope)
| Start | End | Score |
|-------|-----|-------|
| 0 | 2 | 9 |
| 2 | 5 | 7 |
| 5 | 8 | 5 |
| 8 | 12 | 3 |
| 12 | 15 | 2 |
| 15 | 90 | 1 |

### Transmission Distance (Reclass_Trans)
| Start (m) | End (m) | Score |
|-----------|---------|-------|
| 0 | 500 | 9 |
| 500 | 1500 | 8 |
| 1500 | 3000 | 6 |
| 3000 | 5000 | 4 |
| 5000 | 10000 | 2 |
| 10000 | 51639 | 1 |

### Road Distance (Reclass_Roads)
| Start (m) | End (m) | Score |
|-----------|---------|-------|
| 0 | 500 | 9 |
| 500 | 2000 | 7 |
| 2000 | 5000 | 5 |
| 5000 | 10000 | 3 |
| 10000 | 91773 | 1 |

### Solar Irradiance (Reclass_Solar)
Based on actual Maricopa County data range (234-251 W/m²)
| Start (W/m²) | End (W/m²) | Score |
|-------------|------------|-------|
| 234 | 237 | 1 |
| 237 | 240 | 3 |
| 240 | 243 | 5 |
| 243 | 246 | 7 |
| 246 | 251 | 9 |

## Step 8: Weighted Overlay
- Tool: Weighted Overlay
- Scale: 1-9
- Weights: Solar 40%, Slope 25%, Transmission 25%, Roads 10%
- Output: Weighted_Maricopa / Suitability_Final

## Key Findings
- Highest suitability corridors follow transmission lines 
  through flat Sonoran Desert
- Maricopa solar irradiance uniformly high (234-250 W/m²)
- Northeast corner (Tonto National Forest) lowest scoring
- Phoenix metro core excluded by urban development scoring
