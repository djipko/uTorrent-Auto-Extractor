'''
Created on Mar 2, 2011

@author: Vladimir Cvetic
'''
import ConfigParser, os, sys
from _winreg import OpenKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, QueryValueEx

global ConfigDefault 
ConfigDefault = {
    "Global":{"imdb":         "1",
              "storage_dir":  "%USERPROFILE%\\Downloads\\Storage",
              "levenshtein":  "6",
              "use_labels":   "1",
              "debug":        "0",
              "7zip":         "-1"},
    
    "Labels":{}
    }

def write_config(config=None):
    """
    given a dictionary with key's of the form 'section.option: value'
    write() generates a list of unique section names
    creates sections based that list
    use config.set to add entries to each section
    """
    if config is None:
        config = ConfigDefault
    
    if config['Global']['7zip'] == '-1':
        if OpenKey(HKEY_CURRENT_USER, r"Software\7-Zip", 0, KEY_ALL_ACCESS):
            t = OpenKey(HKEY_CURRENT_USER, r"Software\7-Zip", 0, KEY_ALL_ACCESS) 
            sevenzip_path = QueryValueEx(t, 'Path')[0]
            sevenzip = '{}\\7z.exe'.format(sevenzip_path)  
            config['Global']['7zip'] = sevenzip;
        else:
            config['Global']['7zip'] = ''
    
    conf_filename = os.path.join(os.path.dirname(sys.argv[0]), 'config.ini')
    rcp = ConfigParser.ConfigParser()  
    rcp.read(conf_filename) 
    
    for section in config:
        if rcp.has_section(section) == False:
            rcp.add_section(section)
        for opt in config[section]:
            rcp.set(section, opt, config[section][opt])
    
    rcp.write(open(conf_filename, "w"))

def read_config():
    options = {}
    config = ConfigParser.ConfigParser()    
    conf_filename = os.path.join(os.path.dirname(sys.argv[0]), 'config.ini')
    
    if os.path.exists(conf_filename)==False:
        write_config(ConfigDefault)
         
    config.read(conf_filename)  
    
    for section in config.sections():
        options[section] = {}
        opts = config.options(section)
        for opt in opts:
            options[section][opt] = config.get(section, opt)
  
    return options
