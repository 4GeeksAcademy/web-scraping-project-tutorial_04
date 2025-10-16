"""Se se realiza práctica de web scrapping a la pagina web https://books.toscrape.com/
   habilitada para dicha práctica
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd


URL = "https://books.toscrape.com/"
header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}

#Hacer la petición a la url indicada
response = requests.get(URL, headers = header, timeout = 3)

#comprobar la conexión de la petición 200 ok y 400, 500 bad
#print(response.status_code)

#imprimir la 500 primeras lineas para comprobar
#print(response.text[:500])
#crear el objeto `Beautifulsoup`
soup = BeautifulSoup(response.content, "html.parser")

# Examinando el documento html encuentro dentro de un div, 
# un único <ul class='nav nav-list'> con <ul> anidado`y dentro
# una etiqueta <a>`que contiene las categorias que busco
# usar .find() para encontrar una unica etiqueta <ul>, el bloque principal de las categorias
nav_list = soup.find('ul', class_='nav nav-list')

#dentro encuentro 'ul' anidado
sub_list = nav_list.find('ul')

#y por último  localizo todas las <a> dentro del último <ul>
categoria = sub_list.find_all('a')

#lista final con las categorías, libros y precios
libreria = []

#recorro todas las categorias y extraigo el texto
for i in categoria:
    NOMBRE_CATEGORIA= str.strip(i.get_text())
    #completo la url relativa para cada página en 'categoria'
    url_categoria = URL + i['href']
    #peticiones a las primeras págians de las categorias
    response = requests.get(url_categoria, headers=header, timeout=2)
    soup = BeautifulSoup(response.content, "html.parser")
    #extaer libros y precios
    #<article class="product_pod">
    libros = soup.find_all('article', class_='product_pod')
    for libro in libros:
        #dentro de 'article', class_='product_pod'busco etiqueta h3-->a
        #para obtener el titulo del libro
        titulo = libro.h3.a['title']
        PRICE = str.strip(libro.find('p', class_='price_color').get_text())#strip=tTrue
        libreria.append({"Categoria":NOMBRE_CATEGORIA, "Título": titulo, "Precio": PRICE[1:]})

#libreria
df = pd.DataFrame(libreria)
df.to_csv("libreria.csv")
print(df)
