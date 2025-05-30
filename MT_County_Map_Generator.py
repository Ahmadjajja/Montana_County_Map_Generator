# # 3 Coloring basic logic
# # Code for custom own .shp file

# import geopandas as gpd
# import matplotlib.pyplot as plt
# import pandas as pd

# # Load shapefile
# montana = gpd.read_file("MontanaCounties_shp/County.shp")

# # Normalize county name column from shapefile
# montana.columns = montana.columns.str.strip()
# montana["County"] = montana["NAME"].str.strip().str.lower()  # ✅ Adjust if column is not NAME

# # Read and normalize Excel
# df = pd.read_excel("Count list file.xlsx")
# df.columns = df.columns.str.strip()
# df["County"] = df["County"].str.strip().str.lower()  # ✅ Make lowercase for match

# # Default color
# montana["Color"] = "white"

# # Color logic
# for _, row in df.iterrows():
#     county = row["County"]
#     if county in list(montana["County"]):
#         if "Blue" in row and str(row["Blue"]).lower() == "x":
#             montana.loc[montana["County"] == county, "Color"] = "blue"
#         elif "Red" in row and str(row["Red"]).lower() == "x":
#             montana.loc[montana["County"] == county, "Color"] = "red"
#         elif "Green" in row and str(row["Green"]).lower() == "x":
#             montana.loc[montana["County"] == county, "Color"] = "green"

# # Plot
# fig, ax = plt.subplots(figsize=(10, 10))
# montana.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
# montana.plot(ax=ax, color=montana["Color"], alpha=0.6)

# # # Annotate
# # for _, row in montana.iterrows():
# #     plt.annotate(
# #         row["County"].title(),  # Show with capitalized name
# #         (row.geometry.centroid.x, row.geometry.centroid.y),
# #         ha="center", fontsize=7
# #     )

# plt.title("Montana County Bee Species Map", fontsize=14)
# plt.axis("off")
# plt.tight_layout()
# plt.savefig("montana_bee_species_map.tiff", format="tiff", dpi=300)
# plt.show()


# # logic for 2 coloring
# import geopandas as gpd
# import matplotlib.pyplot as plt
# import pandas as pd

# # Load Montana county shapefile
# montana = gpd.read_file("MontanaCounties_shp/County.shp")

# # Normalize shapefile columns
# montana.columns = montana.columns.str.strip()
# montana["County"] = montana["NAME"].str.strip().str.lower()

# # Load Excel (targeting the "Summary" sheet)
# df = pd.read_excel("Bombus records test-Ahmad.xlsx", sheet_name=0)
# # df = pd.read_excel("All MT bumble bees-databases combined-Ahmad.xlsx", sheet_name=0)
# df.columns = df.columns.str.strip()

# # Detect county column
# county_col = next((col for col in df.columns if 'county' in col.lower()), None)
# if not county_col:
#     raise ValueError("❌ 'County' column not found.")

# # Normalize Excel county values
# df["County"] = df[county_col].astype(str).str.strip().str.lower()

# # Keep Montana counties only
# df = df[df["County"].isin(set(montana["County"]))]

# # Default color is white
# montana["Color"] = "white"

# # Color logic: Post = red, Pre = grey
# if "Pre vs. Post" in df.columns:
#     post, pre = 0, 0
#     for _, row in df.iterrows():
#         val = str(row["Pre vs. Post"]).strip().lower()
#         if val == "post":
#             print("post runs...", val)
#             post += 1
#             montana.loc[montana["County"] == row["County"], "Color"] = "red"
#         elif val == "pre":
#             montana.loc[montana["County"] == row["County"], "Color"] = "grey"
#             pre += 1
#     print("post count: ", post)
#     print("pre count: ", pre)

# # Plot
# fig, ax = plt.subplots(figsize=(10, 10))
# montana.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
# montana.plot(ax=ax, color=montana["Color"], alpha=0.6)

# # Show color count at bottom
# counts = montana["Color"].value_counts()
# text = "\n".join(f"{k.title()}: {v}" for k, v in counts.items())
# plt.figtext(0.5, 0.01, f"Color Summary:\n{text}", ha="center", fontsize=10)

# plt.title("Montana Bee Species (Pre vs. Post)", fontsize=14)
# plt.axis("off")
# plt.tight_layout()
# plt.savefig("montana_bee_species_map.tiff", format="tiff", dpi=300)
# plt.show()


# Correct logic

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load shapefile
montana = gpd.read_file("MontanaCounties_shp/County.shp")
montana.columns = montana.columns.str.strip()
montana["County"] = montana["NAME"].str.strip().str.lower()

# Read Excel, specify sheet, and clean
df = pd.read_excel("All MT bumble bees-databases combined-Ahmad.xlsx", sheet_name=0)
df.columns = df.columns.str.strip()
df["county"] = df["county"].astype(str).str.strip().str.lower()
df["Pre vs. Post"] = df["Pre vs. Post"].astype(str).str.strip().str.lower()

# Initialize color column
montana["Color"] = "white"

# Color logic: count per county
for county_name in df["county"].unique():
    county_data = df[df["county"] == county_name]
    pre_count = (county_data["Pre vs. Post"] == "pre").sum()
    post_count = (county_data["Pre vs. Post"] == "post").sum()

    if county_name in list(montana["County"]):
        if post_count >= pre_count:
            montana.loc[montana["County"] == county_name, "Color"] = "red"
        elif pre_count > post_count:
            montana.loc[montana["County"] == county_name, "Color"] = "gray"

# Plot
fig, ax = plt.subplots(figsize=(11, 10))
montana.boundary.plot(ax=ax, linewidth=1, edgecolor="black")
montana.plot(ax=ax, color=montana["Color"], alpha=0.65)

# Count summary
red_count = (montana["Color"] == "red").sum()
gray_count = (montana["Color"] == "gray").sum()
white_count = (montana["Color"] == "white").sum()

# Annotate
for _, row in montana.iterrows():
    plt.annotate(
        row["County"].title(),  # Show with capitalized name
        (row.geometry.centroid.x, row.geometry.centroid.y),
        ha="center", fontsize=7
    )

plt.title("Montana County - Pre vs. Post Bee Sampling", fontsize=15)
plt.figtext(0.5, 0.02, f"Post (red): {red_count}    Pre (gray): {gray_count}    Unmatched (white): {white_count}", 
            ha="center", fontsize=12)
plt.axis("off")
plt.tight_layout()
plt.savefig("montana_pre_post_map.tiff", format="tiff", dpi=300)
plt.show()
