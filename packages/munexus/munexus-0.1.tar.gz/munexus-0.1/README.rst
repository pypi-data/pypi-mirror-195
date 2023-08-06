NeXus hack for a very limited access to the library

Aim
===
  To read ISIS muon data, such as:: 
     EMU00020882.nxs 
     
  into python without compiling any os-dependent code.
  (nexusformat reader.py from `<https://github.com/nexusformat/python-nxs>`_ is broken on in python3)

Requisites for the hack
=======================
  You just need a nexus library installed as, e.g.:: 
     libnexus1         [/focal,now 4.4.3-4 amd64 on Ubuntu 20.04]
     on macos   see `<https://github.com/nexusformat/code/blob/master/README.macos>`_
     on windows with `<https://github.com/nexusformat/code/blob/master/README.cygwin`_ if you have `<https://www.cygwin.com/>`_
     on windows with `<https://github.com/nexusformat/code/blob/master/README.VS2008.pdf>`_ if you have Visual Studio 2008
  
  To understand what's inside EMU00020882.nxs it is useful to have::
     nexus-tools       [/focal,now 4.4.3-4 amd64 on Ubuntu 20.04]
  
Python 3
========
  This hack works only with python3
  
How
===
  python3 trymunxs.py
  (requires that matplotlib and numpy are installed, but only for this demo purposes)
