# For Windows OS

import requests, os, ctypes, sys, wget, shutil
from bs4 import BeautifulSoup
from zipfile import ZipFile

# Function for running commands with elevated permissions, for copying files into Program Files
# https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
# Using the above function to check for, and create the folders relevant to this script
if is_admin():
    os.chdir(r'C:\\Program Files\\')
    if not os.path.exists("Terraform"):
        os.mkdir("Terraform")
    os.chdir(r'C:\\Program Files\\Terraform')
    if not os.path.exists("Download"):
        os.mkdir("Download")
    if not os.path.exists("Archive"):
        os.mkdir("Archive")
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

FilePath = r'C:\\Program Files\\Terraform\\Download'

# Take the version number from the existing file in the Downloads folder
# If no files are present, set the Current Version to 0.0.0
if len(FilePath) != 0:
    FileNames = os.listdir(FilePath)
    FileName = ''.join(FileNames)
    FileParts = FileName.split('_')
    CurrentVersion = FileParts[1]
else:
    CurrentVersion = '0.0.0'

# Gather a list of all the links on the Terraform versions page
MainURL = 'https://releases.hashicorp.com/terraform/'
DownloadLink = 'https://releases.hashicorp.com'
response = requests.get(MainURL)
soup = BeautifulSoup(response.text, 'html.parser')

Links = []
for Link in soup.find_all('a'):
    Links.append(Link.get('href'))

# Check the second link, if the current version on the host does not match the version number in the link, grab the
# download file based on that. Also checks for hyphens, which look like could be determinant for if a version is
# beta/alpha or not.
LinkLocation = 1
if CurrentVersion not in Links[LinkLocation] and "-" not in Links[LinkLocation]:
    LatestVersion = Links[LinkLocation].split('/')
    # creates a download link based on the available information.
    DownloadLink = ('https://releases.hashicorp.com' + Links[LinkLocation] + 'terraform_' + LatestVersion[2]
                    + '_windows_386.zip')
    DownloadName = 'terraform_' + LatestVersion[2] + '_windows_386'

    RootPath = r'C:\\Program Files\\Terraform'
    SavePath = r'C:\\Program Files\\Terraform\\Download'
    Version = LatestVersion[2]

    DownloadFile = os.path.join(SavePath, DownloadName + '.zip')
    ExeFile = os.path.join(SavePath, 'terraform.exe')

    # Running with elevated permissions to first download the file to Program Files\Terraform\Downloads
    # Then unzip the zip file, and then move it down a directory.
    # For challenge 3, if there is a new version, but already a Terraform.exe in Program Files\Terraform, rename it with the version number,
    # and move it to the Archive folder.
    if is_admin():
        for file in os.listdir(SavePath):
            shutil.move(os.path.join(SavePath, file), r'C:\\Program Files\\Terraform\\Archive')
        wget.download(DownloadLink, out=SavePath)
        with ZipFile(DownloadFile, 'r') as ZipObject:
            ZipObject.extractall(FilePath)

        os.chdir(SavePath)
        if os.path.isfile(r'C:\\Program Files\\Terraform\\terraform.exe'):
            os.rename(os.path.join(RootPath, 'terraform.exe'), os.path.join(RootPath, 'terraform_' + CurrentVersion + '.exe'))
            shutil.move(os.path.join(RootPath, 'terraform_' + CurrentVersion + '.exe'), r'C:\\Program Files\\Terraform\\Archive')
        shutil.move(os.path.join(SavePath, 'terraform.exe'), r'C:\\Program Files\\Terraform')
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    print('Already on latest version.')
    
# Things to Improve
# Better method of checking version. Running terraform -version in CMD returns version, maybe see if that value can be pulled.
# Better checking of versioning on site, logic is shaky currently and relies on the newest version being at the top of the page.
#       Set up some loop to check previous versions. Like if the latest version (one at the top) is beta, go to next link, if version number is greater than installed
#       version number, download that file.
# Not entirely positive whether backing up the old .exe also backs up the Terraform binary, need to investigate further.
# This works on my personal computer, but not work . Unsure if this is due to more strict restrictions on the work computer. Need to investigate.
