import json
import pandas as pd

def check_all(df, max_value_to_show=10):
    dfs = [check_columns(df, max_value_to_show),
           check_datapoints_dtype(df).iloc[:, 1:]]
    return pd.concat(dfs, axis=1)


def check_columns(df, max_item_to_show=10):
    '''Column dtype are computed from non-NaN values to prevent int64 columns becomes float64.'''
    column = []
    dtyp = []
    uniq_cnt = []
    data_cnt = []
    nan_cnt=[]
    sample_value = []
    d = {'column': column, 'dtype': dtyp, 'uniq_cnt': uniq_cnt,
         'data_cnt': data_cnt, 'nan_cnt': nan_cnt,
         'sample_value': sample_value}

    for i in df.columns:
        col = df[i]
        uniques = col.unique()
        cnt = len(col)

        column.append(i)
        dtyp.append(col.dropna().dtype)
        uniq_cnt.append(len(uniques))
        nan_cnt.append(cnt - col.count())
        data_cnt.append(cnt)

        # Convert to string, otherwise jupyter notebook display without padding spaces
        #sample_value.append(str(uniques[:max_item_to_show].tolist()))
        sample_value.append(json.dumps(uniques[:max_item_to_show].tolist()))

    return pd.DataFrame(d, columns=['column', 'dtype', 'uniq_cnt', 'data_cnt', 'nan_cnt', 'sample_value'])


def check_datapoints_dtype(df):
    '''Only dtypes of non-NaN values to prevent int64 columns become float64.'''
    column = list(df.columns)
    dtypes = []
    dtype_cnt = []
    d = {'column': column, 'dtypes': dtypes, 'dtype_cnt': dtype_cnt}

    for i in column:
        dt = df[i].dropna().apply(lambda x: x.__class__.__name__).unique().tolist()
        dtypes.append(dt)
        dtype_cnt.append(len(dt))

    return pd.DataFrame(d, columns=['column', 'dtypes', 'dtype_cnt'])
