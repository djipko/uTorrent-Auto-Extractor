from distutils.core import setup
import py2exe

setup(console=['autoextractor.py'], windows=['configui.py'],
      options = {"py2exe": {"packages" : ['lxml', 'gzip', 'configobj'], "bundle_files": 1}},
      zipfile = "shared.lib",      
      )