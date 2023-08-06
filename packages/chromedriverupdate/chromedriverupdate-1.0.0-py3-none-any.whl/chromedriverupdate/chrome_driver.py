import os
import platform
from sys import platform as sys_platform
import zipfile
import requests


class ChromeDriverUpdate:

    def __init__(self, errMsg, output_dir):
        self.errMsg = errMsg
        self.outputDir = output_dir

    def download_url(self, url, save_path, chunk_size=128):
        r = requests.get(url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)

    def update(self):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
        }
        majorVersion = self.errMsg.split(
            'Current browser version is ')[1].split(' ')[0][:3]
        response = requests.get(
            f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{majorVersion}',
            headers=headers,
        )
        version = response.text

        systemPlatform = ''
        if sys_platform == "linux" or sys_platform == "linux2":
            systemPlatform = 'linux64'
        elif sys_platform == "darwin":
            if platform.processor() == 'arm':
                systemPlatform = 'mac64_m1'
            else:
                systemPlatform = 'mac64'
        elif sys_platform == "win32":
            systemPlatform = 'win32'

        zipPath = os.path.join(self.outputDir, '_tmpchromedriver.zip')
        self.download_url(
            f'https://chromedriver.storage.googleapis.com/{version}/chromedriver_{systemPlatform}.zip',
            zipPath,
        )
        with zipfile.ZipFile(zipPath, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(zipPath))
        os.remove(zipPath)


if __name__ == '__main__':
    msg = "session not created: This version of ChromeDriver only supports Chrome version 105\nCurrent browser version is 107.0.5304.88 with binary path C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    chrome = ChromeDriverUpdate(msg, os.path.dirname(__file__))
    chrome.update()
