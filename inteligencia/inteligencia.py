import bs4
from selenium import webdriver
import os
from selenium import webdriver
import time, requests
from urllib.request import urlopen
import json
import pyodbc
import Dao.conexion as conn
from google_images_download import google_images_download  

#variables Globales
#driver=webdriver.Chrome(executable_path=r'c:/Selenium/chromedriver.exe')


def createFolder(name):
    folder_name = name
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
    return folder_name

def download_image(url, folder_name, num):
    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(folder_name, str(num)+".jpg"), 'wb') as file:
            file.write(reponse.content)



def openBrowser(search_query,driver):
    #search_URL = "https://www.google.com/search?q=car+parts&source=lnms&tbsearch_querym=isch"
    #search_URL = f"http://sesat.fdi.ucm.es:8080/servicios/rest/sinonimos/json/{search_query}"
    search_URL = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
    #images_url = []
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

  
    
    

#words = get_Sinonimos('andar')
#items = search_google('perro')
def main():
    thing = input("¿Que deseas Buscar?")
    driver=webdriver.Chrome(executable_path=r'c:/Selenium/chromedriver.exe')
    insertData()
    name_folder = createFolder(thing)
    openBrowser(thing,driver)
    getInformationImages(name_folder,driver)
main()