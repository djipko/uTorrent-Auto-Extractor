'''
Created on Mar 2, 2011

@author: Vladimir Cvetic
'''
import ConfigParser, os, sys, re
#from _winreg import OpenKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, QueryValueEx

global ConfigDefault 
ConfigDefault = {
    "Global":{"imdb":         "1",
              "storage_dir":  "%USERPROFILE%\\Downloads\\Storage",
              "levenshtein":  "6",
              "use_labels":   "1",
              "debug":        "0"
              },
    
    "Labels":{}
    }
global conf_filename
conf_filename = os.path.join(os.path.dirname(sys.argv[0]), 'config.ini')

def resetToDefault():
    os.remove(conf_filename)
    write_config()

def write_config(config=None):
    """
    given a dictionary with key's of the form 'section.option: value'
    write() generates a list of unique section names
    creates sections based that list
    use config.set to add entries to each section
    """
    if config is None:
        config = ConfigDefault

    
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
    
    if os.path.exists(conf_filename)==False:
        write_config(ConfigDefault)
         
    config.read(conf_filename)  
    
    for section in config.sections():
        options[section] = {}
        opts = config.options(section)
        for opt in opts:
            parsed = re.sub('\%USERPROFILE\%', os.environ['USERPROFILE'], config.get(section, opt))
            #print parsed
            options[section][opt] = parsed

    return options
