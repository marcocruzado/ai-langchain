#realizaremos un web scraping a la url https://clubelcomercio.pe/beneficio/buscar/tipo/gastronomia/distrito/150122
import requests
from bs4 import BeautifulSoup
import csv

def out_blank_spaces(text):
    return text.replace('\n', '').replace('\t', '').replace('\r', '').strip()

def split_pipe(text):
    if '|' in text:
        split = text.split('|')
        #retornar el ultimo elemento y eliminar espacios en blanco
        horario = split[-1].strip()
        #y la direccion va a ser el resto
        direccion = '|'.join(split[:-1])
        return direccion, horario
    else:
        direccion = text
        horario = ''
        return direccion, horario





all_promociones = [
    'educacion',
    'entretenimiento',
    'gastronomia',
    'productos-servicios',
    'hogar',
    'mascotas',
    'moda-belleza',
    'turismo',
]

promociones = []

def web_scraping():
    # URL a la que se realizará el web scraping
    urlbase = 'https://clubelcomercio.pe/catalogo-virtual/tipo/'
    
    for promocion in all_promociones:
        # Realizar la solicitud GET a la página web
        response = requests.get(urlbase + promocion)
        html_content = response.text
        # Crear el objeto BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(html_content, "html.parser")
        # Extraer información relevante de la página
        productos = soup.find_all("div", class_="item_colc")
        
        # Recorrer las ofertas y extraer los detalles
        for producto in productos:
            descuento_element = producto.find('div', class_='descuento')
            descuento = out_blank_spaces(descuento_element.text) if descuento_element else '' 
            descuento_valor = out_blank_spaces(producto.find('h3').text)
            descuento_descripcion = out_blank_spaces(producto.find('div', class_='ofert_cs').find('p').text)
            url_establecimiento = out_blank_spaces(producto.find('a')['href'])
            nombre = out_blank_spaces(producto.find('h2').text)
            facebook = out_blank_spaces(producto.find('a', class_='share-link')['href'])
            categoria = out_blank_spaces(producto.find('div', class_='ofert_cs').find('h3').text)
            # Agregar los datos a la lista
            promociones.append([descuento, descuento_valor, descuento_descripcion, url_establecimiento, nombre, facebook, categoria])

        for promocion in promociones:
            url_establecimiento = promocion[3]
            response = requests.get(url_establecimiento)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            
            descripcion = out_blank_spaces(soup.find('p', class_='descripcion').text)
            ubic_beneficio =soup.find('div', class_='ubic_benf').find("div",class_="clearfix").find_all("div", class_="cont_ubic")
            #Cal. Enrique Palacios 140, Miraflores | Jr. El Polo 284 C.C Monterrico | L-S: 12pm-9:30pm y D: 12pm-6pm
            direccion_full = out_blank_spaces(ubic_beneficio[0].find('p').text)
            direccion, horario = split_pipe(direccion_full)
            vigencia = out_blank_spaces(ubic_beneficio[1].find('p').text)
            condicion = out_blank_spaces(ubic_beneficio[2].find('p').text)
            lugar = soup.find('div', class_='lugar2').find("div",class_="clearfix").find_all("div", class_="cont_ubic")
            telefono = out_blank_spaces(lugar[0].find('h3').text)
            correo = out_blank_spaces(lugar[1].find('h3').text)
            web = out_blank_spaces(lugar[2].find('h3').text)
            terminos = out_blank_spaces(soup.find('div', class_='terminos').find("div",class_="clearfix").find('p').text)

            promociones[promociones.index(promocion)].append(descripcion)
            promociones[promociones.index(promocion)].append(direccion)
            promociones[promociones.index(promocion)].append(horario)
            promociones[promociones.index(promocion)].append(vigencia)
            promociones[promociones.index(promocion)].append(condicion)
            promociones[promociones.index(promocion)].append(telefono)
            promociones[promociones.index(promocion)].append(correo)
            promociones[promociones.index(promocion)].append(web)
            promociones[promociones.index(promocion)].append(terminos)
    return promociones

promociones = web_scraping()

print(promociones)


# Guardar los datos en un archivo CSV
filename = './data/datos_club_suscriptores.csv'
with open(filename, 'w', newline='', encoding='utf-8') as file:
    #escribir el archivo csv y adicionarle como primera columna un id autoincrementable
    writer = csv.writer(file)
    writer.writerow(["descuento", "descuento_valor", "descuento_descripcion", "url_establecimiento", "nombre", "facebook", "categoria", "descripcion", "direccion", "horario","vigencia", "condicion", "telefono", "correo", "web", "terminos"])
    writer.writerows(promociones)