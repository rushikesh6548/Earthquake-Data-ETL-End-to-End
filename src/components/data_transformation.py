import os
import pandas as pd
from sklearn.impute import KNNImputer
import numpy as np

class Preprocessing():
    def __init__(self):
        self.raw_data_path = os.path.join('all_data','raw_data_excel.xlsx')
        self.preprocessed_data  = None


    def preprocess_data(self):
        # Reading the data that we got from data extraction process:
        data = pd.read_excel(f'{self.raw_data_path}',index_col=False)
        print(data)


        numeric_col = data.select_dtypes(include='float64')

        print(numeric_col)

        knn = KNNImputer(n_neighbors=5)

        numeric_col_imputed = knn.fit_transform(numeric_col)
        print(f"Numeric_col_imputed : \n{numeric_col_imputed}")

        numeric_col_imputed_data = pd.DataFrame(numeric_col_imputed,columns=numeric_col.columns)

        print(f"Numeric_col_imputed_Df : \n{numeric_col_imputed_data}")

        data.loc[numeric_col.index,numeric_col.columns] = numeric_col_imputed_data

        print(f"Data with numeric things imputed : \n{data}")

        data = data.dropna(subset=['magType'])
        data = data.dropna(subset=['place'])

        print(f"Data with all things imputed : \n {data}")

        data.to_csv("all_data/preprocessed_data.xlsx")

        return data 




class DataTransformation():
    def __init__(self):
        preprocessing_obj = Preprocessing()
        self.preprocessed_data = preprocessing_obj.preprocess_data()

    def transform(self):
        data = self.preprocessed_data
        data['time'] = pd.to_datetime(data['time'])

        # Transforming data according to Star Schema :
        data = data.drop_duplicates().reset_index(drop=True)
        data['earthquake_id'] = data.index
        datetime_dim = data['time'].reset_index(drop=True)
        datetime_dim = np.array(datetime_dim)
        datetime_dim = pd.DataFrame(datetime_dim, columns=['earthquake_datetime'])
        datetime_dim['earthquake_hour'] = datetime_dim['earthquake_datetime'].dt.hour
        datetime_dim['earthquake_day'] = datetime_dim['earthquake_datetime'].dt.day
        datetime_dim['earthquake_month'] = datetime_dim['earthquake_datetime'].dt.month
        datetime_dim['earthquake_year'] = datetime_dim['earthquake_datetime'].dt.year
        datetime_dim['earthquake_weekday'] = datetime_dim['earthquake_datetime'].dt.weekday
        datetime_dim['datetime_id'] = datetime_dim.index


        # Location dim :
        location_dim = data['place'].reset_index(drop=True)
        location_dim = np.array(location_dim)
        location_dim = pd.DataFrame(location_dim, columns=['place'])
        location_dim['location_id'] = location_dim.index
        location_dim['Longitude'] = data['longitude']
        location_dim['Latitude'] = data['latitude']
        location_dim['location_source'] = data['locationSource']

        # Magnitude dim :
        magnitude_dim = data['mag'].reset_index(drop=True)
        magnitude_dim = data['mag'].reset_index(drop=True)
        magnitude_dim = np.array(magnitude_dim)
        magnitude_dim = pd.DataFrame(magnitude_dim, columns=['earthquake_mag'])
        magnitude_dim['magnitude_id'] = magnitude_dim.index
        magnitude_dim['magnitude_error'] = data['magError']
        magnitude_dim['magnitude_nst'] = data['magNst']


        #Fact table:
        fact_table = pd.DataFrame(columns=['earthquake_id'])
        fact_table['earthquake_id'] = data.index
        fact_table['datetime_id'] = datetime_dim['datetime_id']
        fact_table['location_id'] = location_dim['location_id']
        fact_table['magnitude_id'] = magnitude_dim['magnitude_id']
        fact_table['depth'] = data['depth']
        fact_table['nst'] = data['nst']
        fact_table['gap'] = data['gap']
        fact_table['dmin'] = data['dmin']
        fact_table['rms'] = data['rms']


        print(f"Fact table \n{fact_table}")
        print(f"Magnitude dim table \n {magnitude_dim}")
        print(f"Location dim table \n {location_dim}")
        print(f"Datetime dim table \n {datetime_dim}")


trnf = DataTransformation()
trnf.transform()

table_id = 'snappy-abode-386009.earthquakedataetl.fact_table'