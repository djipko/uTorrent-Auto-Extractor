'''
Created on Mar 2, 2011

@author: Vladimir Cvetic
'''
import ConfigParser, os, sys, re
from _winreg import OpenKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, QueryValueEx

global ConfigDefault 
ConfigDefault = {
    "Values.imdb":                      "1",
    "Values.storage_dir":               "%USERPROFILE%\\Downloads\\Storage",
    "Values.levenshtein":               "6",
    "Values.7zip":                      "auto",
    "Values.7zip_binary":               "7z.exe",
    "Values.use_labels":                "1",
    "Values.label_folders":             "video:%USERPROFILE%\\videos;music:%USERPROFILE%\\music;",
    "Values.debug":                     "0"
    }

def get_utorrent_labels():
    """
    fetches all defined labels in utorrent
    """

def write_config(config):
    """
    given a dictionary with key's of the form 'section.option: value'
    write() generates a list of unique section names
    creates sections based that list
    use config.set to add entries to each section
    """
    cp = ConfigParser.ConfigParser()
    sections = set([k.split('.')[0] for k in config.keys()])
    map(cp.add_section, sections)
    for k,v in config.items():
        s, o = k.split('.')
        cp.set(s, o, v)
    cp.write(open(os.path.join(os.path.dirname(sys.argv[0]), 'config.ini'), "w"))

def read_config():
    options = {}
    config = ConfigParser.ConfigParser()
    userprofile = os.environ['USERPROFILE'];
    conf_filename = os.path.join(os.path.dirname(sys.argv[0]), 'config.ini')
    
    if os.path.exists(conf_filename)==False:
        write_config(ConfigDefault)
         
    config.read(conf_filename)  
    
    options['use_labels'] = config.getboolean('Values', 'use_labels')
    options['imdb_flag'] = config.getboolean('Values', 'imdb')
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
        
    return options
