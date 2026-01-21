"""
Module for using GMGT datasets. Simply copy the `records` function in your code.
See README for further details
"""

# virtual anv with python3.11
# pip install --upgrade pip setuptools && pip install h5py tables pandas

from collections.abc import Iterator
import numpy as np
import pandas as pd
import h5py



def get_records(
    dataset_path, **filters
) -> Iterator[tuple[np.ndarray, np.ndarray, np.ndarray, float, tuple]]:
    """
    Yield datasets records in the form:

    (h1, h2, v, dt, metadata)

    where:
    - h1, h2 and v are numpy arrays denoting the time histories, in m/s^2. h1 and h2
      denote the two horizontal components and v the vertical. An empty array indicates
      that the component is not available. The two horizontal components do not have
      further information (e.g., orientation N/S is N/A).
    - dt is the float denoting the data sampling interval (in s)
    - metadata is a namedtuple and it's quite self-explanatory (you can access all
      metadata fields as normal attributes, e.g. `metadata.magnitude`. For a full list
      of fields, see:
      <https://github.com/rizac/gmgt-collect/blob/main/metadata_fields.yml>

    :param dataset_path: a string denoting the dataset path (absolute path to hdf file)
    :param filters: a keyword argument whose parameters are any metadata fields,
        optionally prefixed with 'min_', 'max_' and 'missing_' mapped to a matching
        values in order to filter specific metadata row and yield only the corresponding
        data. Values cannot be None / nan, NaT: to get those values, use the 'missing_'
        prefix:, e.g. type `missing_magnitude: False` to yield only records where the
        magnitude is provided (not N/A). Values can also be list/tuples, in this case
        records whose fields are equal to any value in the list/tuple will be yielded

        Examples:
            for h1, h2, v, dt, m in records(path, available_components=['HHV', 'HH']):
            for h1, h2, v, dt, m in records(path, min_magnitude=6):
            for h1, h2, v, dt, m in records(path, max_magnitude=6)
            for h1, h2, v, dt, m in records(path, magnitude=6)
            for h1, h2, v, dt, m in records(path, magnitude=[4, 5, 6])
    """
    chunk_size = 100000  # chunk for pandas read_hdf

    with pd.HDFStore(dataset_path, "r") as pd_f, h5py.File(dataset_path, "r") as h5_f:
        h5_root_group = h5_f["waveforms"]
        for chunk in pd_f.select("metadata", chunksize=chunk_size):  # noqa
            mask = pd.Series(True, index=chunk.index)
            for expr, value in filters.items():
                try:
                    if expr.startswith('min_'):
                        col = expr[4:]
                        # categorical column, need to work on categories:
                        if isinstance(chunk[col].dtype, pd.CategoricalDtype):
                            categs = chunk[col].cat.categories  # pandas Index
                            col_mask = chunk[col].isin(categs[categs >= value])
                        else:
                            col_mask = chunk[col] >= value
                    elif expr.startswith('max_'):
                        col = expr[4:]
                        if isinstance(chunk[col].dtype, pd.CategoricalDtype):
                            categs = chunk[col].cat.categories  # pandas Index
                            col_mask = chunk[col].isin(categs[categs <= value])
                        else:
                            col_mask = chunk[col] <= value
                    elif expr.startswith('missing_'):
                        col = expr[8:]
                        if value is True:
                            col_mask = chunk[col].isna()
                        elif value is False:
                            col_mask = chunk[col].notna()
                        else:
                            raise ValueError(f'True/False expected, found {value}')
                    else:
                        col = expr
                        if isinstance(value, (tuple, list, set)):
                            col_mask = chunk[col].isin(value)
                        else:
                            col_mask = chunk[col] == value
                    mask &= col_mask

                except (TypeError, ValueError, KeyError, AssertionError) as exc:
                    raise ValueError(f'Error in "{expr}": {exc}')

            for row in chunk[mask].itertuples(name='metadata', index=False):
                if row.event_id in h5_root_group:
                    event_waveforms = h5_root_group[row.event_id]
                    if row.station_id in event_waveforms:
                        wav = event_waveforms[row.station_id]
                        yield wav[0], wav[1], wav[2], wav.attrs['dt'], row
