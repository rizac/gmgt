"""
Module for using GMGT datasets. Simply copy the `records` function in your code.
See README for further details
"""

# virtual anv with python3.11
# pip install --upgrade pip setuptools && pip install h5py tables pandas

import numpy as np
import pandas as pd
import h5py
from typing import Iterator, NamedTuple


def get_records(
    hdf_path, **filters
) -> Iterator[tuple[np.ndarray, np.ndarray, np.ndarray, float, NamedTuple]]:
    """
    Yield waveform records matching the given filters.

    Each record is returned as:
        (h1, h2, v, dt, metadata)

    The first three elements are numpy arrays representing acceleration
    time histories in m/s**2. The arrays correspond to the two horizontal
    components and the vertical component, respectively. If a component is
    missing, an empty array is returned.

    `dt` is the sampling interval in seconds.

    `metadata` contains record metadata and can be accessed as attributes,
    for example: `metadata.magnitude`.

    Parameters
    ----------
    hdf_path : str
        Path to the HDF dataset containing waveforms and metadata.

    filters : dict
        Keyword filters applied to metadata fields. Filter keys may be
        optionally prefixed with:

        - `min_` or `max_` to specify numeric range constraints
        - `missing_` to filter records based on missing values

        Filter values may also be lists or tuples, in which case records
        matching any value in the collection will be returned.

        Notes:
        1. The `min_` and `max_` prefixes can be used only with numeric,
           boolean or datetime fields to avoid lexical comparison issues
           (e.g. "9" > "10"), except for `origin_time_resolution`. Example:
           `min_origin_time_resolution="s"` will get records with
           event time resolutions equal to or finer than seconds

        2. Values cannot be None or NaN. To filter missing values,
           use the `missing_` prefix. Example: `missing_magnitude=False`
           to get only records with magnitude defined

    Examples
    --------

    for h1, h2, v, dt, m in records(path, min_magnitude=6):
    for h1, h2, v, dt, m in records(path, max_magnitude=6):
    for h1, h2, v, dt, m in records(path, magnitude=6):
    for h1, h2, v, dt, m in records(path, magnitude=[4, 5, 6]):
    """
    with pd.HDFStore(hdf_path, "r") as pd_f, h5py.File(hdf_path, "r") as h5_f:
        h5_root_group = h5_f["waveforms"]
        meta_columns: set = None

        #  pandas functions proxies:
        is_datetime = pd.api.types.is_datetime64_dtype
        is_numeric = pd.api.types.is_numeric_dtype

        # iterate over metadata (adjust chunk size if needed):
        for chunk in pd_f.select("metadata", chunksize=100000):  # noqa
            mask = np.ones(len(chunk), dtype=bool)

            if meta_columns is None:
                # lazy create columns
                meta_columns = set(chunk.columns)

                # check (one-time op) on values (we don't need to know meta columns):
                invalid = [xpr for xpr, val in filters.items() if np.any(pd.isna(val))]
                if invalid:
                    raise ValueError(
                        f'Invalid None/NaN value provided for: {", ".join(invalid)}'
                    )

            for expr, value in filters.items():
                try:
                    col_mask = None

                    if expr in meta_columns:

                        if isinstance(value, (tuple, list, set)):
                            col_mask = chunk[expr].isin(value)
                        else:
                            col_mask = chunk[expr] == value

                    elif expr.startswith('missing_'):
                        col = expr[8:]

                        if col in meta_columns:

                            if value is True:
                                col_mask = chunk[col].isna()
                            elif value is False:
                                col_mask = chunk[col].notna()
                            else:
                                raise ValueError(f'True/False expected, found {value}')

                    elif expr.startswith('min_') or expr.startswith('max_'):
                        col = expr[4:]

                        if col in meta_columns:

                            if col == 'origin_time_resolution':
                                categories = ['Y', 'M', 'D', 'H', 'm', 's']
                                assert value in categories, f'invalid value: {value}'

                                if expr.startswith('min_'):
                                    values = categories[categories.index(value):]
                                else:
                                    values = categories[:categories.index(value)]

                                col_mask = chunk[col].isin(values)

                            elif isinstance(chunk[col].dtype, pd.CategoricalDtype):
                                # categorical column, need to work on categories:
                                categories = chunk[col].cat.categories  # pandas Index

                                if is_datetime(categories) or is_numeric(categories):

                                    if expr.startswith('min_'):
                                        values = categories[categories >= value]
                                    else:
                                        values = categories[categories <= value]
                                    col_mask = chunk[col].isin(values)

                            elif is_datetime(chunk[col]) or is_numeric(chunk[col]):

                                if expr.startswith('min_'):
                                    col_mask = chunk[col] >= value
                                else:
                                    col_mask = chunk[col] <= value

                            if col_mask is None:
                                raise ValueError(
                                    'invalid on non-numeric, non-datetime data field'
                                )

                    if col_mask is None:
                        raise ValueError(f'expected metadata field name or expression')

                    mask &= col_mask.to_numpy()

                except (TypeError, ValueError, KeyError, AssertionError) as exc:
                    raise ValueError(f'Error in "{expr}": {exc}')

            for row in chunk[mask].itertuples(name='metadata', index=False):
                waveform = h5_root_group[row.event_id][row.station_id]
                yield waveform[0], waveform[1], waveform[2], waveform.attrs['dt'], row
