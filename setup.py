from distutils.core import setup
import py2exe

setup(console=['autoextractor.py'], windows=['configuration.py'],
      options = {"py2exe": {"packages" : ['lxml', 'sip'], "bundle_files": 1}},
      zipfile = "shared.lib",      
      )