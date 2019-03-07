import pandas as pd

def check_columns(df, max_item_to_show=10):
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
        dtyp.append(col.dtype)
        uniq_cnt.append(len(uniques))
        nan_cnt.append(cnt - col.count())
        data_cnt.append(cnt)
        sample_value.append(uniques[:max_item_to_show])

    return pd.DataFrame(d, columns=['column', 'dtype', 'uniq_cnt', 'data_cnt', 'nan_cnt', 'sample_value'])


def check_datapoints_dtype(df):
    print('col, dtypes')
    for i in df.columns:
        print(i, df[i].apply(type).unique(), sep=', ')
