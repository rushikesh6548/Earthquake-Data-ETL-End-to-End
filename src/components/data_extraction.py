import os
import sys
import pandas as pd
from src.logger import logging

class DataExtractionConfig():
    def __int__(self):
        if os.path.exists('all_data'):
            os.makedirs('all_data')
        self.raw_data_path = os.path.join('all_data','raw_data.csv')


class DataExtraction():
    def __int__(self):
        data_extraction_config_obj = DataExtractionConfig()
        self.raw_data_path = data_extraction_config_obj.raw_data_path

    def initiate_data_extraction(self):
        logging.info("Initiated data extraction from API")
        # extracting all data from API from year
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

        earthquake_df = pd.DataFrame()
        for year in range(2010, 2024):

            for month in range(1, 13):

                start_date = f"{year}-{month:02d}-01"
                end_date = f"{year}-{month:02d}-30"
                query_parameters = {
                    "format": "csv",
                    "starttime": start_date,
                    "endtime": end_date,
                    "minmagnitude": "3",
                    "limit": "20000"
                }
                # Hit the API and get the response
                response = requests.get(url, params=query_parameters)

                # If the response is successful, add the data to the earthquake_data DataFrame
                if response.status_code == 200:
                    # Convert the CSV string to a pandas DataFrame
                    csv_string = response.text
                    df = pd.read_csv(StringIO(csv_string), header=None)

                    # Assign column name

                    # Append the data to the earthquake_data DataFrame
                    earthquake_df = earthquake_df._append(df.iloc[1:, :])


        earthquake_df.columns = [
            "time", "latitude", "longitude", "depth", "mag", "magType",
            "nst", "gap", "dmin", "rms", "net", "id", "updated", "place",
            "type", "horizontalError", "depthError", "magError", "magNst",
            "status", "locationSource", "magSource"
        ]

        earthquake_df.to_csv(self.raw_data_path,header=True,index = False)


extraction_obj = DataExtraction()

