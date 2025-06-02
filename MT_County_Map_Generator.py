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



