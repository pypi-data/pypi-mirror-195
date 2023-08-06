# This program is public domain
# Author: Paul Kienzle
# with R De Renzi's very unprofessional muon hack

"""
Wrapper for the NeXus shared library.

Use this interface when converting code from other languages which
do not support the natural view of the hierarchy.

Muon hack
=========
Indicated by comment # RDR
Problems: incompatibility of bytes and str in python3
Now the filename is a string, 
the inner keywords (name, nxclass, etc) are still bytes 
but string comparison is (mostly) fixed
What does work
import munxs as nxs
path = 'EMU00020882.nxs' # EMU 96 detector data file
run = nxs(path,'r')
run.opengrouppath(b'/run') # is like cd in nxbrowse, notice that keywordss must be bytes!!
out = run.getentries() # is like ls in nxbrowse
run.opengrouppath(b'/run/histogram_data_1')
y = run(b'counts') # reads 96 x 2000 integers into a numpyt array
# run.readfile() doesn't work because it hits on Could not open b'UNKNOWN':b'UNKNOWN' in /home/roberto.derenzi/Downloads/mantid/muon_cupper/EMU00020882.nxs(b'/c:\\data\\EMU00020882.nxs/fakeDim0')

Library Location
================

:py:mod:`nxs.napi` needs to know the location of the `libNeXus` C-library in
order to load it via :py:mod:`ctypes`.  It looks in the following places in
order:


+-------------------------------------+-----------------+
| Environment                         | Platforms       |
+=====================================+=================+
| ``os.environ['NEXUSLIB']``          | All             |
+-------------------------------------+-----------------+
| directory containing nxs.py         | All             |
+-------------------------------------+-----------------+
| ``os.environ['NEXUSDIR']\\bin``      | Windows         |
+-------------------------------------+-----------------+
| ``os.environ['LD_LIBRARY_PATH']``   | Unix            |
+-------------------------------------+-----------------+
| ``os.environ['DYLD_LIBRARY_PATH']`` | Darwin          |
+-------------------------------------+-----------------+
| ``LIBDIR``                          | Unix and Darwin |
+-------------------------------------+-----------------+


* On Windows it looks for one of ``libNeXus.dll`` or ``libNeXus-0.dll``.
* On OS X it looks for ``libNeXus.0.dylib``
* On Unix it looks for ``libNeXus.so.1``
* ``NEXUSDIR`` defaults to ``C:\\Program Files\\NeXus Data Format``.
* ``LIBDIR`` defaults to ``/usr/local/lib``, but is replaced by the value of
  ``--libdir`` during configure.

The import will raise an :py:exc:`OSError` exception if the library wasn't
found or couldn't be loaded.  Note that on Windows in particular this may be
because the supporting HDF5 dlls were not available in the usual places.

If you are extracting the nexus library from a bundle at runtime, set
`os.environ['NEXUSLIB']` to the path where it is extracted before the
first import of nxs.

Example
=======
.. code-block:: python

  import nxs
  file = nxs.open('filename.nxs','rw')
  file.opengroup('entry1')
  file.opendata('definition')
  print file.getdata()
  file.close()


See @see nxstest.py for a more complete example.

Interface
=========

When converting code to python from other languages you do not necessarily want
to redo the file handling code.  The nxs provides an interface which more
closely follows the NeXus application programming interface (NAPI_).

This wrapper differs from NAPI in several respects:

* Data values are loaded/stored directly from numpy arrays.
* Return codes are turned into exceptions.
* The file handle is stored in a file object
* Constants are handled somewhat differently (see below)
* Type checking on data/parameter storage
* Adds iterators file.entries() and file.attrs()
* Adds link() function to return the name of the linked to group, if any
* NXmalloc/NXfree are not needed.

File open modes can be constants or strings:

+--------------------------+--------------------------+
| Flag                     | Character representation |
+==========================+==========================+
| `nxs.napi.ACC_READ`      | 'r'                      |
+--------------------------+--------------------------+
| `nxs.napi.ACC_RDWR`      | 'rw'                     |
+--------------------------+--------------------------+
| `nxs.napi.ACC_CREATE`    | 'w'                      |
+--------------------------+--------------------------+
| `nxs.napi.ACC_CREATE4`   | 'w4'                     |
+--------------------------+--------------------------+
| `nxs.napi.ACC_CREATE5`   | 'w5'                     |
+--------------------------+--------------------------+
| `nxs.napi.ACC_CREATEXML` | 'wx'                     |
+--------------------------+--------------------------+


Dimension constants:
   
+---------------+---------------------------------------+
| Constant      | Description                           |
+===============+=======================================+
| nxs.UNLIMITED | for the extensible data dimension     |
+---------------+---------------------------------------+
| nxs.MAXRANK   | for the number of possible dimensions |
+---------------+---------------------------------------+

Data types are strings corresponding to the numpy data types:

+---------------+-----------------------------+
| Type string   | Description                 |
+===============+=============================+
| ``'float32'`` | 32Bit floating point number |
+---------------+-----------------------------+
| ``'float64'`` | 64Bit floating point number |
+---------------+-----------------------------+
| ``'int8'``    | 8Bit singed integer         |
+---------------+-----------------------------+
| ``'int16'``   | 16Bit signed integer        |
+---------------+-----------------------------+
| ``'int32'``   | 32Bit signed integer        |
+---------------+-----------------------------+
| ``'int64'``   | 64Bit signed integer        |
+---------------+-----------------------------+
| ``'uint8'``   | 8Bit unsigned integer       |
+---------------+-----------------------------+
| ``'uint16'``  | 16Bit unsigned integer      |
+---------------+-----------------------------+
| ``'uint32'``  | 32Bit unsigned integer      |
+---------------+-----------------------------+
| ``'uint64'``  | 64Bit unsigned integer      |
+---------------+-----------------------------+
| ``'char'``    | used for string data        |
+---------------+-----------------------------+


To retrieve the type of a :py:mod:`numpy` array  one can use its
:py:attr:`dtype` attribute.

Dimensions are lists of integers or numpy arrays.  You can use the
numpy A.shape attribute for the dimensions of array A.

Compression codes are::

 'none' 'lzw' 'rle' 'huffman'

  As of this writing NeXus only supports 'none' and 'lzw'.

Miscellaneous constants:
    
+----------------+--------------------------------------------------------------+
| Constant       | Description                                                  |
+================+==============================================================+
| :py:const:`nxs | names must be shorter than this                              |
| .napi.MAXNAMEL |                                                              |
| EN`            |                                                              |
+----------------+--------------------------------------------------------------+
| nxs.napi.MAXPA | total path length must be shorter than this                  |
| THLEN          |                                                              |
+----------------+--------------------------------------------------------------+
| nxs.napi.H4SKI | class names that may appear in HDF4 files but can be ignored |
| P              |                                                              |
+----------------+--------------------------------------------------------------+

Caveats
=======

@todo NOSTRIP constant is probably not handled properly,
@todo Embedded nulls in strings is not supported

@warning  We have a memory leak.  Calling open/close costs about 90k a pair.
This is an eigenbug:
 - if I test ctypes on a simple library it does not leak
 - if I use the leak_test1 code in the nexus distribution it doesn't leak
 - if I remove the open/close call in the wrapper it doesn't leak.

"""

from __future__ import print_function

## @example nxstest.py
#  Test program for NeXus python interface

__all__ = ['UNLIMITED', 'MAXRANK', 'MAXNAMELEN','MAXPATHLEN','H4SKIP',
           'NeXus','NeXusError','open']

import sys, os, numpy, ctypes
import six

# Defined ctypes
from ctypes import c_void_p, c_int, c_int64, c_long, c_char, c_char_p
from ctypes import byref as _ref
c_void_pp = ctypes.POINTER(c_void_p)
c_int_p = ctypes.POINTER(c_int)
c_int64_p = ctypes.POINTER(c_int64)
class _NXlink(ctypes.Structure):
    _fields_ = [("iTag", c_long),
                ("iRef", c_long),
                ("targetPath", c_char*1024),
                ("linktype", c_int)]
    _pack_ = False
c_NXlink_p = ctypes.POINTER(_NXlink)


# Open modes:
ACC_READ,ACC_RDWR,ACC_CREATE=1,2,3
ACC_CREATE4,ACC_CREATE5,ACC_CREATEXML=4,5,6
_nxopen_mode=dict(r=1,rw=2,w=3,w4=4,w5=5,wx=6)
NOSTRIP=128

# Status codes
OK,ERROR,EOD=1,0,-1

# Other constants
UNLIMITED=-1
MAXRANK=32
MAXNAMELEN=64
MAXPATHLEN=1024 # inferred from code

# bogus groups; these groups are ignored in HDFView from NCSA.
H4SKIP = ['CDF0.0','_HDF_CHK_TBL_','Attr0.0',
          'RIG0.0','RI0.0', 'RIATTR0.0N','RIATTR0.0C']

# HDF data types from numpy types
_nxtype_code=dict(
    char=4,
    float32=5,float64=6,
    int8=20,uint8=21,
    int16=22,uint16=23,
    int32=24,uint32=25,
    int64=26,uint64=27,
    )
# Python types from HDF data types
# Other than 'char' for the string type, the python types correspond to
# the numpy data types, and can be used directly to create numpy arrays.
# Note: put this in a lambda to hide v,k from the local namespace
_pytype_code=(lambda : dict([(v,k) for (k,v) in six.iteritems(_nxtype_code)]))()

# Compression to use when creating data blocks
_compression_code=dict(
    none=100,
    lzw=200,
    rle=300,
    huffman=400)

def _is_string_like(obj):
    """
    Return True if object acts like a string.
    """
    # From matplotlib cbook.py John D. Hunter
    # Python 2.2 style licence.  See license.py in matplotlib for details.
    if hasattr(obj, 'shape'): return False
    try: obj + ''
    except (TypeError, ValueError): return False
    return True

def _is_list_like(obj):
    """
    Return True if object acts like a list
    """
    try: obj + []
    except TypeError: return False
    return True

def _libnexus():
    """
    Load the NeXus library.
    """
    # this will get changed as part of the install process
    # it should correspond to --libdir specified to ./configure
    # NEXUSLIB takes precedence
    if 'NEXUSLIB' in os.environ:
        file = os.environ['NEXUSLIB']
        if not os.path.isfile(file):
            raise OSError("File %s from environment variable NEXUSLIB does "
                          "exist" % file)
        files = [file]
    else:
        files = []

    # Default names and locations to look for the library are system dependent
    filedir = os.path.dirname(__file__)
    if sys.platform in ('win32','cygwin'):
        # NEXUSDIR is set by the Windows installer for NeXus
        if 'NEXUSDIR' in os.environ:
            winnxdir = os.environ['NEXUSDIR']
        else:
            winnxdir =  'C:/Program Files/NeXus Data Format'

        files += [filedir+"/libNeXus-0.dll",
                  winnxdir + '/bin/libNeXus-0.dll',
                  filedir+"/libNeXus.dll"]
    else:
        if sys.platform in ('darwin'):
            lib = 'libNeXus.0.dylib'
            ldenv = 'DYLD_LIBRARY_PATH'
        else:
            lib = 'libNeXus.so.1'
            ldenv = 'LD_LIBRARY_PATH'
        # Search the load library path as well as the standard locations
        ldpath = [p for p in os.environ.get(ldenv,'').split(':') if p != '']
        stdpath = [ '/usr/local/lib', '/usr/local/lib64',
                    '/usr/lib', '/usr/lib64']
        files += [os.path.join(p,lib) for p in [filedir]+ldpath+stdpath]

    # Given a list of files, try loading the first one that is available.
    for file in files:
        if not os.path.isfile(file): continue
        try:
            return ctypes.cdll[file]
        except:
            raise OSError("NeXus library %s could not be loaded: %s" %
                          (file,sys.exc_info()))
    raise OSError("Set NEXUSLIB or move NeXus to one of: %s" %
                  ", ".join(files))

def _init():
    lib = _libnexus()
    lib.NXMDisableErrorReporting()
    return lib

# Define the interface to the dll
nxlib = _init()


def open(filename, mode='r'):
    """
    Returns a NeXus file object.
    """
    return NeXus(filename, mode)

class NeXusError(Exception):
    """NeXus Error"""
    pass

class NeXus(object):

    # ==== File ====
    nxlib.nxiopen_.restype = c_int
    nxlib.nxiopen_.argtypes = [c_char_p, c_int, c_void_pp]
    def __init__(self, filename, mode='r'):
        """
        Open the NeXus file returning a handle.

        mode can be one of the following:
            nxs.ACC_READ      'r'     open a file read-only
            nxs.ACC_RDWR      'rw'    open a file read/write
            nxs.ACC_CREATE    'w'     open a file write
            nxs.ACC_CREATE4   'w4'    open a Nexus file with HDF4
            nxs.ACC_CREATE5   'w5'    open a Nexus file with HDF5
            nxs.ACC_CREATEXML 'wx'    open a Nexus file with XML

        Raises ValueError if the open mode is invalid.

        Raises NeXusError if the file could not be opened, with the
        filename as part of the error message.

        Corresponds to NXopen(filename,mode,&handle)
        """
        self.isopen = False

        # Convert open mode from string to integer and check it is valid
        if mode in _nxopen_mode: mode = _nxopen_mode[mode]
        if mode not in _nxopen_mode.values():
            raise ValueError("Invalid open mode %s" % str(mode))

        self.filename, self.mode = filename, mode
        self.handle = c_void_p(None)
        self._path = []
        self._indata = False
        status = nxlib.nxiopen_(filename.encode('utf-8'),mode,_ref(self.handle)) # RDR
        if status == ERROR:
            if mode in [ACC_READ, ACC_RDWR]:
                op = 'open'
            else:
                op = 'create'
            raise NeXusError("Could not %s %s" % (op,filename))
        self.isopen = True

    def _getpath(self):
        mypath = [level[0] for level in self._path]
        return b'/'+b'/'.join(mypath) # RDR
    path = property(_getpath,doc="Unix-style path to node")

    def _getlongpath(self):
        mypath = [b':'.join(level) for level in self._path]  # RDR
        return b'/' + b'/'.join(mypath)  # RDR
    longpath = property(_getlongpath, doc="Unix-style path including " \
                        + "nxclass to the node")

    def __del__(self):
        """
        Be sure to close the file before deleting the last reference.
        """
        if self.isopen: self.close()


    def __str__(self):
        """
        Return a string representation of the NeXus file handle.
        """
        return "NeXus('%s')"%self.filename


    def open(self):
        """
        Opens the NeXus file handle if it is not already open.

        Raises NeXusError if the file could not be opened.

        Corresponds to NXopen(filename,mode,&handle)
        """
        if self.isopen: return
        if self.mode==ACC_READ:
            mode = ACC_READ
        else:
            mode = ACC_RDWR
        status = nxlib.nxiopen_(self.filename,mode,_ref(self.handle))
        if status == ERROR:
            raise NeXusError("Could not open %s" % (self.filename))
        self._path = []
        self._indata = False

    nxlib.nxiclose_.restype = c_int
    nxlib.nxiclose_.argtypes = [c_void_pp]
    def close(self):
        """
        Close the NeXus file associated with handle.

        Raises NeXusError if file could not be closed.

        Corresponds to NXclose(&handle)
        """
        if self.isopen:
            self.isopen = False
            status = nxlib.nxiclose_(_ref(self.handle))
            if status == ERROR:
                raise NeXusError("Could not close NeXus file %s" %
                                 (self.filename))
        self._path = []
        self._indata = False

    nxlib.nxiflush_.restype = c_int
    nxlib.nxiflush_.argtypes = [c_void_pp]
    def flush(self):
        """
        Flush all data to the NeXus file.

        Raises NeXusError if this fails.

        Corresponds to NXflush(&handle)
        """
        status = nxlib.nxiflush_(_ref(self.handle))
        if status == ERROR:
            raise NeXusError("Could not flush NeXus file %s" % (self.filename))

    nxlib.nxisetnumberformat_.restype = c_int
    nxlib.nxisetnumberformat_.argtypes = [c_void_p, c_int, c_char_p]
    def setnumberformat(self,type,format):
        """
        Set the output format for the numbers of the given type (only
        applies to XML).

        Raises ValueError if the number format is incorrect.

        Corresponds to NXsetnumberformat(&handle,type,format)
        """
        type = _nxtype_code[type]
        status = nxlib.nxisetnumberformat_(self.handle,type,format)
        if status == ERROR:
            raise ValueError("Could not set %s to %s in %s" %
                             (type, format, self.filename))

    # ==== Group ====
    nxlib.nximakegroup_.restype = c_int
    nxlib.nximakegroup_.argtypes = [c_void_p, c_char_p, c_char_p]
    def makegroup(self, name, nxclass):
        """
        Create the group nxclass:name.

        Raises NeXusError if the group could not be created.

        Corresponds to NXmakegroup(handle, name, nxclass)
        """
        # print("makegroup", self._loc(), name, nxclass)
        status = nxlib.nximakegroup_(self.handle, name, nxclass)
        if status == ERROR:
            raise NeXusError("Could not create %s:%s in %s" %
                             (nxclass, name, self._loc()))

    nxlib.nxiopenpath_.restype = c_int
    nxlib.nxiopenpath_.argtypes = [c_void_p, c_char_p]
    def openpath(self, path):
        """
        Open a particular group '/path/to/group'.  Paths can be
        absolute or relative to the currently open group.  If openpath
        fails, then currently open path may not be different from the
        starting path. For better performation the types can be
        specified as well using '/path:type1/to:type2/group:type3'
        which will prevent searching the file for the types associated
        with the supplied names.

        Raises ValueError.

        Corresponds to NXopenpath(handle, path)
        """
        self._openpath(path, opendata=True)

    def _openpath(self, path, opendata=True):
        """helper function: open relative path and maybe data"""
        # Determine target node as sequence of group names
        # print('_openpath: path = {}'.format(path))
        if path == b'/' or path == '/': # RDR
            target = []
        else:
            try:
                dot, dotdot, col = b'.', b'..', b':' # RDR
                if path.decode('utf-8').endswith("/"): # RDR
                    path = path[:-1]
                if path.decode('utf-8').startswith('/'): # RDR
                    target = path[1:].split(b'/')  # RDR
                else:
                    target = self._path + path.split(b'/')  # RDR
            except: # RDR
                dot, dotdot, col = '.', '..', ':' # RDR
                if path.endswith("/"): 
                    path = path[:-1]
                if path.startswith('/'): 
                    target = path[1:].split('/')  
                else:
                    target = self._path + path.split('/') 

        # Remove relative path indicators from target
        L = []
        for t in target:
            if t == dot: # RDR
                # Skip current node
                pass
            elif t == dotdot: # RDR
                if L == []:
                    raise ValueError("too many '..' in path")
                L.pop()
            else:
                L.append(t)
        target = L

        # split out nxclass from each level if available
        L = []
        for t in target:
            try:
                item = t.split(col) # RDR
                if len(item) == 1:
                    L.append((item[0], None))
                else:
                    L.append(tuple(item))
            except AttributeError:
                L.append(t)
        target = L

        # print("current path", self._path)
        # print("%s" % path, target)

        # Find which groups need to be closed and opened
        up = []
        down = []
        for (i, (name, nxclass)) in enumerate(target):
            if i == len(self._path):
                # print("target longer than current")
                up = []
                down = target[i:]
                break
            elif self._path[i] != name:
                # print("target and current differ at", name)
                up = self._path[i:]
                down = target[i:]
                break
        else:
            # print("target shorter than current")
            up = self._path[len(target):]
            down = []

        # add more information to the down path
        for i in range(len(down)): # RDR was xrange (not defined in python 3)
            try:
                (name, nxclass) = down[i]
            except ValueError:
                down[i] = (down[i], None)
        # print("close,open", up, down)

        # Close groups on the way up
        if self._indata and up != []:
            self.closedata()
            up.pop()
        for target in up:
            self.closegroup()

        # Open groups on the way down
        for target in down:
            (name, nxclass) = target
            if nxclass is None:
                nxclass = self.__getnxclass(name)
            if nxclass != b'SDS':
                self.opengroup(name, nxclass)
            elif opendata:
                self.opendata(name)
            else:
                raise ValueError("node %s not in %s" % (name, self.path))

    nxlib.nxiopengrouppath_.restype = c_int
    nxlib.nxiopengrouppath_.argtypes = [c_void_p, c_char_p]
    def opengrouppath(self, path):
        """
        Open a particular group '/path/to/group', or the dataset containing
        the group if the path refers to a dataset.  Paths can be relative to
        the currently open group.

        Raises ValueError.

        Corresponds to NXopengrouppath(handle, path)
        """
        self._openpath(path,opendata=False)

    nxlib.nxiopengroup_.restype = c_int
    nxlib.nxiopengroup_.argtypes = [c_void_p, c_char_p, c_char_p]
    def opengroup(self, name, nxclass=None):
        """
        Open the group nxclass:name. If the nxclass is not specified
        this will search for it.

        Raises NeXusError if the group could not be opened.

        Corresponds to NXopengroup(handle, name, nxclass)
        """
        # print("opengroup", self._loc(), name, nxclass)
        if nxclass is None:
            nxclass = self.__getnxclass(name)
        status = nxlib.nxiopengroup_(self.handle, name, nxclass)
        if status == ERROR:
            raise ValueError("Could not open %s:%s in %s" %
                             (nxclass, name, self._loc()))
        self._path.append((name,nxclass))

    nxlib.nxiclosegroup_.restype = c_int
    nxlib.nxiclosegroup_.argtypes = [c_void_p]
    def closegroup(self):
        """
        Close the currently open group.

        Raises NeXusError if the group could not be closed.

        Corresponds to NXclosegroup(handle)
        """
        # print("closegroup")
        if self._indata:
            raise NeXusError("Close data before group at %s" % (self._loc()))
        status = nxlib.nxiclosegroup_(self.handle)
        if status == ERROR:
            raise NeXusError("Could not close group at %s" % (self._loc()))
        self._path.pop()

    nxlib.nxigetgroupinfo_.restype = c_int
    nxlib.nxigetgroupinfo_.argtypes = [c_void_p, c_int_p, c_char_p, c_char_p]
    def getgroupinfo(self):
        """
        Query the currently open group returning the tuple
        numentries, name, nxclass.

        Raises ValueError if the group could not be opened.

        Corresponds to NXgetgroupinfo(handle)

        Note: corrects error in HDF5 where getgroupinfo returns the entire
        path rather than the group name.  Use the path attribute to get
        a sensible value of path.
        """
        # Space for the returned strings
        path = ctypes.create_string_buffer(MAXPATHLEN)
        nxclass = ctypes.create_string_buffer(MAXNAMELEN)
        n = c_int(0)
        status = nxlib.nxigetgroupinfo_(self.handle,_ref(n),path,nxclass)
        try: # RDR
            pathvalue = path.value.decode('utf-8') # RDR
        except: # RDR
            pathvalue = path.value
        print('path = {}, path.value = {}'.format(path,path.value)) # RDR
        if status == ERROR:
            raise ValueError("Could not get group info: %s" % (self._loc()))
        # print("getgroupinfo", self._loc(), nxclass.value, name.value, n.value)
        name = pathvalue.split('/')[-1]  # Protect against HDF5 returning path
        return n.value,name,nxclass.value

    nxlib.nxiinitgroupdir_.restype = c_int
    nxlib.nxiinitgroupdir_.argtypes = [c_void_p]
    def initgroupdir(self):
        """
        Reset getnextentry to return the first entry in the group.

        Raises NeXusError if this fails.

        Corresponds to NXinitgroupdir(handle)
        """
        status = nxlib.nxiinitgroupdir_(self.handle)
        if status == ERROR:
            raise NeXusError("Could not reset group scan: %s" % (self._loc()))

    nxlib.nxigetnextentry_.restype = c_int
    nxlib.nxigetnextentry_.argtypes = [c_void_p, c_char_p, c_char_p, c_int_p]
    def getnextentry(self):
        """
        Return the next entry in the group as name,nxclass tuple. If
        end of data is reached this returns the tuple (None, None)

        Raises NeXusError if this fails.

        Corresponds to NXgetnextentry(handle,name,nxclass,&storage).

        This function doesn't return the storage class for data entries
        since getinfo returns shape and storage, both of which are required
        to read the data.

        Note that HDF4 files can have entries in the file with classes
        that don't need to be processed.  If the file follows the standard
        NeXus DTDs then skip any entry for which nxclass.startswith('NX')
        is False.  For non-conforming files, skip those entries with
        nxclass in nxs.H4SKIP.
        """
        name = ctypes.create_string_buffer(MAXNAMELEN)
        nxclass = ctypes.create_string_buffer(MAXNAMELEN)
        storage = c_int(0)
        status = nxlib.nxigetnextentry_(self.handle,name,nxclass,_ref(storage))
        if status == EOD:
            return (None, None)
        if status == ERROR:
            raise NeXusError("Could not get next entry: %s" % (self._loc()))
        ## Note: ignoring storage --- it is useless without dimensions
        # if nxclass == 'SDS':
        #     dtype = _pytype_code(storage.value)
        # print("nextentry", nxclass.value, name.value, storage.value)
        return name.value,nxclass.value

    def getentries(self):
        """
        Return a dictionary of the groups[name]=type below the
        existing open one.

        Raises NeXusError if this fails.
        """
        self.initgroupdir()
        result = {}
        (name, nxclass) = self.getnextentry()
        if (name, nxclass) != (None, None):
            result[name] = nxclass
        while (name, nxclass) != (None, None):
            result[name] = nxclass
            (name, nxclass) = self.getnextentry()
        return result

    def __getnxclass(self, target):
        """
        Return the nxclass of the supplied name.
        """
        self.initgroupdir()
        while True:
            (nxname, nxclass) = self.getnextentry()
            if nxname == target:
                return nxclass
            if nxname is None:
                break
        raise NeXusError("Failed to find entry with name \"%s\" at %s" %
                         (target, self.path))

    def entries(self):
        """
        Iterator of entries.

        for name,nxclass in nxs.entries():
            process(name,nxclass)

        This automatically opens the corresponding group/data for you,
        and closes it when you are done.  Do not rely on any paths
        remaining open between entries as we restore the current
        path each time.

        This does not correspond to an existing NeXus API function,
        but instead combines the work of initgroupdir/getnextentry
        and open/close on data and group.  Entries in nxs.H4SKIP are
        ignored.
        """
        # To preserve the semantics we must read in the whole list
        # first, then process the entries one by one.  Keep track
        # of the path so we can restore it between entries.
        path = self.path

        # Read list of entries
        self.initgroupdir()
        n,_,_ = self.getgroupinfo()
        L = []
        for dummy in range(n):
            name,nxclass = self.getnextentry()
            if nxclass not in H4SKIP:
                L.append((name,nxclass))
        for name,nxclass in L:
            self.openpath(path)  # Reset the file cursor
            if nxclass == "SDS":
                self.opendata(name)
            else:
                self.opengroup(name,nxclass)
            yield name,nxclass

    # ==== Data ====
    nxlib.nxigetrawinfo64_.restype = c_int
    nxlib.nxigetrawinfo64_.argtypes = [c_void_p, c_int_p, c_void_p, c_int_p]
    def getrawinfo(self):
        """
        Returns the tuple dimensions,type for the currently open dataset.
        Dimensions is an integer array whose length corresponds to the rank
        of the dataset and whose elements are the size of the individual
        dimensions.  Storage type is returned as a string, with 'char' for
        a stored string, '[u]int[8|16|32]' for various integer values or
        'float[32|64]' for floating point values.  No support for
        complex values.

        Unlike getinfo(), the size of the string storage area is
        returned rather than the length of the stored string.

        Raises NeXusError if this fails.

        Corresponds to NXgetrawinfo(handle, &rank, dims, &storage),
        but with storage converted from HDF values to numpy compatible
        strings, and rank implicit in the length of the returned dimensions.
        """
        rank = c_int(0)
        shape = numpy.zeros(MAXRANK, 'int64')
        storage = c_int(0)
        status = nxlib.nxigetrawinfo64_(self.handle, _ref(rank),
                                        shape.ctypes.data, _ref(storage))
        if status == ERROR:
            raise NeXusError("Could not get data info: %s" % (self._loc()))
        shape = shape[:rank.value]+0
        dtype = _pytype_code[storage.value]
        # print("getrawinfo", self._loc(), "->", shape, dtype)
        return shape,dtype

    nxlib.nxigetinfo64_.restype = c_int
    nxlib.nxigetinfo64_.argtypes = [c_void_p, c_int_p, c_void_p, c_int_p]
    def getinfo(self):
        """
        Returns the tuple dimensions,type for the currently open dataset.
        Dimensions is an integer array whose length corresponds to the rank
        of the dataset and whose elements are the size of the individual
        dimensions.  Storage type is returned as a string, with 'char' for
        a stored string, '[u]int[8|16|32]' for various integer values or
        'float[32|64]' for floating point values.  No support for
        complex values.

        Unlike getrawinfo(), the length of the stored string is
        returned rather than the size of the string storage area.

        Raises NeXusError if this fails.

        Note that this is the recommended way to establish if you have
        a dataset open.

        Corresponds to NXgetinfo(handle, &rank, dims, &storage),
        but with storage converted from HDF values to numpy compatible
        strings, and rank implicit in the length of the returned dimensions.
        """
        rank = c_int(0)
        shape = numpy.zeros(MAXRANK, 'int64')
        storage = c_int(0)
        status = nxlib.nxigetinfo64_(self.handle, _ref(rank),
                                     shape.ctypes.data,
                                     _ref(storage))
        if status == ERROR:
            raise NeXusError("Could not get data info: %s" % (self._loc()))
        shape = shape[:rank.value]+0
        dtype = _pytype_code[storage.value]
        # print("getinfo", self._loc(), "->", shape, dtype)
        return shape,dtype

    nxlib.nxiopendata_.restype = c_int
    nxlib.nxiopendata_.argtypes = [c_void_p, c_char_p]
    def opendata(self, name):
        """
        Open the named data set within the current group.

        Raises ValueError if could not open the dataset.

        Corresponds to NXopendata(handle, name)
        """
        # print("opendata", self._loc(), name)
        if self._indata:
            status = ERROR
        else:
            status = nxlib.nxiopendata_(self.handle, name)
        if status == ERROR:
            raise ValueError("Could not open data %s: %s" % (name, self._loc()))
        self._path.append((name,"SDS"))
        self._indata = True

    nxlib.nxiclosedata_.restype = c_int
    nxlib.nxiclosedata_.argtypes = [c_void_p]
    def closedata(self):
        """
        Close the currently open data set.

        Raises NeXusError if this fails (e.g., because no
        dataset is open).

        Corresponds to NXclosedata(handle)
        """
        # print("closedata")
        status = nxlib.nxiclosedata_(self.handle)
        if status == ERROR:
            raise NeXusError("Could not close data at %s" % (self._loc()))
        self._path.pop()
        self._indata = False

    nxlib.nximakedata64_.restype = c_int
    nxlib.nximakedata64_.argtypes  = [c_void_p, c_char_p, c_int, c_int, c_int64_p]
    def makedata(self, name, dtype=None, shape=None):
        """
        Create a data element of the given type and shape.  See getinfo
        for details on types.  This does not open the data for writing.

        Set the first dimension to nxs.UNLIMITED, for extensible data sets,
        and use putslab to write individual slabs.

        Raises ValueError if it fails.

        Corresponds to NXmakedata(handle,name,type,rank,dims)
        """
        # TODO: With keywords for compression and chunks, this can act as
        # TODO: compmakedata.
        # TODO: With keywords for value and attr, this can be used for
        # TODO: makedata, opendata, putdata, putattr, putattr, ..., closedata
        # print("makedata", self._loc(), name, shape, dtype)
        storage = _nxtype_code[str(dtype)]
        shape = numpy.asarray(shape,'int64')
        status = nxlib.nximakedata64_(self.handle,name,storage,len(shape),
                                      shape.ctypes.data_as(c_int64_p))
        if status == ERROR:
            raise ValueError("Could not create data %s: %s" %
                             (name,self._loc()))

    nxlib.nxicompmakedata64_.restype = c_int
    nxlib.nxicompmakedata64_.argtypes  = [c_void_p, c_char_p, c_int, c_int, c_int64_p,
                                          c_int, c_int64_p]
    def compmakedata(self, name, dtype=None, shape=None, mode='lzw',
                     chunks=None):
        """
        Create a data element of the given dimensions and type.  See
        getinfo for details on types.  Compression mode is one of
        'none', 'lzw', 'rle' or 'huffman'.  chunks gives the alignment
        of the compressed chunks in the data file.  There should be one
        chunk size for each dimension in the data.

        Defaults to mode='lzw' with chunk size set to the length of the
        fastest varying dimension.

        Raises ValueError if it fails.

        Corresponds to NXmakedata(handle,name,type,rank,dims).
        """
        storage = _nxtype_code[str(dtype)]
        # Make sure shape/chunk_shape are integers; hope that 32/64 bit issues
        # with the c int type sort themselves out.
        dims = numpy.asarray(shape,'int64')
        if chunks is None:
            chunks = numpy.ones(dims.shape,'int64')
            chunks[-1] = shape[-1]
        else:
            chunks = numpy.array(chunks,'int64')
        status = nxlib.nxicompmakedata64_(self.handle,name,storage,len(dims),
                                          dims.ctypes.data_as(c_int64_p),
                                          _compression_code[mode],
                                          chunks.ctypes.data_as(c_int64_p))
        if status == ERROR:
            raise ValueError("Could not create compressed data %s: %s" %
                             (name, self._loc()))

    nxlib.nxigetdata_.restype = c_int
    nxlib.nxigetdata_.argtypes = [c_void_p, c_void_p]
    def getdata(self):
        """
        Return the data.  If data is a string (1-D char array), a python
        string is returned.  If data is a scalar (1-D numeric array of
        length 1), a python scalar is returned.  If data is a string
        array, a numpy array of type 'S#' where # is the maximum string
        length is returned.  If data is a numeric array, a numpy array
        is returned.

        Raises ValueError if this fails.

        Corresponds to NXgetdata(handle, data)
        """
        # TODO: consider accepting preallocated data so we don't thrash memory
        shape,dtype = self.getinfo()
        dummy_data,pdata,dummy_size,datafn = self._poutput(dtype,shape)
        status = nxlib.nxigetdata_(self.handle,pdata)
        if status == ERROR:
            raise ValueError("Could not read data: %s" % (self._loc()))
        # print("getdata", self._loc(), shape, dtype)
        return datafn()

    nxlib.nxigetslab64_.restype = c_int
    nxlib.nxigetslab64_.argtypes = [c_void_p, c_void_p, c_int64_p, c_int64_p]
    def getslab(self, slab_offset, slab_shape):
        """
        Get a slab from the data array.

        Offsets are 0-origin.  Shape can be inferred from the data.
        Offset and shape must each have one entry per dimension.

        Raises ValueError if this fails.

        Corresponds to NXgetslab(handle,data,offset,shape)
        """
        # TODO: consider accepting preallocated data so we don't thrash memory
        dummy_shape,dtype = self.getrawinfo()
        dummy_data,pdata,dummy_size,datafn = self._poutput(dtype,slab_shape)
        slab_offset = numpy.asarray(slab_offset,'int64')
        slab_shape = numpy.asarray(slab_shape,'int64')
        status = nxlib.nxigetslab64_(self.handle,pdata,
                                     slab_offset.ctypes.data_as(c_int64_p),
                                     slab_shape.ctypes.data_as(c_int64_p))
        # print("slab", offset, size, data)
        if status == ERROR:
            raise ValueError("Could not read slab: %s" % (self._loc()))
        return datafn()

    nxlib.nxiputdata_.restype = c_int
    nxlib.nxiputdata_.argtypes = [c_void_p, c_void_p]
    def putdata(self, data):
        """
        Write data into the currently open data block.

        Raises ValueError if this fails.

        Corresponds to NXputdata(handle, data)
        """
        shape,dtype = self.getrawinfo()
        # print("putdata", self._loc(), shape, dtype)
        data,pdata = self._pinput(data,dtype,shape)
        status = nxlib.nxiputdata_(self.handle,pdata)
        if status == ERROR:
            raise ValueError("Could not write data: %s" % (self._loc()))

    nxlib.nxiputslab64_.restype = c_int
    nxlib.nxiputslab64_.argtypes = [c_void_p, c_void_p, c_int64_p, c_int64_p]
    def putslab(self, data, slab_offset, slab_shape):
        """
        Put a slab into the data array.

        Offsets are 0-origin.  Shape can be inferred from the data.
        Offset and shape must each have one entry per dimension.

        Raises ValueError if this fails.

        Corresponds to NXputslab(handle,data,offset,shape)
        """
        dummy_shape,dtype = self.getrawinfo()
        data,pdata = self._pinput(data,dtype,slab_shape)
        slab_offset = numpy.asarray(slab_offset,'int64')
        slab_shape = numpy.asarray(slab_shape,'int64')
        # print("slab", offset, size, data)
        status = nxlib.nxiputslab64_(self.handle,pdata,
                                     slab_offset.ctypes.data_as(c_int64_p),
                                     slab_shape.ctypes.data_as(c_int64_p))
        if status == ERROR:
            raise ValueError("Could not write slab: %s" % (self._loc()))



    # ==== Attributes ====
    nxlib.nxiinitattrdir_.restype = c_int
    nxlib.nxiinitattrdir_.argtypes = [c_void_p]
    def initattrdir(self):
        """
        Reset the getnextattr list to the first attribute.

        Raises NeXusError if this fails.

        Corresponds to NXinitattrdir(handle)
        """
        status = nxlib.nxiinitattrdir_(self.handle)
        if status == ERROR:
            raise NeXusError("Could not reset attribute list: %s" %
                             (self._loc()))

    nxlib.nxigetattrinfo_.restype = c_int
    nxlib.nxigetattrinfo_.argtypes = [c_void_p, c_int_p]
    def getattrinfo(self):
        """
        Returns the number of attributes for the currently open
        group/data object.  Do not call getnextattr() more than
        this number of times.

        Raises NeXusError if this fails.

        Corresponds to NXgetattrinfo(handl, &n)
        """
        n = c_int(0)
        status = nxlib.nxigetattrinfo_(self.handle,_ref(n))
        if status == ERROR:
            raise NeXusError("Could not get attr info: %s" % (self._loc()))
        # print("num attrs", n.value)
        return n.value

    nxlib.nxigetnextattr_.restype = c_int
    nxlib.nxigetnextattr_.argtypes = [c_void_p, c_char_p, c_int_p, c_int_p]
    def getnextattr(self):
        """
        Returns the name, length, and data type for the next attribute.
        Call getattrinfo to determine the number of attributes before
        calling getnextattr. Data type is returned as a string.  See
        getinfo for details.  Length is the number of elements in the
        attribute.

        Raises NeXusError if NeXus returns ERROR or EOD.

        Corresponds to NXgetnextattr(handle,name,&length,&storage)
        but with storage converted from HDF values to numpy compatible
        strings.

        Note: NeXus API documentation seems to say that length is the number
        of bytes required to store the entire attribute.
        """
        name = ctypes.create_string_buffer(MAXNAMELEN)
        length = c_int(0)
        storage = c_int(0)
        status = nxlib.nxigetnextattr_(self.handle,name,_ref(length),_ref(storage))
        if status == EOD:
            return (None, None, None)
        if status == ERROR or status == EOD:
            raise NeXusError("Could not get next attr: %s" % (self._loc()))
        dtype = _pytype_code[storage.value]
        # print("getnextattr", name.value, length.value, dtype)
        return name.value, length.value, dtype

    # TODO: Resolve discrepency between NeXus API documentation and
    # TODO: apparent behaviour for getattr/putattr length.
    nxlib.nxigetattr_.restype = c_int
    nxlib.nxigetattr_.argtypes = [c_void_p, c_char_p, c_void_p, c_int_p, c_int_p]
    def getattr(self, name, length, dtype):
        """
        Returns the value of the named attribute.  Requires length and
        data type from getnextattr to allocate the appropriate amount of
        space for the attribute.

        Corresponds to NXgetattr(handle,name,data,&length,&storage)
        """
        if dtype=='char': length += 1  # HDF4 needs zero-terminator # RDR "is" not understood in python 3
        dummy_data,pdata,size,datafn = self._poutput(str(dtype),[length])
        storage = c_int(_nxtype_code[str(dtype)])
        # print("getattr", self._loc(), name, length, size, dtype)
        size = c_int(size)
        status = nxlib.nxigetattr_(self.handle,name,pdata,_ref(size),_ref(storage))
        if status == ERROR:
            raise ValueError("Could not read attr %s: %s" % (name, self._loc()))
        # print("getattr", self._loc(), name, datafn())
        return datafn()

    nxlib.nxiputattr_.restype = c_int
    nxlib.nxiputattr_.argtypes = [c_void_p, c_char_p, c_void_p, c_int, c_int]
    def putattr(self, name, value, dtype = None):
        """
        Saves the named attribute.  The attribute value is a string
        or a scalar.

        Raises TypeError if the value type is incorrect.
        Raises NeXusError if the attribute could not be saved.

        Corresponds to NXputattr(handle,name,data,length,storage)

        Note length is the number of elements to write rather
        than the number of bytes to write.
        """
        # Establish attribute type
        if dtype == None:
            # Type is inferred from value
            if hasattr(value,'dtype'):
                dtype = str(value.dtype)
            elif _is_string_like(value):
                dtype = 'char'
            else:
                value = numpy.array(value)
                dtype = str(value.dtype)
        else:
            # Set value to type
            dtype = str(dtype)
            if dtype == 'char' and not _is_string_like(value):
                raise TypeError("Expected string for 'char' attribute value")
            if dtype != 'char':
                value = numpy.array(value,dtype=dtype)

        # Determine shape
        if dtype == 'char':
            length = len(value)
            data = value
        elif numpy.prod(value.shape) != 1:
            # NAPI silently ignores attribute arrays
            raise TypeError("Attribute value must be scalar or string")
        else:
            length = 1
            data = value.ctypes.data

        # Perform the call
        storage = c_int(_nxtype_code[dtype])
        status = nxlib.nxiputattr_(self.handle,name,data,length,storage)
        if status == ERROR:
            raise NeXusError("Could not write attr %s: %s" %
                             (name, self._loc()))

    def getattrs(self):
        """
        Returns a dicitonary of the attributes on the current node.

        This is a second form of attrs(self).
        """
        result = {}
        for (name, value) in self.attrs():
            result[name] = value
        return result

    def attrs(self):
        """
        Iterate over attributes.

        for name,value in file.attrs():
            process(name,value)

        This automatically reads the attributes of the group/data.  Do not
        change the active group/data while processing the list.

        This does not correspond to an existing NeXus API function, but
        combines the work of attrinfo/initattrdir/getnextattr/getattr.
        """
        self.initattrdir()
        n = self.getattrinfo()
        for dummy in range(n):
            name,length,dtype = self.getnextattr()
            value = self.getattr(name,length,dtype)
            yield name,value

    # ==== Linking ====
    nxlib.nxigetgroupid_.restype = c_int
    nxlib.nxigetgroupid_.argtypes = [c_void_p, c_NXlink_p]
    def getgroupID(self):
        """
        Return the id of the current group so we can link to it later.

        Raises NeXusError

        Corresponds to NXgetgroupID(handle, &ID)
        """
        ID = _NXlink()
        status = nxlib.nxigetgroupid_(self.handle,_ref(ID))
        if status == ERROR:
            raise NeXusError("Could not link to group: %s" % (self._loc()))# RDR
        return ID

    nxlib.nxigetdataid_.restype = c_int
    nxlib.nxigetdataid_.argtypes = [c_void_p, c_NXlink_p]
    def getdataID(self):
        """
        Return the id of the current data so we can link to it later.

        Raises NeXusError

        Corresponds to NXgetdataID(handle, &ID)
        """
        ID = _NXlink()
        status = nxlib.nxigetdataid_(self.handle,_ref(ID))
        if status == ERROR:
            raise NeXusError("Could not link to data: %s" % (self._loc()))
        return ID

    nxlib.nximakelink_.restype = c_int
    nxlib.nximakelink_.argtypes = [c_void_p, c_NXlink_p]
    def makelink(self, ID):
        """
        Link the previously captured group/data ID into the currently
        open group.

        Raises NeXusError

        Corresponds to NXmakelink(handle, &ID)
        """
        status = nxlib.nximakelink_(self.handle,_ref(ID))
        if status == ERROR:
            raise NeXusError("Could not make link: %s" % (self._loc()))

    nxlib.nximakenamedlink_.restype = c_int
    nxlib.nximakenamedlink_.argtypes = [c_void_p, c_char_p, c_NXlink_p]
    def makenamedlink(self,name,ID):
        """
        Link the previously captured group/data ID into the currently
        open group, but under a different name.

        Raises NeXusError

        Corresponds to NXmakenamedlink(handle,name,&ID)
        """
        status = nxlib.nximakenamedlink_(self.handle,name,_ref(ID))
        if status == ERROR:
            raise NeXusError("Could not make link %s: %s" % (name, self._loc()))

    nxlib.nxisameid_.restype = c_int
    nxlib.nxisameid_.argtypes = [c_void_p, c_NXlink_p, c_NXlink_p]
    def sameID(self, ID1, ID2):
        """
        Return True of ID1 and ID2 point to the same group/data.

        This should not raise any errors.

        Corresponds to NXsameID(handle,&ID1,&ID2)
        """
        status = nxlib.nxisameid_(self.handle, _ref(ID1), _ref(ID2))
        return status == OK

    nxlib.nxiopensourcegroup_.restype = c_int
    nxlib.nxiopensourcegroup_.argtyps = [c_void_p]
    def opensourcegroup(self):
        """
        If the current node is a linked to another group or data, then
        open the group or data that it is linked to.

        Note: it is unclear how can we tell if we are linked, other than
        perhaps the existence of a 'target' attribute in the current item.

        Raises NeXusError.

        Corresponds to NXopensourcegroup(handle)
        """
        status = nxlib.nxiopensourcegroup_(self.handle)
        if status == ERROR:
            raise NeXusError("Could not open source group: %s" % (self._loc()))

    def link(self):
        """
        Returns the item which the current item links to, or None if the
        current item is not linked.  This is equivalent to scanning the
        attributes for target and returning it if target is not equal
        to self.

        This does not correspond to an existing NeXus API function, but
        combines the work of attrinfo/initattrdir/getnextattr/getattr.
        """
        n = self.getattrinfo()
        self.initattrdir()
        for dummy in range(n):
            name,length,dtype = self.getnextattr()
            if name == "target":
                target = self.getattr(name,length,dtype)
                # print("target %s, path %s" % (target,self.path))
                if target != self.path:
                    return target
                else:
                    return None
        return None

    # ==== External linking ====
    nxlib.nxiinquirefile_.restype = c_int
    nxlib.nxiinquirefile_.argtypes = [c_void_p, c_char_p, c_int]
    def inquirefile(self, maxnamelen=MAXPATHLEN):
        """
        Return the filename for the current file.  This may be different
        from the file that was opened (file.filename) if the current
        group is an external link to another file.

        Raises NeXusError if this fails.

        Corresponds to NXinquirefile(&handle,file,len)
        """
        filename = ctypes.create_string_buffer(maxnamelen)
        status = nxlib.nxiinquirefile_(self.handle,filename,maxnamelen)
        if status == ERROR:
            raise NeXusError("Could not determine filename: %s" % (self._loc()))
        return filename.value

    nxlib.nxilinkexternal_.restype = c_int
    nxlib.nxilinkexternal_.argtyps = [c_void_p, c_char_p,
                                       c_char_p, c_char_p]
    def linkexternal(self, name, nxclass, url):
        """
        Return the filename for the external link if there is one,
        otherwise return None.

        Raises NeXusError if link fails.

        Corresponds to NXisexternalgroup(&handle,name,nxclass,file,len)
        """
        status = nxlib.nxilinkexternal_(self.handle,name,nxclass,url)
        if status == ERROR:
            raise NeXusError("Could not link %s to %s: %s" %
                             (name, url, self._loc()))

    nxlib.nxiisexternalgroup_.restype = c_int
    nxlib.nxiisexternalgroup_.argtyps = [c_void_p, c_char_p,
                                       c_char_p, c_char_p, c_int]
    def isexternalgroup(self, name, nxclass, maxnamelen=MAXPATHLEN):
        """
        Return the filename for the external link if there is one,
        otherwise return None.

        Corresponds to NXisexternalgroup(&handle,name,nxclass,file,len)
        """
        url = ctypes.create_string_buffer(maxnamelen)
        status = nxlib.nxiisexternalgroup_(self.handle,name,nxclass,
                                              url,maxnamelen)
        if status == ERROR:
            return None
        else:
            return url.value

    # ==== Utility functions ====
    def _loc(self):
        """
        Return file location as string filename(path)

        This is an extension to the NeXus API.
        """
        return "%s(%s)"%(self.filename,self.path)

    def _poutput(self, dtype, shape):
        """
        Build space to collect a nexus data element.
        Returns data,pdata,size,datafn where
        - data is a python type to hold the returned data
        - pdata is the pointer to the start of the data
        - size is the number of bytes in the data block
        - datafn is a lamba expression to extract the return value from data
        Note that datafn can return a string, a scalar or an array depending
        on the data type and shape of the data group.
        """
        if isinstance(shape, int):
            shape = [shape]
        if len(shape) == 1 and dtype == 'char':
            # string - use ctypes allocator
            size = int(shape[0])
            data = ctypes.create_string_buffer(size)
            pdata = data
            datafn = lambda: data.value
        else:
            # scalar, array or string list - use numpy array
            if dtype=='char':
                data = numpy.zeros(shape[:-1], dtype='S%i'%shape[-1])
            else:
                data = numpy.zeros(shape, dtype)
            if len(shape) == 1 and shape[0] == 1:
                datafn = lambda: data[0]
            else:
                datafn = lambda: data
            pdata = data.ctypes.data
            size = data.nbytes
        return data,pdata,size,datafn

    def _pinput(self, data, dtype, shape):
        """
        Convert an input array to a C pointer to a dense array.

        Returns data, pdata where
        - data is a possibly new copy of the array
        - pdata is a pointer to the beginning of the array.
        Note that you must hold a reference to data for as long
        as you need pdata to keep the memory from being released to the heap.
        """
        if isinstance(shape, int):
            shape = [shape]
        if dtype == "char":
            data = numpy.asarray(data, dtype='S%d'%(shape[-1]))
        else:
            # Convert scalars to vectors of length one
            if numpy.prod(shape) == 1 and not hasattr(data,'shape'):
                data = numpy.array([data], dtype=dtype)
            # Check that dimensions match
            # Ick! need to exclude dimensions of length 1 in order to catch
            # array slices such as a[:,1], which only report one dimension
            input_shape = numpy.array([i for i in data.shape if i != 1])
            target_shape = numpy.array([i for i in shape if i != 1])
            if len(input_shape) != len(target_shape) \
                    or (input_shape != target_shape).any():
                raise ValueError("Shape mismatch %s!=%s: %s" %
                                 (data.shape, shape, self._loc()))
            # Check data type
            if str(data.dtype) != dtype:
                raise ValueError("Type mismatch %s!=%s: %s" %
                                 (dtype, data.dtype, self._loc()))

        data = numpy.ascontiguousarray(data)
        pdata = data.ctypes.data

        return data,pdata

    def show(self, path=None, indent=0):
        """
        Print the structure of a NeXus file from the current node.

        TODO: Break this into a tree walker and a visitor.
        """
        oldpath = self.path
        self.openpath(path)

        print("=== File", self.inquirefile(), path)
        self._show(indent=indent)
        self.openpath(oldpath)

    def _show(self, indent=0):
        """
        Print the structure of a NeXus file from the current node.

        TODO: Break this into a tree walker and a visitor.
        """
        prefix = ' '*indent
        link = self.link()
        if link:
            print("%(prefix)s-> %(link)s" % locals())
            return
        for attr,value in self.attrs():
            print("%(prefix)s@%(attr)s: %(value)s" % locals())
        for name,nxclass in self.entries():
            if nxclass == b'SDS': # RDR
                shape,dtype = self.getinfo()
                dims = "x".join([str(x) for x in shape])
                print("%(prefix)s%(name)s %(dtype)s %(dims)s" % locals())
                link = self.link()
                if link:
                    print("  %(prefix)s-> %(link)s" % locals())
                else:
                    for attr,value in self.attrs():
                        print("  %(prefix)s@%(attr)s: %(value)s" % locals())
                    if numpy.prod(shape) < 8:
                        value = self.getdata()
                        print("  %s%s"%(prefix,str(value)))
            else:
                print("%(prefix)s%(name)s %(nxclass)s" % locals())
                self._show(indent=indent+2)


__id__ = "$ID$"
