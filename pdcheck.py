"""See Jupyter notebooks on how to use these module to assess data quality of .csv data.

Note that python-3.6+ permits '_' as floating point separator, thus this module will treat '_'-separated float string
as valid floating points.
"""

import json
import pandas as pd
import re

ALPHANUMERIC_REGEXP = re.compile(r'[0-9a-zA-Z]')


def check_all(df, max_value_to_show=10):
    """Perform check_columns() and check_datapoints_dtype()."""
    dfs = [check_columns(df, max_value_to_show),
           check_datapoints_dtype(df).iloc[:, 1:]]
    return pd.concat(dfs, axis=1)


def check_possible_dtype(df, skip_fn=None, print_str=False):
    """Guess dtypes for each column in a dataframe, where dataframe must contains only string values otherwise exception occurs.

    :param df: a DataFrame whose all values must be strings.
    """
    column = []
    int_cnt = []
    dec_cnt = []
    str_cnt = []
    d = {'column': column, 'int_cnt': int_cnt, 'dec_cnt': dec_cnt, 'str_cnt': str_cnt}

    for i in df.columns:
        ser = df[i].drop_duplicates()
        column.append(i)
        int_cnt.append(ser.apply(lambda x: is_int_str(x, skip_fn)).sum())
        dec_cnt.append(ser.apply(lambda x: is_dec_str(x, skip_fn)).sum())
        str_cnt.append(ser.apply(lambda x: is_not_number_str(x, skip_fn, print_str)).sum())

    dtype_options_df = pd.DataFrame(d, columns=['column', 'int_cnt', 'dec_cnt', 'str_cnt'])

    # Best-effort guess on dtype
    guessed_dtype = dtype_options_df.apply(guess_dtype, axis=1).rename('guessed_type')

    return pd.concat([dtype_options_df, guessed_dtype], axis=1)


def extract_str_values(df, skip_fn=None) -> pd.DataFrame:
    """

    :rtype:
    """
    column = []
    str_values = []
    d = {'column': column, 'str_values': str_values}

    for i in df.columns:
        ser = df[i].drop_duplicates()
        column.append(i)
        str_filter = ser.apply(lambda x: is_not_number_str(x, skip_fn))
        str_ser = ser[str_filter]
        str_values.append(json.dumps(str_ser.tolist(), ensure_ascii=False))

    return pd.DataFrame(d, columns=['column', 'str_values'])


def check_columns(df, max_item_to_show=10):
    """Column dtype are computed from non-NaN values to prevent int64 columns becomes float64."""
    column = []
    dtyp = []
    uniq_cnt = []
    data_cnt = []
    nan_cnt = []
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
        # sample_value.append(str(uniques[:max_item_to_show].tolist()))
        sample_value.append(json.dumps(uniques[:max_item_to_show].tolist()))

    return pd.DataFrame(d, columns=['column', 'dtype', 'uniq_cnt', 'data_cnt', 'nan_cnt', 'sample_value'])


def check_datapoints_dtype(df):
    """Only dtypes of non-NaN values to prevent int64 columns become float64."""
    column = list(df.columns)
    dtypes = []
    dtype_cnt = []
    d = {'column': column, 'dtypes': dtypes, 'dtype_cnt': dtype_cnt}

    for i in column:
        dt = df[i].dropna().apply(lambda x: x.__class__.__name__).unique().tolist()
        dtypes.append(dt)
        dtype_cnt.append(len(dt))

    return pd.DataFrame(d, columns=['column', 'dtypes', 'dtype_cnt'])


def guess_dtype(x):
    if x['str_cnt'] > 0:
        return 'str'
    if x['dec_cnt'] != x['int_cnt']:
        return 'float'
    if x['int_cnt'] == 0 and x['dec_cnt'] == 0:
        return 'str'
    return 'int'


def is_suspicious_str(s) -> bool:
    """Check whether string `s` looks suspicious (e.g., '' or a non-alphanumeric value)."""
    try:
        _ = s.encode('ascii')
        return True if s == '' else not ALPHANUMERIC_REGEXP.search(s)
    except UnicodeEncodeError:
        # Treat string with non-CJK_space characters as "not suspicious".
        # NOTE:
        # - \u3000 is CJK whitespace
        # - There're other unicode whitespaces listed here: https://stackoverflow.com/a/37903645
        return b'\\u3000' in s.encode('unicode_escape')
    except:
        print(s)
        raise


def is_int_str(x: str, skip_fn=None):
    if skip_fn is not None and skip_fn(x):
        return False
    return x.isnumeric()


def is_dec_str(x: str, skip_fn=None):
    if skip_fn is not None and skip_fn(x):
        return False
    try:
        float(x)
    except:
        return False
    else:
        return True


def is_not_number_str(x: str, skip_fn=None, print_str=False):
    if skip_fn is not None and skip_fn(x):
        return False
    try:
        float(x)
    except:
        if print_str:
            print(x)
        return True
    else:
        return False
