# Estos son los Responders para Cortex Analyzer 

Los responders se encuentran en el directorio:
**/opt/Cortex-Analyzers/responders**

## Responder capMEUri
Este responder hace una consulta al servidor Master que cuenta con capME y descarga en pcap con los parametros que obtiene de la alerta.
Son necesarios los siguientes parametros:

- IP destino
- IP origen
- Puerto destino
- Puerto origen
- Tiempo de inicio

Dichos parametros deben estar en los observables y los nombres deben coincidir con los que se le dio en las configuraciones del responder.
Estos ultimos se pueden cambiar desde cortex en cualquier momento.

Para mas informacion ver:
-------------------------
Documentacion Cortex 

- https://github.com/TheHive-Project/CortexDocs
