# Copyright 2014-2015 Thomas Schatz, Mathieu Bernard, Roland Thiolliere
#
# This file is part of h5features.
#
# h5features is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# h5features is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with h5features.  If not, see <http://www.gnu.org/licenses/>.
"""Provides the read() and write() wrapper functions.

.. note::

   For compatibility with h5features 1.0, this legacy top-level API
   have been conserved in this module. Except for use in legacy code,
   it is **better not to use it**. Use instead the `h5features.write`
   and `h5features.read` modules.

"""

from .reader import Reader
from .writer import Writer
from .items import Items
from .times import Times
from .features import Features, SparseFeatures, parse_dformat

def read(filename, groupname, from_item=None, to_item=None,
         from_time=None, to_time=None, index=None):
    """Reads in a h5features file.

    :param str filename: Path to a hdf5 file potentially serving as a
        container for many small files

    :param str groupname: HDF5 group to read the data from.

    :param str from_item: Optional. Read the data starting from this
        item. (defaults to the first stored item)

    :param str to_item: Optional. Read the data until reaching the
        item. (defaults to from_item if it was specified and to the
        last stored item otherwise)

    :param float from_time: Optional. (defaults to the beginning time
        in from_item) the specified times are included in the output

    :param float to_time: Optional. (defaults to the ending time in
        to_item) the specified times are included in the output

    :param int index: Optional. For faster access. TODO Document and
        test this.

    :return: A tuple (times, features) such as:

        * time is a dictionary of 1D arrays values (keys are items).

        * features: A dictionary of 2D arrays values (keys are
          items) with the 'feature' dimension along the columns and the
          'time' dimension along the lines.

    .. note:: Note that all the files that are present on disk between
        file1 and file2 will be loaded and returned. It's the
        responsibility of the user to make sure that it will fit into
        RAM memory.

    """

    reader = Reader(filename, groupname)
    data = (reader.read(from_item, to_item, from_time, to_time)
            if index is None else reader.index_read(index))
    return (dict(zip(data['items'].data, data['times'].data)),
            dict(zip(data['items'].data, data['features'].data)))


def write(filename, groupname, items_data, times_data, features_data,
          dformat='dense', chunk_size=0.1, sparsity=0.1):
    """Write h5features data in a HDF5 file.

    This function is a wrapper to the Writer class. It has three purposes:

    * Check parameters for errors (see details below),
    * Create Items, Times and Features objects
    * Send them to the Writer.

    :param str filename: HDF5 file to be writted, potentially serving
        as a container for many small files. If the file does not
        exist, it is created. If the file is already a valid HDF5
        file, try to append the data in it.

    :param str groupname: Name of the group to write the data in, or
        to append the data to if the group already exists in the file.

    :param items_data: List of files from which the features where
        extracted.
    :type items_data: list of str

    :param times_data: Time value for the features array. Elements of
        a 1D array are considered as the center of the time window
        associated with the features. A 2D array must have 2 columns
        corresponding to the begin and end timestamps of the features
        time window.
    :type times_data: list of  1D or 2D numpy arrays

    :param features_data: Features should have
        time along the lines and features along the columns
        (accomodating row-major storage in hdf5 files).
    :type features_data: list of 2D numpy arrays

    :param str dformat: Optional. Which format to store the features
        into (sparse or dense). Default is dense.

    :param float chunk_size: Optional. In Mo, tuning parameter
        corresponding to the size of a chunk in the h5file. Ignored if
        the file already exists.

    :param float sparsity: Optional. Tuning parameter corresponding to
        the expected proportion of non-zeros elements on average in a
        single frame.

    :raise IOError: if the filename is not valid or parameters are inconsistent.

    :raise NotImplementedError: if features_format == 'sparse'

    """
    # Prepare the data, raise on error
    data = {}
    data['items'] = Items(items_data)
    data['times'] = Times(times_data)
    data['features'] = (SparseFeatures(features_data, sparsity)
                        if parse_dformat(dformat) == 'sparse'
                        else Features(features_data))

    # Write all that stuff in the HDF5 file's specified group
    Writer(filename, chunk_size).write(data, groupname, append=True)


def simple_write(filename, group, times, features, item='item'):
    """Simplified version of `write()` when there is only one item."""
    write(filename, group, [item], [times], [features])
