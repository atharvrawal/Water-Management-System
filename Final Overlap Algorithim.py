import pandas as pd
from geopy.distance import geodesic

# Load the CSV files
df1 = pd.read_csv('bbmp_lakes_masterlist-final.csv')
df2 = pd.read_csv('flooding_vulnerable_locations.csv')

df2[['Longitude', 'Latitude']] = df2['WKT'].str.extract(r'POINT \((.*?) (.*?)\)')

# Convert the Longitude and Latitude columns to numeric
df2['Longitude'] = pd.to_numeric(df2['Longitude'])
df2['Latitude'] = pd.to_numeric(df2['Latitude'])

# Ensure the dataframes have 'Latitude' and 'Longitude' columns
assert 'Latitude' in df1.columns and 'Longitude' in df1.columns
assert 'Latitude' in df2.columns and 'Longitude' in df2.columns

# Create an empty dataframe to store the results
result_df = pd.DataFrame(columns=['average_latitude', 'average_longitude', 'Name_of_th', 'LocationName'])
print(result_df)

# Compare each pair of coordinates
for index1, row1 in df1.iterrows():
    for index2, row2 in df2.iterrows():
        coord1 = (row1['Latitude'], row1['Longitude'])
        coord2 = (row2['Latitude'], row2['Longitude'])
        
        # If the distance is less than or equal to 15km
        if geodesic(coord1, coord2).km <= 15:
            # Calculate the average coordinates
            avg_latitude = (row1['Latitude'] + row2['Latitude']) / 2
            avg_longitude = (row1['Longitude'] + row2['Longitude']) / 2
            
            # Create a temporary DataFrame for the new row
            new_row = pd.DataFrame({
                'average_latitude': [avg_latitude],
                'average_longitude': [avg_longitude],
                'Name_of_th': [row1['Name_of_th']],
                'LocationName': [row2['LocationName']]
            })
            
            # Add the new row to the DataFrame if it's not empty
            if not new_row.empty:
                result_df = result_df.combine_first(new_row)