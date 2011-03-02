'''
Created on Mar 2, 2011

@author: Vladimir Cvetic
'''
import ConfigParser, os, sys, re
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

def get_utorrent_labels():
    """
    fetches all defined labels in utorrent
    """

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
    print options
    return options
    """
    userprofile = os.environ['USERPROFILE'];
    options['use_labels'] = config.getboolean('Values', 'use_labels')
    options['imdb'] = config.getboolean('Values', 'imdb')
    options['debug'] = config.getboolean('Values', 'debug')
    options['sevenzip'] = config.get('Values', '7zip')
    options['levenshtein'] = config.get('Values', 'levenshtein')
    options['sevenzip_binary'] = config.get('Values', '7zip_binary')
    options['storage_dir'] = config.get('Values', 'storage_dir')
    options['supported_formats'] = '^(.*)\.((zip|rar|7z|gz|bz|tar)|(r[0-9]{1,3})|([0-9]{1,3}))$'
    options['storage_dir'] = re.sub('\%USERPROFILE\%', userprofile, options['storage_dir'])
    
    label_folders = config.get('Values', 'label_folders')
    options['label_folders'] = re.sub('\%USERPROFILE\%', userprofile, label_folders).split(';')
      
    if options['sevenzip'] == 'auto':
        t = OpenKey(HKEY_CURRENT_USER, r"Software\7-Zip", 0, KEY_ALL_ACCESS)
        if t == False:
            print 'Unable to find 7-Zip in registry. Please manualy enter full path in config.ini'
        options['sevenzip_path'] = QueryValueEx(t, 'Path')[0]
        if options['sevenzip_path'] == False:
            print 'Unable to find 7-Zip in registry. Please manualy enter full path in config.ini'
    else:
        options['sevenzip_path'] = options['sevenzip']
    
    options['full_sevenzip_path'] = os.path.join(options['sevenzip_path'], options['sevenzip_binary'])
    if os.path.exists(options['full_sevenzip_path'])==False:
        if options['debug']:
            print "full 7zip path: ".format(options['full_sevenzip_path'])
        print "{} can not be found. Please fix errors in config.ini".format(options['full_sevenzip_path'])

    if os.path.exists(options['storage_dir'])==False:
        print "{} doesn't exist, attempting to make dir".format(options['storage_dir'])
        os.mkdir(options['storage_dir'])
        if os.path.exists(options['storage_dir'])==False:
            print "failed to create {}, please create it manually".format(options['storage_dir'])
            sys.exit()
    """   
    return options
