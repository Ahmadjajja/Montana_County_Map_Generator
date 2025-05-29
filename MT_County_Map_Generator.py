# # Code for downloaded .shp file

# import geopandas as gpd
# import matplotlib.pyplot as plt
# import pandas as pd

# # Load the US counties shapefile
# gdf = gpd.read_file("shapefiles/cb_2021_us_county_5m.shp")
# # gdf = gpd.read_file("MontanaCounties_shp/County.shp")

# # Filter only Montana counties
# montana = gdf[gdf["STATEFP"] == "30"].copy()

# # Read Excel and clean column names
# df = pd.read_excel("Count list file.xlsx")
# df.columns = df.columns.str.strip()  # ✅ Fix: strip column names
# df['County'] = df['County'].str.strip()

# # Initialize default color
# montana["Color"] = "lightgrey"

# # Apply coloring logic
# for _, row in df.iterrows():
#     county = row["County"]
#     if county in list(montana["NAME"]):
#         if "Blue" in row and str(row["Blue"]).lower() == "x":
#             montana.loc[montana["NAME"] == county, "Color"] = "blue"
#         elif "Red" in row and str(row["Red"]).lower() == "x":
#             montana.loc[montana["NAME"] == county, "Color"] = "red"
#         elif "Green" in row and str(row["Green"]).lower() == "x":
#             montana.loc[montana["NAME"] == county, "Color"] = "green"

# # # Plot the result
# # fig, ax = plt.subplots(figsize=(10, 10))
# # montana.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
# # montana.plot(ax=ax, color=montana["Color"], alpha=0.6)

# # # Annotate county names
# # for _, row in montana.iterrows():
# #     plt.annotate(
# #         row["NAME"],
# #         (row.geometry.centroid.x, row.geometry.centroid.y),
# #         ha="center", fontsize=7
# #     )

# # plt.title("Montana County Bee Species Map", fontsize=14)
# # plt.axis("off")
# # plt.tight_layout()
# # plt.show()


# # Plot the result
# fig, ax = plt.subplots(figsize=(10, 10))
# montana.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
# montana.plot(ax=ax, color=montana["Color"], alpha=0.6)

# # Annotate county names
# for _, row in montana.iterrows():
#     plt.annotate(
#         row["NAME"],
#         (row.geometry.centroid.x, row.geometry.centroid.y),
#         ha="center", fontsize=7
#     )

# plt.title("Montana County Bee Species Map", fontsize=14)
# plt.axis("off")
# plt.tight_layout()

# # ✅ Save as TIFF
# plt.savefig("Montana_Bee_Species_Map.tiff", format="tiff", dpi=300)

# # Show plot
# plt.show()



# Code for custom own .shp file

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Load shapefile
montana = gpd.read_file("MontanaCounties_shp/County.shp")

# Normalize county name column from shapefile
montana.columns = montana.columns.str.strip()
montana["County"] = montana["NAME"].str.strip().str.lower()  # ✅ Adjust if column is not NAME

# Read and normalize Excel
df = pd.read_excel("Count list file.xlsx")
df.columns = df.columns.str.strip()
df["County"] = df["County"].str.strip().str.lower()  # ✅ Make lowercase for match

# Default color
montana["Color"] = "white"

# Color logic
for _, row in df.iterrows():
    county = row["County"]
    if county in list(montana["County"]):
        if "Blue" in row and str(row["Blue"]).lower() == "x":
            montana.loc[montana["County"] == county, "Color"] = "blue"
        elif "Red" in row and str(row["Red"]).lower() == "x":
            montana.loc[montana["County"] == county, "Color"] = "red"
        elif "Green" in row and str(row["Green"]).lower() == "x":
            montana.loc[montana["County"] == county, "Color"] = "green"

# Plot
fig, ax = plt.subplots(figsize=(10, 10))
montana.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
montana.plot(ax=ax, color=montana["Color"], alpha=0.6)

# # Annotate
# for _, row in montana.iterrows():
#     plt.annotate(
#         row["County"].title(),  # Show with capitalized name
#         (row.geometry.centroid.x, row.geometry.centroid.y),
#         ha="center", fontsize=7
#     )

plt.title("Montana County Bee Species Map", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.savefig("montana_bee_species_map.tiff", format="tiff", dpi=300)
plt.show()

