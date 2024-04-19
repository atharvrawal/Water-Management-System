# prompt: get latitude and longititude coordinates from two different csv files and check the ones in 15km range of each other
# where to upload file from

import pandas as pd
import pandas as pd
from haversine import haversine, Unit
# Read the first CSV file
df1 = pd.read_csv('bbmp_lakes_masterlist-final.csv')

# Read the second CSV file
df2 = pd.read_csv('flooding_vulnerable_locations.csv')

# Extract latitude and longitude columns from both DataFrames
lat1 = df1['latitude']
lon1 = df1['longitude']

lat2 = df2['latitude']
lon2 = df2['longitude']

# Calculate the distance between each pair of coordinates
distances = []
for i in range(len(lat1)):
  for j in range(len(lat2)):
    distance = haversine(df1.iloc[i][['latitude', 'longitude']], df2.iloc[j][['latitude', 'longitude']], unit=Unit.KILOMETERS)
    distances.append(distance)

# Find the pairs of coordinates that are within 15km of each other
close_pairs = []
for i, distance in enumerate(distances):
  if distance <= 15:
    close_pairs.append((df1.iloc[i], df2.iloc[j]))

# Print the close pairs of coordinates
for pair in close_pairs:
  print(f"({pair[0]['latitude']}, {pair[0]['longitude']}), ({pair[1]['latitude']}, {pair[1]['longitude']})")

# Function to calculate the distance between two coordinates
def haversine_distance(lat1, lon1, lat2, lon2):
  R = 6371  # Earth's radius in kilometers
  dlat = degrees_to_radians(lat2 - lat1)
  dlon = degrees_to_radians(lon2 - lon1)
  a = sin(dlat / 2) ** 2 + cos(degrees_to_radians(lat1)) * cos(degrees_to_radians(lat2)) * sin(dlon / 2) ** 2
  c = 2 * asin(sqrt(a))
  return R * c

# Function to convert degrees to radians
def degrees_to_radians(degrees):
  return degrees * (pi / 180)
