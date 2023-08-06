# MIT License

# Copyright (c) 2023 MatrixEditor

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import overload
from io import IOBase

from fsapi.isu.product import FSCustomisation, FSVersion
from fsapi.isu.fsfs import FSFSTree

__all__ = [
    "ISUFileBuffer", "ISUInspector", "ISUCompressionField", "ISUHeader",
    "ISU_MAGIC_BYTES", "set_inspector", "ISUPartition", "get_instance"
]

ISU_MAGIC_BYTES = [0x76, 0x11, 0x00, 0x00]

class ISUFileBuffer:
    """File buffer storing all bytes of an ISU file.

    :raises TypeError: if the given resource is not a valid ISU file
    """

    @overload
    def __init__(self, res: str) -> None: ...
    @overload
    def __init__(self, res: bytes) -> None: ...

    def __init__(self, res: IOBase) -> None:
        self._file = None
        self._pos = 0
        if isinstance(res, str):
            with open(res, 'rb') as res_fp:
                self._file = res_fp.read()
        elif isinstance(res, (bytearray, bytes, list)):
            self._file = res
        elif isinstance(res, IOBase):
            self._file = res.read()
        else:
            raise TypeError(f'Unexpected resource type: {type(res)}')

        # accessable attributes
        self.version = None
        self.customisation = None

    def __getitem__(self, key):
        return self._file[key]

    def pull(self) -> int:
        """Pulls the next byte and moving the pointer forwards.

        :return: the byte at the current position
        :rtype: int
        """
        pos = self._pos
        self._pos += 1
        return self[pos]

    def get_buffer(self) -> bytes:
        """Returns the raw bytes

        :return: the raw buffer
        :rtype: bytes
        """
        return self._file

    @property
    def position(self) -> int:
        """Returns the current (absolute) position.

        :return: the absolute file position
        :rtype: int
        """
        return self._pos


class ISUCompressionField:
    """Definition of an ISU compression field.

    These fields usually store the compressed size value of a partition
    defined in the ISU header.
    """
    def __init__(self) -> None:
        self.name = None
        self.size = -1

    def __bytes__(self) -> bytes:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()


class ISUHeader:
    """Structure for the header of an ISU file.

    There is a specific file header for the update files which contains additional
    information about the firmware file. Note that all of the inspected binary files
    contain almost the same header structure.

    During analysis of different binary files, there was one that contained two
    additional fields in the ISU-Header. These fields are most likely there to define
    the major and minor version of the used file structure. Also, this custom header
    specifies a length of 0xA2 (162) bytes.

    Headers with additional specifications can be found in products with the Venice 2.5
    module and the ir-fsccp-scb interface specification.

    :param meos_version: may be used to indicate the MeOS MajorVersion and MeOS Minor
                         Version, defaults to 0
    :type meos_version: int, optional

    :param version: The FSVersion object storing version information, defaults to None
    :type version: FSVersion, optional

    :param customisation: A FSCustomisation object storing product information, defaults
                          to None
    :type customisation: FSCustomisation, optional

    :param size: the header's size, defaults to -1
    :type size: int, optional
    """
    def __init__(self, meos_version: int = 0, version: FSVersion = None,
                customisation: FSCustomisation = None, size: int = -1) -> None:
        self.meos_version = meos_version
        self.version = version
        self.customisation = customisation
        self.size = size

    def __repr__(self) -> str:
        return f'<ISUHeader size={self.size}>'


class ISUPartition:
    """Partition entry structur of ISU files.

    Note, that partition entries start immediately after the header of an ISU file. This
    data always have a size of 16 bytes and maybe indicate what partitions this file
    contains.
    """
    ENTRY_END = 1
    ENTRY_PT = 0

    PT_10_CRC = (0x06, 0x02, 0x1F, 0x2B)
    PT_20_CRC = (0x0A, 0x02, 0x7E, 0xDB)

    def __init__(self, number: int = -1, entry_type: int = 0) -> None:
        self._number = number
        self._type = entry_type

    @property
    def partition(self) -> int:
        """Returns the partition number for this object,

        :return: the partition number
        :rtype: int
        """
        return self._number
    
    @property
    def entry_type(self) -> int:
        return self._type

    @partition.setter
    def partition(self, value: int):
        self._number = value

    def get_crc(self) -> tuple:
        """Returns the check-returncode tuple

        :return: a tuple storing bytes to chang against
        :rtype: tuple
        """
        if self.partition == 1:
            return ISUPartition.PT_10_CRC
        if self.partition == 2:
            return ISUPartition.PT_20_CRC
        return tuple()

    def is_web_partition(self) -> bool:
        """Returns whether this partition is a web-partition.

        :return: True if the ISUFile might contain a web-partition
        :rtype: bool
        """
        return self.partition == 2

    def __repr__(self) -> str:
        return f'<Partition {self.partition}: web={self.is_web_partition()}>'


class ISUInspector:
    """Abstract Base Adapter for all ISU file inspectors.

    Instances of the ISUInspector should be able to:
        - read and extract ISUHeader objects from a given buffer,
        - read and extract ISUPartition objects,
        - and optionally read and extract a stored directory archive

    This class is designed to have optional arguments that can be passed
    to the sub implementation by adding positionals at the end of each
    method call.
    """

    def get_fs_tree(self, buffer: ISUFileBuffer, offset: int = 0, **kwgs) -> FSFSTree:
        """Tries to parse the directory archive stored in the provided ISU file.

        :param buffer: the file buffer
        :type buffer: ISUFileBuffer
        :param offset: the starting offset, defaults to 0
        :type offset: int, optional
        :return: the parsed file system tree
        :rtype: FSFSTree
        """
        pass

    def get_header(self, buffer: ISUFileBuffer, offset: int = 0, **kwgs) -> ISUHeader:
        """Returns the parsed ISUHeader.

        :param buffer: the file buffer
        :type buffer: ISUFileBuffer
        :param offset: the starting offset, defaults to 0
        :type offset: int, optional
        :return: header information parsed into an ISUHeader object
        :rtype: ISUHeader
        """
        pass

    def get_compression_fields(self, buffer: ISUFileBuffer, offset: int = 0, **kwgs) -> list:
        """Returns the compression fields found in the given file buffer.

        :param buffer: the file buffer
        :type buffer: ISUFileBuffer
        :param offset: the starting offset, defaults to 0
        :type offset: int, optional
        :return: a list of compression fields
        :rtype: list
        """
        return []

    def get_partitions(self, buffer: ISUFileBuffer, **kwgs) -> list:
        """Tries to resolve all defined partitions in the given ISU file.

        :param buffer: the file buffer
        :type buffer: ISUFileBuffer
        :return: a list of resolved partitions
        :rtype: list
        """
        return []


INSPECTOR_TABLE = {}
"""Small dict to store all registered inspector types"""

def set_inspector(name: str):
    """Registers a new ISUInspector class

    :param name: the mapping name
    :type name: str
    """
    def add_inspector(insp):
        if name not in INSPECTOR_TABLE:
            INSPECTOR_TABLE[name] = insp
        return insp
    return add_inspector


def get_instance(name: str) -> ISUInspector:
    """Resolves the given name and returns the corresponding ISUInspector.

    :param name: the mapped inspector name, type name or file name
    :type name: str
    :raises ValueError: if the name is null
    :raises NameError: if no registered ISUInspector could be found
    :return: an instance of the right ISUInspector class
    :rtype: ISUInspector
    """
    if not name or len(INSPECTOR_TABLE) == 0:
        raise ValueError('Name is null or no inspector defined')

    if name in INSPECTOR_TABLE:
        itype = INSPECTOR_TABLE[name]
        return itype()

    for _, itype in INSPECTOR_TABLE.items():
        if itype.__name__ == name:
            return itype()

    values = name.lower().split('-')
    # NOTE: The inspector can be retrieved by replacing the '-' with a '/'
    # for the first three elements (if 'FS' is present in the third one)
    path = None
    if 'fs' in values[2]:
        path = '/'.join(values[:3])
    else:
        path = values[0]
        pos = 1
        next_path = []
        # NOTE: some inspectors contain sub-type definitions, which are added
        # with a '.' in the descriptor string: e.g. 'ir/mmi.16m/fs2026'
        while 'fs' not in values[pos]:
            next_path.append(values[pos])
            pos += 1
            if len(values) <= pos:
                raise ValueError('Invalid inspector name')

        next_path = '.'.join(next_path)
        path = f"{path}/{next_path}/{values[pos]}"

    if path not in INSPECTOR_TABLE:
        raise NameError(f'Could not resolve inspector: "{path}"')

    itype = INSPECTOR_TABLE[path]
    return itype()
