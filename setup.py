from distutils.core import setup
import py2exe
import getopt, sys, os, subprocess, imdb, re, jellyfish, lxml

setup(console=['autoextractor.py'], windows=['configui.py'],
      options = {"py2exe": {"packages" : ['lxml', 'gzip', 'configobj'], "bundle_files": 1}},
      zipfile = "shared.lib",      
      )