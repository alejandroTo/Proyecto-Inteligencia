import bs4
from selenium import webdriver
from selenium import webdriver
import time, requests
from urllib.request import urlopen
import json
import pyodbc
import Dao.conexion as conn
import Helpers.CreateFolder as createFolder
import Helpers.DownloadImages as downloadImages
class DownloadImg:
    def download_images(self, url, folder_name, num):
        # write image to file
        reponse = requests.get(url)
        if reponse.status_code==200:
            with open(os.path.join(folder_name, str(num)+".jpg"), 'wb') as file:
                file.write(reponse.content)