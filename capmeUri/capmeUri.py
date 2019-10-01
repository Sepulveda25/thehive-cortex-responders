#!/usr/bin/env python3
# encoding: utf-8
# Este responder se encarga de generar un link para hacer un consulta a capme le pasa los parametros que son obtenidos 
# desde los observables que son:
# IP destino
# IP origen
# Puerto destino
# Puerto origen
# Tiempo de inicio
# Tiempo de finalizacion

from cortexutils.responder import Responder
import requests
from datetime import datetime, timezone
import time
import dateutil.parser as dp
import pytz
import socket
import binascii
import json
import re

#Evita la certificacion ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class capmeUri(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.server_capme_ip = self.get_param('config.server_capme_ip', None, "IP missing")

    def run(self):
        Responder.run(self)

        #Se obtienen el titulo de la alerta del campo data.title
        title = self.get_param('data.title', None, 'title not found in observables')
    	#Se obtienen las IPs origen y destino del bloque data.artifacts
        artifacts = self.get_param('data.artifacts', None, 'artifacts not found in observables')
    	
    	
        source_ip = ''.join([a['data'] for a in artifacts if a.get('dataType') == 'source_ip' and 'data' in a])
        destination_ip = ''.join([a['data'] for a in artifacts if a.get('dataType') == 'destination_ip' and 'data' in a])
        source_port = ''.join([a['data'] for a in artifacts if a.get('dataType') == 'source_port' and 'data' in a])
        destination_port = ''.join([a['data'] for a in artifacts if a.get('dataType') == 'destination_port' and 'data' in a])
        timestamp = ''.join([a['data'] for a in artifacts if a.get('dataType') == 'timestamp' and 'data' in a])

      
        # Validacion de IP y Puerto
        if not chkIP(self,source_ip) and chkIP(self,destination_ip) and chkPort(self,source_port) and chkPort(self,destination_port):
            self.report({'message': 'Error en numero de ip o puerto'})
            exit(1)
             
        #Se convierte el tiempo del timestamp a segundos de unix
        timestamp = timestamp.split("Z")[0].split(".")[0]
        timestamp_datetime_object = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
        start_time = timestamp_datetime_object.timestamp() - 3600
        end_time = timestamp_datetime_object.timestamp() + 3600

        cameUrl = 'https://172.16.81.50/capme/?sip={sip}&dip={dip}&spt={spt}&dpt={dpt}&stime={stime}&etime={etime}&filename=squert'.format(
                sip=source_ip,
                dip=destination_ip,
                spt=source_port,
                dpt=destination_port, 
                stime=int(start_time), 
                etime=int(end_time)
                )
    	
        #se convierten las variables a ascii 
        source_ip_hex=source_ip.encode('utf-8').hex()
        destination_ip_hex=destination_ip.encode('utf-8').hex()
        source_port_hex= source_port.encode('utf-8').hex()
        destination_port_hex=destination_port.encode('utf-8').hex()
        maxtx='500000'.encode('utf-8').hex()
        sidsrc='event'.encode('utf-8').hex()        
        xscript='auto'.encode('utf-8').hex()
        #CONCATENAR VARIABLES
        urArgs = 'd={sip}-{spt}-{dip}-{dpt}-{st}-{et}-{maxtx}-{sidsrc}-{xscript}'.format(
                sip=source_ip_hex,
                spt=source_port_hex, 
                dip=destination_ip_hex,  
                dpt=destination_port_hex, 
                st=int(start_time), 
                et=int(end_time),
                maxtx=maxtx,
                sidsrc=sidsrc,
                xscript=xscript
                )
        callbackLink='https://172.16.81.50/capme/.inc/callback.php?{urArgs}'.format(urArgs=urArgs)
        
        
        #Usuario y pass para ingresar al sitio de securitionion
        ck = {'httpd_username': 'sonion', 'httpd_password': 'sonion'}
        session = requests.Session()
        #Se conecta a capme para generar el pcap y obtener el link para descargarlo
        r = session.post(callbackLink,data=ck, verify=False)
        result = r.text
        resultJSON=json.loads(result) 
        
        resultTX=''.join(resultJSON['tx'])#Si tx=0 es que hubo un error
        #Se busca el href 
        match = re.search(r'href=[\'"]?([^\'" >]+)', resultTX)
        pcapLink='https://172.16.81.50{href}'.format(href= match.group(1))
        path='/home/thehive/responder-output/{fileName}'.format(fileName=match.group(1).split("/")[3])
        #respuesta = session.post(callbackLink,data=ck, verify=False)
        r = session.post(pcapLink,data=ck, verify=False)
        with open(path, 'wb') as f:
            f.write(r.content)


        self.report({'message': path})
        r.close()
        session.close()
        # if r.status_code == 200 :
        # else:
        #     self.error('Failed to send message.')
        # self.report({'message': 'message sent'})
        
    def operations(self, raw):
        return [self.build_operation('AddTagToCase', tag='message sent')]

def chkIP(self,ip):
    try:
        socket.inet_aton(ip)
        #self.report({'message': ip})
        # legal
        return True
    except socket.error:
        # Not legal
        #self.report({'message': 'Ip no valida'})
        return False

def chkPort(self,port):  
   
    try:
        portInt = int(port)
        if 1 <= portInt <= 65535:
             #self.report({'message': 'Ok'})
             return True 
        else:
             #self.report({'message': 'numero no valido'})
             return False 
    except ValueError:
        #self.report({'message': 'hay simbolos'})
        return False 
    
        
if __name__ == '__main__':
    capmeUri().run()

