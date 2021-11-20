import bs4
from selenium import webdriver
import os
from selenium import webdriver
import time, requests
from urllib.request import urlopen
import json
import pyodbc
import Dao.conexion as conn
import Helpers.CreateFolder as createFolder
import Helpers.DownloadImages as download
import cv2
import numpy as np
import imutils
from PIL import Image
#variable gloabal
Datos = 'n'
x1, y1 = 190, 80
x2, y2 = 450, 398

def captura():
    count = 0
    while True:
        ret,frame = cap.read()
        if ret == False:  break
        imAux = frame.copy()
        cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
        objeto = imAux[y1:y2,x1:x2]
        objeto = imutils.resize(objeto, width=38)
        k = cv2.waitKey(1)
        if k == ord('s'):
            cv2.imwrite(Datos+'/objeto_{}.jpg'.format(count),objeto)
            print('Imagen almacenada: ', 'objeto_{}.jpg'.format(count))
            count = count + 1
            if k == 27: 
                break
        cv2.imshow('frame',frame)
        cv2.imshow('objeto',objeto)
    cap.release()
    cv2.destroyAllWindows()

def detectar():
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    majinBooClassif = cv2.CascadeClassifier('cascade.xml')
    while True:
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        toy = majinBooClassif.detectMultiScale(gray,scaleFactor = 5,
	    minNeighbors = 91,minSize=(70,78))
        for (x,y,w,h) in toy:
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame,'Majin Boo',(x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)    
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) == 27:
            break
        cap.release()
        cv2.destroyAllWindows()

def download_image(url, folder_name, num):
    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(folder_name, str(num)+".jpg"), 'wb') as file:
            file.write(reponse.content)
def openBrowser(search_query,driver):
    search_URL = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
    driver.get(search_URL)

def getInformationImages(folder_name,driver):
    #Scrolling all the way up
    driver.execute_script("window.scrollTo(0, 0);")
    page_html = driver.page_source
    pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
    containers = pageSoup.findAll('div', {'class':"isv-r PNCib MSM1fd BUooTd"} )
    print(len(containers))
    len_containers = len(containers)
    for i in range(1, len_containers+1):
        if i % 25 == 0:
            continue

        xPath = """//*[@id="islrg"]/div[1]/div[%s]"""%(i)
        previewImageXPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)
        previewImageElement = driver.find_element_by_xpath(previewImageXPath)
        previewImageURL = previewImageElement.get_attribute("src")
        driver.find_element_by_xpath(xPath).click()
        timeStarted = time.time()
        while True:

            imageElement = driver.find_element_by_xpath("""//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")
            imageURL= imageElement.get_attribute('src')

            if imageURL != previewImageURL:
                break

            else:
                currentTime = time.time()

                if currentTime - timeStarted > 10:
                    print("Timeout! Will download a lower resolution image and move onto the next one")
                    break
        try:
            downimages =  download.DownloadImg()
            #downimages.download_images(imageURL, folder_name, i)
            download_image(imageURL, folder_name, i)
            print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
        except:
            print("Couldn't download an image %s, continuing downloading the next one"%(i))



def insertData():
    c1 = conn.Conexion()
    try:
        objeto = c1.connect() 
        with objeto.cursor() as cursor:
            consulta = "INSERT INTO peliculas(titulo, anio) VALUES (?, ?);"
            # Podemos llamar muchas veces a .execute con datos distintos
            cursor.execute(consulta, ("Volver al futuro 1", 1985))     
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

        
def get_Sinonimos(search_query):
    search_sinonimo = f"http://sesat.fdi.ucm.es:8080/servicios/rest/sinonimos/json/{search_query}"
    response = urlopen(search_sinonimo)
    data_json = json.loads(response.read())
    return data_json

def menu():
    try:
        opc = int(input("1.Buscar Imagenes. \n2.Detectar Objetos. \n3.salir"))
        return opc
    except Exception as e:
      print("Ingresa una opcion valida", e)
    
#words = get_Sinonimos('andar')
#items = search_google('perro')
def main():
    opc = menu()
    while(opc!=3):
        if opc==1:
            thing = input("¿Que deseas Buscar?")
            driver=webdriver.Chrome(executable_path=r'c:/Selenium/chromedriver.exe')
            insertData()
            #objeto Create Folder
            cFolder = createFolder.CreateFolder()
            name_folder = cFolder.createFolder(thing)
           
            openBrowser(thing,driver)
            getInformationImages(name_folder,driver)
            opc = menu()
        elif opc==2:
            detectar()
            opc = menu()
        elif opc==3:
            print("saliendo...")
        else:
             print("Ingresa una opcion valida")
             opc = menu()
main()