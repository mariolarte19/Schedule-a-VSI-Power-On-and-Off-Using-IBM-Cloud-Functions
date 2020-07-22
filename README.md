# Power Off a VSI using IBM Cloud Functions

Este repositorio explica como apagar y prender de forma automatizada un VSI (Servidor virtual) en IBM Cloud utilizando Functions de IBM Cloud.
Requirements:
Requisitos:
* Docker CE instalado en su maquina.
* Python 3.7 para algunas pruebas locales.
* Sistema operativo linux.

Los pasos crean una acción en IBM Cloud Functions basada en un fragmento de código de Python 3.7.

### The Hard Way
1. Clonar este repositorio usando el comando "git clone" y acceder a la carpeta de la aplicación.
Ejemplo
```
git clone https://github.com/itirohidaka/PowerOff-Functions.git
```
```
cd PowerOff-Functions
```

2. Descargue la imagen Docker proporcionada por Functions.
```
docker pull ibmfunctions/action-python-v3.7
```

3. Descargue el paquete (softlayer) especificado en require.txt y colóquelo en el directorio virtualenv.
```
docker run --rm -v "$PWD:/tmp" ibmfunctions/action-python-v3.7 bash -c "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
```
4.Empaquete virtualenv y __main__.py en un archivo zip.
Example:
```
zip -r vsi-classic-power.zip virtualenv __main__.py
```

5. Inicie sesión en ibmcloud y prepare el entorno.
Example:
```
ibmcloud login
ibmcloud account orgs
ibmcloud account spaces
ibmcloud target -o "IBM" -s "Demo"                        # Asocia 
$ ibmcloud target -g Landingzone -r us-south              # Especifica el grupo de recursos y la región a la que pertenece la función 
$ ibmcloud fn namespace create poweroff-on-vsi            # Crea el espacio de nombres en el que se implementa la acción.
$ ibmcloud fn property set --namespace power-off-on-vsi   # Especifica el espacio de nombres creado anteriormente como el destino de despliegue de acción
```

6. Crea una acción . Al mismo tiempo, implemente el paquete (archivo zip).
```
ibmcloud fn action create <action_name> <zip_file> --kind <runtime>
```
Example:
```
ibmcloud fn action create vsi-classic-power-on vsi-classic-power.zip --kind python:3.7
ibmcloud fn action create vsi-classic-power-off vsi-classic-power.zip --kind python:3.7
```

7. Open the IBM Cloud console
```
open https://cloud.ibm.com
```

8.Inicie sesión en IBM Cloud Console con sus credenciales (nombre de usuario y contraseña)

9. Haga click en el menú de hamburguesa y haga clic en "Funciones"

10. Haga click en "Acciones" y compruebe si la Acción aparece en la lista. En mi ejemplo, estoy usando el nombre "vsi-classic-power-on y vsi-classic-power-off" para el nombre de la acción.

11. Haga click en Parametros y agregre los siguientes parametros.

```
vsi "nombre de VSI"
power "ON" o OFF"
apikey "apikey de infrestructura clasica"
user "Usuario softlayer"
```
Ejemplo

```
vsi ""power-off-on""
power "ON"
apikey "73bc6c593e7ef22d38edb204c060055d09c5ad171715"
user "2059386_mario.olarte@ibm.com"
```


12.incie la acción con el botón "Inicio" en la pantalla "Código" y verifique la operación. Si VSI ya se inició.

Imagen

13. El siguiente es un ejemplo de un trigger que se dispara a las 8:00 de lunes a viernes y un comando que crea un disparador que se dispara a las 18:00.

```
ibmcloud fn trigger create 0800weekday --feed /whisk.system/alarms/alarm -p cron "0 8 * * 1-5" 
ibmcloud fn trigger create 1800weekday --feed /whisk.system/alarms/alarm -p cron " 0 18 * * 1-5 "
```

14. Asociar el disparador de alarma de las 8 en punto con la acción de inicio y el disparador de alarma de las 18:00 con la acción de apagado.

```
ibmcloud fn rule create vsi-classic-power-on_0800weekday 0800weekday vsi-classic-power-on
ibmcloud fn rule create vsi-classic-power-off_1800weekday 1800weekday vsi-classic-power-off
```
15. El resultado de la ejecución del disparador se puede confirmar en la pantalla "Monitor".Puede ver el número de éxitos y fracasos en el nombre del activador de resumen de actividad (aquí 0800weekday y 1800weekday) y el gráfico de barras a la derecha de este. También puede verificar el historial de ejecución y los detalles del registro en el registro de actividad.

Imagen

La Funcion es creada con un trigger y una action!

Puedes tener una acción con varios trigger . Cada trigger con un nombre VSI diferente.


