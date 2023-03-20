from base64 import main
from zipfile import ZipFile

import requests
import bs4
import ctypes
import os
import shutil
import sys
import wget


def is_admin():  # https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

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

if len(FilePath) == 0:
    FileNames = os.listdir(FilePath)
    FileName = ''.join(FileNames)
    FileParts = FileName.split('_')
    CurrentVersion = FileParts[1]
else:
    CurrentVersion = '0.0.0'

MainURL = 'https://releases.hashicorp.com/terraform/'
DownloadLink = 'https://releases.hashicorp.com'
response = requests.get(MainURL)
soup = BeautifulSoup(response.text, 'html.parser')

Links = []
for Link in soup.find_all('a'):
    Links.append(Link.get('href'))

LinkLocation = 1
if CurrentVersion not in Links[LinkLocation] and "-" not in Links[LinkLocation]:
    LatestVersion = Links[LinkLocation].split('/')
    DownloadLink = ('https://releases.hashicorp.com' + Links[LinkLocation] + 'terraform_' + LatestVersion[2]
                    + '_windows_386.zip')
    DownloadName = 'terraform_' + LatestVersion[2] + '_windows_386'

    SavePath = r'C:\\Program Files\\Terraform\\Download'
    Version = LatestVersion[2]

    DownloadFile = os.path.join(SavePath, DownloadName + '.zip')
    ExeFile = os.path.join(SavePath, 'terraform.exe')

    if is_admin():
        for file in os.listdir(SavePath):
            shutil.move(os.path.join(SavePath, file), r'C:\\Program Files\\Terraform\\Archive')
        wget.download(DownloadLink, out=SavePath)
        with ZipFile(DownloadFile, 'r') as ZipObject:
            ZipObject.extractall(FilePath)
        os.rename(ExeFile, os.path.join(SavePath, 'terraform_' + Version + '.exe'))
        os.chdir(SavePath)

        shutil.move(os.path.join(SavePath, 'terraform_' + Version + '.exe'), r'C:\\Program Files\\Terraform')
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    print('Already on latest version.')

if __name__ == '__main__':
    main()