def check_columns(df, max_item_to_show=10):
    print(f'col, dtype, #uniques, nan/total, head({max_item_to_show})')
    for i in df.columns:
        col = df[i]
        uniques = col.unique()
        cnt = len(col)
        nan_cnt = cnt - col.count()
        print(i, col.dtype, len(uniques), f'{nan_cnt}/{cnt}', uniques[:max_item_to_show], sep=', ')

def check_datapoints_dtype(df):
    print('col, dtypes')
    for i in df.columns:
        print(i, df[i].apply(type).unique(), sep=', ')
