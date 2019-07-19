#!/usr/bin/env python
# encoding: utf-8

from cortexutils.responder import Responder
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import json
import urllib2
from netaddr import IPNetwork, IPAddress


class MailExcel(Responder):
	def __init__(self):
		Responder.__init__(self)
		self.smtp_host = self.get_param('config.smtp_host', 'medusa.psi.unc.edu.ar')
		self.smtp_port = self.get_param('config.smtp_port', '25')
		self.mail_from = self.get_param('config.from', None, 'Missing sender email address')
#		df = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
#                   '1vWkrGHdbDv2KLJkkBrQ4WleXwwS8fNhAKvHxkifvyo4' +
#                   '/edit#gid=0&format=csv',
#                   # Set first column as rownames in data frame
#                   index_col=0,
#                   # Parse column values to datetime
#                   parse_dates=['Quradate']
#                  )

	def run(self):
		Responder.run(self)

		title = self.get_param('data.title', None, 'title is missing')
		title = title.encode('utf-8')

		description = self.get_param('data.description', None, 'description is missing')
		description = description.encode('utf-8')

#		mail_to = 'unc.csirt@gmail.com'
		artifacts = self.get_param('data.artifacts', None, 'recipient address not found in observables')
		ip_source = [a['data'] for a in artifacts if a.get('dataType') == 'source_ip' and 'data' in a]
		ip_destination = [a['data'] for a in artifacts if a.get('dataType') == 'destination_ip' and 'data' in a]
		port_source = [a['data'] for a in artifacts if a.get('dataType') == 'source_port' and 'data' in a]
		port_destination = [a['data'] for a in artifacts if a.get('dataType') == 'destination_port' and 'data' in a]
		ipOrigen = ip_source.pop()
		ipDestino = ip_destination.pop()
		puertoOrigen = port_source.pop()
		puertoDestino = port_destination.pop()
		octetos = ipDestino.split('.')
		dosOctetos = octetos[0] + "." + octetos[1]
		tresOctetos = dosOctetos + "." + octetos[2]

		url = "http://activos-api.psi.unc.edu.ar/assets?elasticSearch=" + tresOctetos
		response = urllib2.urlopen(url)
		data = response.read()
		values = json.loads(data)
		dictRedes = {}

		for dato in values:
			if IPAddress(ipDestino) in IPNetwork(dato['name']):
				dictRedes.update( {dato['name'] : dato['Grupo_de_contacto']} )

		if not dictRedes:
			url = "http://activos-api.psi.unc.edu.ar/assets?elasticSearch=" + dosOctetos
			response = urllib2.urlopen(url)
			data = response.read()
			values = json.loads(data)
			for dato in values:
				if IPAddress(ipDestino) in IPNetwork(dato['name']):
					dictRedes.update( {dato['name'] : dato['Grupo_de_contacto']} )
		
		maskCandidata = 0
		mailA = ''
		for red, mail in dictRedes.items():
			ip, mascara = red.split('/')
			if int(mascara) > maskCandidata:
				maskCandidata = mascara
				mailA = mail.split(',')

		mail_to = mailA[1]

		msg = MIMEMultipart()
		msg['Subject'] = title
		msg['From'] = self.mail_from
		msg['To'] = mail_to
		msg.attach(MIMEText("Ip de origen: ", 'plain'))
		msg.attach(MIMEText(ipOrigen, 'plain'))
		msg.attach(MIMEText("\n", 'plain'))
		msg.attach(MIMEText("Ip de destino: ", 'plain'))
		msg.attach(MIMEText(ipDestino, 'plain'))
		msg.attach(MIMEText("\n", 'plain'))
#		msg.attach(MIMEText("Puerto de origen: ", 'plain'))	
#		msg.attach(MIMEText(puertoOrigen, 'plain'))
#		msg.attach(MIMEText("\n", 'plain'))
#		msg.attach(MIMEText("Puerto de destino: ", 'plain'))
#		msg.attach(MIMEText(puertoDestino, 'plain'))
#		msg.attach(MIMEText("\n", 'plain'))
		msg.attach(MIMEText(description, 'plain'))

		s = smtplib.SMTP(self.smtp_host, self.smtp_port)
		s.sendmail(self.mail_from, [mail_to], msg.as_string())
		s.quit()
		self.report({'message': dictRedes})

if __name__ == '__main__':
	MailExcel().run()
