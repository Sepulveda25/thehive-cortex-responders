#!/usr/bin/env python
# encoding: utf-8

from cortexutils.responder import Responder
import requests
#import json
import datetime
import time
import dateutil.parser as dp
import pytz

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
        #Se convierte el tiempo del timestamp a segundos de unix
    	parsed_t = dp.parse(timestamp)
    	
    	stimeStr = parsed_t.strftime('%s')
    	
        stimeInt = int(stimeStr)-10800 #se restan 3 horas para que capme lo recozca como hora UTC 
         
        etimeInt = stimeInt +7200
        etimeStr = str(etimeInt)
    	#Se concatenan los valores para enviar el mensaje
        linkCapme = "https://172.16.81.50/capme/?sip=%s&dip=%s&spt=%s&dpt=%s&stime=%d&etime=%s&filename=squert"%(source_ip,destination_ip,source_port,destination_port,stimeInt,etimeStr)  					
        # if r.status_code == 200 :
        self.report({'message': linkCapme })
        # else:
        #     self.error('Failed to send message.')
        # self.report({'message': 'message sent'})

    def operations(self, raw):
        return [self.build_operation('AddTagToCase', tag='message sent')]

if __name__ == '__main__':
    capmeUri().run()

