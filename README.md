# Responders para Cortex Analyzer 

[Volver a documento raiz](https://gitlab.unc.edu.ar/csirt/csirt-docs/tree/master#csirt-docs)

## Directorio de los responders
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

Dichos parametros deben estar en los observables y `los nombres deben coincidir con los que se le dio en las configuraciones del responder`.
Estos ultimos se pueden cambiar desde cortex en cualquier momento.

### Path para el directorio de los pcap
El directorio para almacenar los pcap se debe crear con permisos para el usuario cortex, de esta manera el responder lo va a poder utilizar. 

## Responder excelMails
Este responder envia un correo electronico a la/las persona/s responsables de la red a la cual pertenece la IP de destino del ataque en cuestion.
El correo contiene la informacion de: Ip origen/destino, puerto origen/destino y tiempo de inicio del ataque.
Son necesarios los siguientes parametros:

- mail_from : Mail desde el cual se va a enviar la alerta.
- smtp_host: Nombre del servidor smtp que se utilizara para enviar los correos. Por defecto se utiliza el servidor SMTP de Prosecretaria de Informatica: medusa.psi.unc.edu.ar
- smtp_port: Puerto que utiliza el servidor SMTP. Por defecto utiliza el 25.

Esta informacion se puede modificar desde Cortex en cualquier momento.


Para mas informacion ver:
-------------------------
Documentacion Cortex 

- https://github.com/TheHive-Project/CortexDocs
