import requests
import pandas as pd
import json
import os


url = "https://data.cityofnewyork.us/resource/6v4b-5gp4.json"
page = requests.get(url)
converted = page.json()

# Pull your JSON data programmatically into your Python program, a
# and save this object into the path data/json.
# Parameters for the API request (limit the number of records per request)
params = {
    '$limit': 50000,  # Max limit per request
}

# Function to fetch all data with pagination
def fetch_all_data():
    all_data = []  # List to store all records
    offset = 0  # Starting point (offset)

    while True:
        # Add the current offset to the parameters
        params['$offset'] = offset

        # Send the request to the API
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            # If there is no data in the response, stop the loop
            if not data:
                break

            # Append the data to the all_data list
            all_data.extend(data)

            # Print progress (optional, for debugging)
            print(f"Fetched {len(data)} records, Total: {len(all_data)}")

            # Increase the offset by the limit for the next page
            offset += 50000
        else:
            print(f"Error fetching data: {response.status_code}")
            break

    return all_data

# Fetch all data with pagination
all_data = fetch_all_data()

# Convert the data into a pandas DataFrame
df = pd.DataFrame(all_data)


data_folder_csv = 'csv'
os.makedirs(data_folder_csv, exist_ok=True)  # Ensure the folder exists
csv_path = os.path.join(data_folder_csv, 'nyc_all_parks_special_event.csv')

# Save the DataFrame to a CSV file in the 'data/csv' folder
df.to_csv(csv_path, index=False)

### dropping unwanted columns 
to_drop = ["event_name","source","group_name_partner","unit","locationtype"]
df = df.drop(to_drop, axis=1)



#Converting our time 

df['date_and_time'] = pd.to_datetime(df['date_and_time'])

df['date'] = df['date_and_time'].dt.date
df['time'] = df['date_and_time'].dt.time

#dropping date_and_time columns as we separated these into 2 columns 
df = df.drop("date_and_time" ,  axis = 1)

df = df.sort_values(by= 'date')
df = df.set_index('date')

data_folder_csv = 'csv'
os.makedirs(data_folder_csv, exist_ok=True)  # Ensure the folder exists
csv_path = os.path.join(data_folder_csv, 'nyc_all_parks_filtered.csv')

# Save the DataFrame to a CSV file in the 'data/csv' folder
df.to_csv(csv_path, index= True)

print(df.head(14))


#df = df.groupby('audience').filter(lambda x: len(x) > 123)
