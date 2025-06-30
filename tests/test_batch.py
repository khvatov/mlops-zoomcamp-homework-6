import pytest
import pandas as pd
from batch import read_data, prepare_data

from datetime import datetime

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    print('test_prepare_data')
    data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    expected_data = [
        ('-1', '-1', dt(1, 1), dt(1, 10), 9.0),
        ('1', '1', dt(1, 2), dt(1, 10), 8.0)
    ]   
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    categorical = ['PULocationID', 'DOLocationID']


    expected_df = pd.DataFrame(expected_data, columns=columns + ['duration'])
    
    df_out = prepare_data(df, categorical)
    assert(len(df_out)==2)

    print("expected")
    print(expected_df.to_dict(orient='records') )

    print("actual")
    print(df_out.to_dict(orient='records') )

    #assert(expected_df.to_dict(orient='records') == df_out.to_dict(orient='records'))
    pd.testing.assert_frame_equal(expected_df, df_out, check_dtype=False)
    #anoter way to compare DataFrames
    assert(expected_df[expected_df.columns].values.tolist() == df_out[df_out.columns].values.tolist())
