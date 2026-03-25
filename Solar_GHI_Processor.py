import os
import csv

# =============================================================
# SOLAR IRRADIANCE CSV PROCESSOR
# For use with NREL NSRDB downloaded data
# Converts 1,000+ hourly CSV files into a single point CSV
# ready to import into ArcGIS Pro as XY data
# =============================================================
# INSTRUCTIONS:
# 1. Download solar data from https://nsrdb.nrel.gov/data-viewer
#    - Dataset: Typical Meteorological Year (TMY)
#    - Year: tmy-2024
#    - Attribute: GHI only
#    - Draw polygon over your study area
#    - Hit Download (files sent to your email)
# 2. Unzip all CSV files into ONE folder
# 3. Update the two paths below
# 4. Run this script in ArcGIS Pro Python Window
#    (View > Python Window) or any Python environment
# 5. Output CSV will have 3 columns: Latitude, Longitude, Avg_GHI
# 6. Bring into ArcGIS Pro via Map > Add Data > XY Point Data
#    X Field: Longitude | Y Field: Latitude | CS: GCS_WGS_1984
# =============================================================

# *** INSERT YOUR FOLDER PATH HERE ***
# This is the folder containing all your downloaded CSV files
# Example Windows path: r'C:\GIS_Projects\SolarData\CSV_Files'
# Example: r'D:\MyProject\NREL_Downloads\solar_csvs'
input_folder = r'INSERT YOUR CSV FOLDER PATH HERE'

# *** INSERT YOUR OUTPUT FILE PATH HERE ***
# This is where the final single CSV will be saved
# Include the filename at the end: Solar_GHI_Points.csv
# Example: r'C:\GIS_Projects\SolarAnalysis.gdb\Solar_GHI_Points.csv'
output_file = r'INSERT YOUR OUTPUT FILE PATH HERE\Solar_GHI_Points.csv'

# =============================================================
# DO NOT EDIT BELOW THIS LINE
# =============================================================

print("Starting solar CSV processing...")
print(f"Reading from: {input_folder}")
print(f"Output will be saved to: {output_file}")
print("")

results = []
processed = 0
skipped = 0

for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        filepath = os.path.join(input_folder, filename)
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()

                # Row 2 contains metadata including lat/lon
                meta = lines[1].strip().split(',')
                lat = float(meta[5])   # Column 6 = Latitude
                lon = float(meta[6])   # Column 7 = Longitude

                # Row 4 onward contains hourly GHI readings
                ghi_values = []
                for line in lines[3:]:
                    parts = line.strip().split(',')
                    if len(parts) >= 6:
                        try:
                            ghi_values.append(float(parts[5]))
                        except ValueError:
                            pass  # Skip blank or non-numeric rows

                # Calculate annual average GHI for this location
                if ghi_values:
                    avg_ghi = sum(ghi_values) / len(ghi_values)
                    results.append([lat, lon, round(avg_ghi, 2)])
                    processed += 1

        except Exception as e:
            print(f"  Skipped {filename}: {e}")
            skipped += 1

# Write all results to single output CSV
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Latitude', 'Longitude', 'Avg_GHI'])
    writer.writerows(results)

print(f"Done!")
print(f"  Files processed: {processed}")
print(f"  Files skipped:   {skipped}")
print(f"  Solar points in output: {len(results)}")
print(f"  Output saved to: {output_file}")
print("")
print("Next steps in ArcGIS Pro:")
print("  1. Map > Add Data > XY Point Data")
print("  2. Table: Solar_GHI_Points.csv")
print("  3. X Field: Longitude")
print("  4. Y Field: Latitude")
print("  5. Coordinate System: GCS_WGS_1984")
print("  6. Then run IDW interpolation on the points layer")
