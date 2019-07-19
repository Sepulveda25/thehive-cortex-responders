#!/usr/bin/env python
# encoding: utf-8

from cortexutils.responder import Responder
import requests
import json

#web_hook_url = 'https://hooks.slack.com/services/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'

class slackNotificacion(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.slack_webhook = self.get_param('config.slack_webhook', None, "webhook missing")

    def run(self):
        Responder.run(self)
   
	#Se obtienen el titulo de la alerta del campo data.title
	title = self.get_param('data.title', None, 'title not found in observables')
	#Se obtienen las IPs origen y destino del bloque data.artifacts
	artifacts = self.get_param('data.artifacts', None, 'recipient address not found in observables')
	#ip_artifacts = [a['data'] for a in artifacts if a.get('dataType') == 'source_ip' or a.get('dataType') == 'destination_ip' and 'data' in a]
	#if ip_artifacts:
	#	ipOrigen = ip_artifacts.pop()
	#	ipDestino = ip_artifacts.pop()
	#else:
	#	self.error('recipient address not found in observables')
	
	source_ip = ''.join([a['data'] for a in artifacts if a.get('dataType') == 'source_ip' and 'data' in a])
	destination_ip = ''.join([a['data'] for a in artifacts if a.get('dataType') == 'destination_ip' and 'data' in a])
	source_port = ''.join([a['data'] for a in artifacts if a.get('dataType') == 'source_port' and 'data' in a])
	destination_port = ''.join([a['data'] for a in artifacts if a.get('dataType') == 'destination_port' and 'data' in a])
	
	#Se obtienen el nombre del host (sensor) que envia la alerta del campo data.source
	source = self.get_param('data.source', None, 'title not found in observables')	
	#Se obtienen el numero de categoria de la alerta del campo data.severity
	severity = self.get_param('data.severity', None, 'title not found in observables')		
	
	#Se concatenan los valores para enviar el mensaje
	msgText = "IP origen: %s \n Puerto origen: %s \n IP destino: %s \n Puerto destino: %s \n"%(source_ip,source_port,destination_ip,destination_port)
	#Con los campos anteriores se arma el mensaje para enviar a slack
	slack_msg =	{   
			    "username": "Alerta the hive",
			    "attachments": [
				{
				    "color": "#bc0909",
				    "title": title,
				    "text": msgText,
				    "mrkdwn_in": [
					"text",
					"pretext"
				    ]
				}
			    ]
			}


        r = requests.post(self.slack_webhook,data=json.dumps(slack_msg))
        if r.status_code == 200 :
            self.report({'message': 'message sent'})
        else:
            self.error('Failed to send message.')
       # self.report({'message': 'message sent'})

    def operations(self, raw):
        return [self.build_operation('AddTagToCase', tag='message sent')]

if __name__ == '__main__':
    slackNotificacion().run()

