import configparser, re, os, requests, zipfile

C_LATEST_VERSION_RE = re.compile(r'The latest version of this addon is <b class="VIP">([0-9]+.[0-9]+)</b>')
R_LATEST_VERSION_RE = re.compile(r'The current version of ElvUI is <b class="Premium">([0-9]+.[0-9]+)</b>')
LOCAL_VERSION_RE = re.compile('[0-9]+\\.[0-9]+')
C_ELVUI = requests.get('https://www.tukui.org/classic-addons.php?id=2#extras')
R_ELVUI = requests.get('https://www.tukui.org/download.php?ui=elvui#version')


def c_installed_version(wowdir):
    # Set path to ElvUI.toc
    toc_file = wowdir + '\\_classic_\\interface\\addons\\ElvUI\\ElvUI.toc'
    
    # Read toc file 
    try:
        toc = open(toc_file, 'r')
        toc_lines = toc.readlines()
        toc.close()
    except FileNotFoundError:
        return 'Not Installed'
        
    # Parse version string from toc file
    version = LOCAL_VERSION_RE.search(toc_lines[2])
    return version.group()

def r_installed_version(wowdir):
    # Set path to ElvUI.toc
    toc_file = wowdir + '\\_retail_\\interface\\addons\\ElvUI\\ElvUI.toc'
    
    # Read toc file 
    try:
        toc = open(toc_file, 'r')
        toc_lines = toc.readlines()
        toc.close()
    except FileNotFoundError:
        return 'Not Installed'
        
    # Parse version string from toc file
    version = LOCAL_VERSION_RE.search(toc_lines[2])
    return version.group()    
    
def c_latest_version():
    # Parse version string from webpage
    text = C_ELVUI.text
    
    # Parse version
    return C_LATEST_VERSION_RE.search(text).group(1)

def r_latest_version():
    # Parse version string from webpage
    text = R_ELVUI.text
    
    # Parse version
    return R_LATEST_VERSION_RE.search(text).group(1)
    
def c_update(wowdir):
    # Download
    local_filename = 'c_elvui.zip'
    req = requests.get('https://www.tukui.org/classic-addons.php?download=2', stream=True)
    
    with open(local_filename, 'wb') as download:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                download.write(chunk)
                
    # Unzip
    c_elvui_zip = zipfile.ZipFile(local_filename, 'r')

    # Extract to addons folder
    c_elvui_zip.extractall(path=wowdir + '\\_classic_\\interface\\addons\\')

    # Cleanup
    c_elvui_zip.close()
    os.remove(local_filename)
    
def r_update(wowdir, r_latest):
    # Download
    local_filename = 'r_elvui.zip'
    req = requests.get('https://www.tukui.org/downloads/elvui-' + r_latest + '.zip', stream=True)
    
    with open(local_filename, 'wb') as download:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                download.write(chunk)
                
    # Unzip
    r_elvui_zip = zipfile.ZipFile(local_filename, 'r')

    # Extract to addons folder
    r_elvui_zip.extractall(path=wowdir + '\\_retail_\\interface\\addons\\')

    # Cleanup
    r_elvui_zip.close()
    os.remove(local_filename)

def main():
    # Read config-file
    try:
        config = configparser.ConfigParser()
        config.read('settings.ini')
        
    except FileNotFoundError:
        invalid = True
    
    # Check WoW directory
    wowdir = config['SETTINGS']['game directory']
    
    # Update ElvUI for Classic WoW
    if config['ELVUI']['classic'] == 'True':
        # Get installed version
        c_installed = c_installed_version(wowdir)
        print('Installed Classic Version: ' + c_installed)
        
        # Get latest version
        c_latest = c_latest_version()
        print('Latest Classic Version: ' + c_latest)
        if c_installed != c_latest:
            print('Updating...')
            c_update(wowdir)
            print('Update Complete')
    else:
        print('ElvUI for Classic WoW will not be updated')

    # Update ElvUI for Retail WoW
    if config['ELVUI']['retail'] == 'True':
        # Get installed version
        r_installed = r_installed_version(wowdir)
        print('Installed Retail Version: ' + r_installed)
        
        # Get latest version
        r_latest = r_latest_version()
        print('Latest Retail Version: ' + r_latest)
        if r_installed != r_latest:
            print('Updating...')
            r_update(wowdir, r_latest)
            print('Update Complete')
    else:
        print('ElvUI for Retail WoW will not be updated')
   

   
if __name__ == '__main__':
    main()
