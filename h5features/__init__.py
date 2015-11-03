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

"""This package defines a standard to read/write features from/to HDF5 files.

The h5features file format is briefly documented at
http://abxpy.readthedocs.org/en/latest/FilesFormat.html#features-file

.. note::

   **The functions are not concurrent nor thread-safe**
   because the HDF5 library is not concurrent and not always
   thread-safe. Moreover, they aren't even atomic for independent
   process (because there are several independent calls to the
   file system), so that thread-safety and atomicity of
   operations should be enforced externally when necessary.

"""

from .h5features import read
from .h5features import write
from .h5features import simple_write

from .writer import Writer
from .reader import Reader

from .features import Features
from .times import Times
from .items import Items
