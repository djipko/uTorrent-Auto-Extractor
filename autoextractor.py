import getopt, sys, subprocess, imdb, re, jellyfish, ConfigParser, os, bencode, configui
from _winreg import OpenKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, QueryValueEx
from shutil import copy2, Error, copystat
    
global ConfigDefault    
ConfigDefault = {
    "Values.imdb":                      "1",
    "Values.storage_dir":               "%USERPROFILE%\\Downloads\\Storage",
    "Values.levenshtein":               "6",
    "Values.7zip":                      "auto",
    "Values.7zip_binary":               "7z.exe",
    "Values.use_labels":                "1",
    "Values.label_folders":             "video:%USERPROFILE%\\videos;music:%USERPROFILE%\\music;",
    "Values.debug":                     "0",
    "Lables.imdb":                      "Use Imbd:",
    "Lables.storage_dir":               "Default storage location",
    "Lables.levenshtein":               "Levenshtein distance (default: 6):",
    "Lables.7zip":                      "7zip Location (default: auto):",
    "Lables.7zip_binary":               "7Zip binary (default: 7z.exe):",
    "Lables.use_labels":                "Use uTorrent lables:",
    "Lables.label_folders":             "Lable folders (separated with ;):",
    "Lables.debug":                     "Debug"
    }

def main(argv):
    opt, args = getopt.getopt(argv, "he:da:", ["name=", "label=", "path=", "init", "hook"])
    del args
    for o, a in opt:
        if o in ("--name"): #torrent file name
            name = a
        elif o in ("--label"):
            label = a
        elif o in ("--path"):
            path = a
        elif o in ("--hook"):
            hook2utorrent()
        elif o in ("--init"):
            c=configui.App(False)
            c.MainLoop()
            sys.exit()
                     
    try:
        label
    except NameError:
        label = None

    try:
        path
    except NameError:
        print "Path to package not defined. You can use --path flag to define it. Aborting."
        sys.exit()

    try:
        name
    except NameError:
        print "Name is not defined. You can use --name flag to define it. Aborting."
        sys.exit() 
                        
    if options['imdb_flag']:
        output_name = name_oracle(name)
   
    output_folder = -1
    if options['use_labels']:
        if label==None or label.strip()=='':
            print "Label not defined. Reverting to use_labels=0"
        else:
            lfolder = -1
            rgx = re.compile("^"+label+"\:",re.IGNORECASE|re.UNICODE)
            for lf in options['label_folders']:
                if rgx.match(lf):
                    lfolder = re.sub(label+'\:', '', lf)
                    
            if os.path.exists(lfolder):
                output_folder = os.path.join(lfolder, output_name);
            else:
                output_folder = os.path.join(options['storage_dir'], label, output_name);
    
    if output_folder == -1:
        output_folder = os.path.join(options['storage_dir'], output_name);
    
    sevenzip = '"{}" x "{}" -ryo"{}" '.format(options['full_sevenzip_path'], path, output_folder)
    print
    print sevenzip
    subprocess.call(sevenzip)
    copy(path, output_folder)
    if options['debug']:
        os.system("PAUSE")

def copy(src, dst):
    #ignore = shutil.ignore_patterns('*.rar', '*.7z', '*.zip', '*.r*', '*.0*', '*.gz', '*.tar.gz', '*.tar', '*.bz', '*.tar.bz')
    #print ignore
    my_re = re.compile(options['supported_formats'], re.IGNORECASE|re.UNICODE);
    ignore = ignore_regex(my_re)
    copytree(src, dst, ignore)
    
def ignore_regex(my_re):
    def my_ignore(dir_name, dir_list):
        return [l for l in dir_list if my_re.match(l)]
    return my_ignore

def copytree(src, dst, ignore=None):
    """ Replacement for shutil copytree  """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()
        
    if os.path.exists(dst) == False:
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname):
                copytree(srcname, dstname, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy2(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error, err:
            errors.extend(err.args[0])
        except EnvironmentError, why:
            errors.append((srcname, dstname, str(why)))
    try:
        copystat(src, dst)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise Error, errors


def split_name(name):
    return re.sub(r'\W+', ' ', name).split()

def strip_name(name):
    return re.sub(r'\W+', ' ', name)


def search_imdb(name):
    ia = imdb.IMDb()
    imdb_name = split_name(name);
    prev_word = ''
    i = 0

    matches = {}
    for word in imdb_name:
        prev_word = prev_word + " " + word
        prev_word = prev_word.strip()
        if options['debug']:
            print "Searching for {}".format(prev_word)
            
        s_result = ia.search_movie(prev_word)
                    
        if len(s_result)>0 or (len(prev_word)<=too_little_query and len(s_result)>=too_much_results):
            if options['debug']:
                print "Starting levenshteincmpr() with '{}' query vs list of {} elements".format(prev_word, len(s_result))
            matches[i] = levenshteincmpr(prev_word, s_result)
            if matches[i]==False:
                if options['debug']:
                    print "Failed to search for {}".format(prev_word)
        else:
            if options['debug']:
                print ".....query skipped"
        i = i+1
    
    if len(matches)==0:
        if options['debug']:
            print "Not able to search IMBD at this time. Possible internet connection fail or imdb.com unreachable. Aborting."
        return False
     
    best_lev_match = {'lev':9999999999, 'title':''};
    for key in matches:
        if best_lev_match['lev'] > matches[key]['lev']:
            best_lev_match = {'lev':matches[key]['lev'], 'title':matches[key]['title']};
        if best_lev_match['lev'] == matches[key]['lev']:
            if len(best_lev_match['title'])<matches[key]['title']:
                best_lev_match = {'lev':matches[key]['lev'], 'title':matches[key]['title']};
            
    if options['debug']:
        print best_lev_match
    
    if best_lev_match['lev'] < levenshtein:
        return best_lev_match['title']
    else:
        return False
   
def levenshteincmpr(string, list):
    if len(list)==0:
        return False;
    best_lev_match = 999999999;
    fixed_string = strip_name(str(string).lower()).strip()
    for item in list:
        if options['debug']:
            print ".....Literating through {}".format(item) 
        fixed_itemstring = strip_name(str(item).lower()).strip()  
        levdist = jellyfish.levenshtein_distance(fixed_itemstring, fixed_string)
        if options['debug']:
            print "..........file <{}> vs imdb <{}> gave {} levenshtein distance".format(fixed_string, fixed_itemstring, levdist)
        if best_lev_match > levdist:
            best_lev_match = levdist
            best_match = fixed_itemstring
            
    return {'lev':best_lev_match, 'title':best_match}
    
        
def name_oracle(name):           
    
    regex_episode = re.compile("(.*)S([0-9]+)E([0-9]+)(.*)",re.IGNORECASE|re.UNICODE)
    regex_serial = re.compile("(.*)S([0-9]+)(.*)",re.IGNORECASE|re.UNICODE)
    episode = regex_episode.match(name)
    serial = regex_serial.match(name)
    #is this en episode ?
    if episode: 
        g = regex_episode.search(name)
        series_name = g.groups()[0];
        series_name_imdb = search_imdb(series_name)
        season = g.groups()[1];
        episode = g.groups()[2];
        if series_name_imdb != False:
            folder = '{}\sason{}'.format(series_name_imdb, season)
            print
            print 'I think this is {} episode of {} season of "{}" show'.format(episode, season, series_name_imdb)
            print 'Using folder name {}'.format(folder)
            print
    #is this serial/boxset ?
    elif serial:
        g = regex_serial.search(name)
        series_name = g.groups()[0];
        series_name_imdb = search_imdb(series_name)
        season = g.groups()[1];
        if series_name_imdb != False:
            folder = '{}\sason{}'.format(series_name_imdb, season)
            print
            print 'I think this is boxet of "{}" show of {} season'.format(series_name_imdb, season)
            print 'Using folder name {}'.format(folder)
            print
    #default is movie
    else:
        series_name_imdb = search_imdb(name)
        if series_name_imdb != False:
            folder = series_name_imdb
            print
            print 'I think this is "{}" movie'.format(series_name_imdb)
            print
            
    if series_name_imdb == False: 
        series_name_imdb = name
        folder = series_name_imdb
        print
        print 'Unable to find suitable match on IMDB. Falling back to original name: {}'.format(series_name_imdb)       
        print
        
    return folder

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

def hook2utorrent():
    
    print "Attempting to configure uTorrent..."
    
    utd = os.path.join(os.environ['APPDATA'], 'uTorrent', 'settings.dat');
    if os.path.exists(utd)==False:
        print "Unable to load uTorrent settings.dat, please set 'Run Program' manually. Refer to readme.txt to find out how to do that."
        os.system("PAUSE")
        sys.exit()
    else:
        
        utorrent = -1
        while utorrent == -1:
            if ''.join(os.popen('TASKLIST').readlines()).find('uTorrent.exe') >= 0:
                print "uTorrent is running. Please close uTorrent and try again."
                print
                os.system('PAUSE')
            else:
                utorrent = 1
                
        f = open(utd, 'rb')
        l = f.read()
        f.close()
        ut_settings = bencode.bdecode(l)

        bin_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'autoextractor.exe')
        ut_settings['finish_cmd'] = '"{}" --name "%N" --path "%D" --label "%L"'.format(bin_path)
        ut_settings = bencode.bencode(ut_settings)
        f = open(utd, 'wb')
        f.write(ut_settings)
        f.close() 

if __name__ == "__main__":
    global levenshtein, too_much_results, too_little_query, options
    too_much_results = 50
    too_little_query = 3
    options = read_config()
    levenshtein = options['levenshtein']
    main(sys.argv[1:])