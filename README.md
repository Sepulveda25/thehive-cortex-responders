# Responders para Cortex Analyzer 

[Volver a documento raiz](https://gitlab.unc.edu.ar/csirt/csirt-docs/tree/master#csirt-docs)

## Directorio de los responders
Los responders se encuentran en el directorio:
**/opt/Cortex-Analyzers/responders**

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
