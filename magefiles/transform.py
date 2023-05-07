import pandas as pd
import numpy as np

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
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

    return {"datetime_dim":datetime_dim.to_dict(orient = "dict"),
    "magnitude_dim":magnitude_dim.to_dict(orient = "dict"),
    "location_dim":location_dim.to_dict(orient = "dict"),
    "fact_table":fact_table.to_dict(orient = "dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
