# %% import libraries
from collections import Counter
import pandas as pd
import geopandas as gp
from geopy.geocoders import Nominatim
import statsmodels.api as sm
import statsmodels.formula.api as smf
import contextily as cx
import seaborn as sns
import json
import matplotlib.pyplot as plt
# %% read data
employer_data = (
    "https://data.london.gov.uk/download/gender-pay-gaps/"
    "42ab9dc1-08f5-4536-927d-ad4bfa59660a/"
    "pay-gaps-london-employers.csv"
)
df = pd.read_csv(employer_data, skiprows=1)
df.set_index("EmployerName", inplace=True)

# # %% geolocating companies
# # pass a custom user agent
# geolocator = Nominatim(user_agent="my_user_agent")
# # get locations
# # --+ to iterate
# employers = df.index
# adresses = df.loc[:, "Address"].to_list()
# # --+ my data
# coords = {}
# # --+ ... and loop
# for i, j in zip(employers, adresses):
#     clean_str = j.replace("\n|\t", " ").replace("  ", " ")
#     try:
#         location = geolocator.geocode(clean_str)
#         if (location.latitude is not None) & (location.longitude is not None):
#             coords[i] = {
#                 "Lat": location.latitude,
#                 "Long": location.longitude,
#             }
#         else:
#             pass
#     except:
#         print("Not finding a match!?")

# does gender pay gap change across industries?
# create covariates by manipulating SIC codes
# --+ remove obs with null values
df = df.loc[df["SicCodes"].notnull()]
# --+ 2 digit SIC codes
df.loc[:, "SicCodes_twod"] = df["SicCodes"].str[0:2]
# --+ business diversification
df.loc[:, "divers"] = [Counter(item)[","] + 1 for item in df.loc[:, "SicCodes"]]

# OLS estimation
# does gender pay gap change across industries and companies?
model1 = "DiffMeanHourlyPercent ~ C(SicCodes_twod)"
res = smf.ols(formula=model1, data=df).fit()
print(res.summary())
model2 = "DiffMeanHourlyPercent ~ C(divers) + C(EmployerSize) + C(SicCodes_twod)"
res = smf.ols(formula=model2, data=df.loc[df["EmployerSize"] != "Not Provided"]).fit()
print(res.summary())

# does gender pay gap change across different areas of the city?
# get a geopandas df
# --+ a bit of data wrangling

with open('coords.json', 'r') as f:
    coords = json.load(f)

df = pd.merge(
    df, pd.DataFrame(coords).T, left_index=True, right_index=True, how="inner"
)

#%%
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
ax = sns.scatterplot(df['Lat'], df['Long'])
plt.show()

#%%
df = df.loc[(df["Long"] < 25) & (df["Long"] > -1),]
df = df.loc[(df["Lat"] < 52) & (df["Lat"] > -52),]

#%%
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
ax = sns.scatterplot(df['Lat'], df['Long'])
plt.show()

# %%
db = gp.read_file(gp.datasets.get_path("nybb"))
db.crs
db_wm = db.to_crs(epsg=3857)
# db_wm.plot()

ax = db_wm.plot(color="red", alpha=0.5, figsize=(10, 10))
cx.add_basemap(ax, source=cx.providers.Esri.WorldImagery)

# %% and there we go
# slice data
# df = df.loc[(df["Long"] < 25) & (df["Long"] > -25),]
gdf = gp.GeoDataFrame(df, geometry=gp.points_from_xy(df.Long, df.Lat))
# set the coordinate reference systems
# gdf.set_crs("EPSG:3857", inplace=True)
# # check the coordinate reference systemm
# gdf.crs

# %%
gdf_geo = gdf.set_crs(epsg=4326)
gdf_wm = gdf_geo.to_crs(epsg=3857)
gdf_wm.crs

ax = gdf_wm.plot(color="red", alpha=0.2, figsize=(10, 10))
ax.axis("off")
cx.add_basemap(ax) #, source=cx.providers.OpenStreetMap.BlackAndWhite
# %%
gdf_geo = gdf.set_crs(epsg=4326)
gdf_wm = gdf_geo.to_crs(epsg=3857)
gdf_wm.crs

ax = gdf_wm.plot(c=gdf_wm["DiffMeanHourlyPercent"], figsize=(10,10), colormap="coolwarm")
ax.axis("off")
cx.add_basemap(ax)
# %%
