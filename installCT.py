import os,requests
from os.path import isfile, join
from os import listdir
import zipfile
import shutil
import sys
from zipfile import ZipFile

home_directory = os.path.expanduser("~")
download_folder = os.path.join(home_directory, "Downloads")
def download(url):
    try:
        get_response = requests.get(url, stream=True)
        file_name = url.split("/")[-1]
        
        home_directory = os.path.expanduser("~")
        
        download_folder = os.path.join(home_directory, "Downloads")
        os.makedirs(download_folder, exist_ok=True)

        save_path = os.path.join(download_folder, file_name)

        with open(save_path, 'wb') as f:
            for chunk in get_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("Download successful")
    except Exception as e:
        print("Failed to download:", e)
    

def installModules(path, finalPath):
    modules = os.listdir(path)
    if(len(modules) == 0):
        print("No modules found in the InstallModules folder, no changes were made")
    else:
        try:
            print("Found " + str(len(modules)) + " modules, moving modules into chattriggers modules folder")
            for module in modules:
                if str(module).__contains__(".zip"):
                    with zipfile.ZipFile(path + module, 'r') as zip_ref:
                        zip_ref.extractall(path)
                    os.remove(path+module)

            modules = os.listdir(path)
            for module in modules:
                os.rename(path+module, finalPath + str("/") + module)
                print("Successfully installed "+str(module))

            print("All modules installed successfully, run /ct load to enable them")
        except Exception as e: print(e)
    input("Enter any key to exit: ")

def remove(path):
    try:
        """ param <path> could either be relative or absolute. """
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)  # remove the file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains
        else:
            raise ValueError("file {} is not a file or dir.".format(path))
    except Exception as e: print(e)

def getDir():
    if getattr(sys, 'frozen', False):
        # If the script is running as a bundled executable
        return os.path.dirname(sys.executable)
    else:
        # If the script is running as a regular Python script
        return os.path.dirname(os.path.abspath(__file__))
    
localModulesPath = ""
localModulesPath += getDir()
localModulesPath += "\\InstallModules\\"
pathFinal = ""
path = ""
path += os.getenv('APPDATA')
path += "\.minecraft"
use = input('Would you like to use the default minecraft path for installations? (' + path + ') Enter "Y", else enter your own .minecraft path: ')
if(use.lower() == "y"):
    pathFinal = path
else:
    pathFinal = use

if not os.path.exists(pathFinal+"\config\ChatTriggers\modules"):
    ans = input("No Chat triggers installation found, Would you like to install ChatTriggers? (Y/N): ")
    if(ans.lower() == "y"):
        try:
            print("Checking config path")
            if not os.path.exists(pathFinal+"\config"):
                print("config path not found")
                os.makedirs(pathFinal+"\config")
                print("Created config path")
            else:
                print("Found Config path")
        except:
            print()
        
        try:
            print("Checking ChatTriggers path")
            if not os.path.exists(pathFinal+"\config\ChatTriggers"):
                print("ChatTriggers path not found")
                os.makedirs(pathFinal+"\config\ChatTriggers")
                print("Created ChatTriggers path")
            else:
                print("Found ChatTriggers path")
        except:
            print()
        
        try:
            print("Checking ChatTriggers modules path")
            if not os.path.exists(pathFinal+"\config\ChatTriggers\modules"):
                print("ChatTriggers modules path not found")
                os.makedirs(pathFinal+"\config\ChatTriggers\modules")
                print("Created ChatTriggers modules path")
            else:
                print("Found ChatTriggers modules path")
        except:
            print()

        try:
            print("Downloading ChatTriggers mod")
            download("http://cdn.discordapp.com/attachments/1072701996114645065/1135272380718133278/ctjs-2.2.0-1.8.9.jar")
            os.rename(download_folder+"\ctjs-2.2.0-1.8.9.jar", pathFinal+"/mods/ctjs-2.2.0-1.8.9.jar")
            print("ChatTriggers has been placed into your mods folder successfully")
            print(">>> Please restart your game to load chat triggers <<<")

            r = input("Would you like to install modules? Place the modules you want to install inside the 'InstallModules' folder, then enter (Y/N): ")
            if(r.lower() == "y"):
                installModules(localModulesPath, pathFinal+"\config\ChatTriggers\modules")
        except Exception as e: print(e)
    else:
        exit()
else:
    r = input("ChatTrigger found! Would you like to install modules? Place the modules you want to install inside the 'InstallModules' folder, then enter (Y/N): ")
    if(r.lower() == "y"):
        try:
            installModules(localModulesPath, pathFinal+"\config\ChatTriggers\modules")
        except Exception as e: print(e)
    else:
        exit()