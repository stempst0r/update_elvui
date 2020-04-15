from lxml import html
import configparser, re, os, requests, zipfile

LATEST_VERSION_RE = re.compile(r'The latest version of this addon is <b class="VIP">([0-9]+.[0-9]+)</b>')
LOCAL_VERSION_RE = re.compile('[0-9]+\\.[0-9]+')
ELVUI = requests.get('https://www.tukui.org/classic-addons.php?id=2#extras')


def installed_version(wowdir):
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
    
    
def latest_version():
    # Parse version string from webpage
    text = ELVUI.text

    # Parse version
    return LATEST_VERSION_RE.search(text).group(1)
    
def update(wowdir):
    # Download
    local_filename = 'elvui.zip'
    req = requests.get('https://www.tukui.org/classic-addons.php?download=2', stream=True)
    
    with open(local_filename, 'wb') as download:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                download.write(chunk)
                
    # Unzip
    elvui_zip = zipfile.ZipFile(local_filename, 'r')

    # Extract to addons folder
    elvui_zip.extractall(path=wowdir + '\\_classic_\\interface\\addons\\')

    # Cleanup
    elvui_zip.close()
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
       
    # Get installed version
    installed = installed_version(wowdir)
    print('Installed Version: ' + installed)
    
    # Get latest version
    latest = latest_version()
    print('Latest Version: ' + latest)
    
    
    if installed != latest:
        print('Updating...')
        update(wowdir)
        print('Update Complete')
    
if __name__ == '__main__':
    main()