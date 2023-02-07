#librerias
import json
import requests
import urllib3
import xml.etree.cElementTree as xml
import os
import errno

from decimal import Decimal
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

#funciones
def bancocentralparaguay():
    try:
        soup = BeautifulSoup(requests.get("https://www.bcp.gov.py/webapps/web/cotizacion/referencial-fluctuante",timeout=10,headers={"user-agent": "Mozilla/5.0"},verify=False,).text,"html.parser",)
        compra_array = soup.find(class_="table table-striped table-bordered table-condensed").select("tr > td:nth-of-type(2)")
        venta_array = soup.find(class_="table table-striped table-bordered table-condensed").select("tr > td:nth-of-type(3)")
        
        #Se toma la cotizacion promedio del día anterior.
        compra = compra_array[0].get_text().replace(".", "").replace(",", ".")
        venta = venta_array[0].get_text().replace(".", "").replace(",", ".")
            
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta)

def superintendenciadebancaperu():
    try:
        soup = BeautifulSoup(requests.get("https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx",timeout=10,headers={"user-agent": "Mozilla/5.0"},verify=False,).text,"html.parser",)
        compra_array = soup.find(id="ctl00_cphContent_rgTipoCambio_ctl00__0").select("tr > td:nth-of-type(2)")
        venta_array = soup.find(id="ctl00_cphContent_rgTipoCambio_ctl00__0").select("tr > td:nth-of-type(3)")
        #Dolar de N.A.
        compra = compra_array[0].get_text().replace(".", "").replace(",", ".")
        venta = venta_array[0].get_text().replace(".", "").replace(",", ".")
        
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0
        
    return Decimal(compra), Decimal(venta)

def GetCotizacionesAndGenerateXML():
    #Banco Central Paraguay
    bcParaguayCompra, bcParaguayVenta = bancocentralparaguay()
    #SuperIntendencia de Banca Perú
    sbPeruCompra, sbPeruVenta = superintendenciadebancaperu()
    
    nodoPrincipal = xml.Element('Cotizaciones')
    bcParaguay = xml.SubElement(nodoPrincipal, 'BancoCentralParaguay')
    xml.SubElement(bcParaguay, 'Compra').text = str(bcParaguayCompra)
    xml.SubElement(bcParaguay, 'Venta').text = str(bcParaguayVenta)
    sbPeru = xml.SubElement(nodoPrincipal, 'SuperIntendenciaBancaPeru')
    xml.SubElement(sbPeru, 'Compra').text = str(sbPeruCompra)
    xml.SubElement(sbPeru, 'Venta').text = str(sbPeruVenta)
    documentoxml = xml.ElementTree(nodoPrincipal)

    try:
        os.mkdir('data')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    documentoxml.write('data/cotizacionActual.xml')
    # #historico
    # str_path = 'Archivos Cotizaciones/cotizacionHistorica-'+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'.xml'
    # str_path = Path(str_path)
    # documentoxml.write(str_path)
    
    
    
#Ejecución principal
GetCotizacionesAndGenerateXML()