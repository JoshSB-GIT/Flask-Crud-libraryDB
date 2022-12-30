# API con flask y MySQL
## Proyecto para parcticar con el framework flask

Este proyecto está siendo creado unicamente por mi para entender mejor el funcionamiento del framework flask y mejorar la forma en la que programo con él. aún no está terminado, pero puede editar, actualizar, eliminar, insertar y leer datos de todas las tablas de la base de datos, a excepción de una, pero... ¡ya estoy por terminarla!.


## ¿Cómo puedes ejecutar el proyecto?

Lo primero que debes hacer es crear un entorno virual desde la terminal con el comando:
```sh
py -m venv env 
```
Luego ve a la ruta ```env/Scripts/``` y por ultimo ejecuta con ```.\activate``` el entorno virtual, después de eso es mejor que te dirijas a la ruta raíz del proyecto.

Por úlimo puedes ejecutar la API con el comando:
```
python .\src\app.py
```

Puedes hacerle las pruebas que desees con programas como postman o insomnia.

## Dependencias

En caso de que llegues a presentar errores que yo no tengo, pues la API hasta ahora no tiene ninguno, sería bueno que instales todo lo que flask y la misma API necesita para arrancar correctamente. 

Para hacer este procedimiento más sencillo, me tomé la libertad de crear un archivo llamado "requirements.txt" donde se encuentran absolutamente todas las dependencias.
```sh
pip install -r requirements.txt
```

## En caso de problemas
Si tienes problemas aún con las dependencias instaladas, podrías actualizar PIP con:
```sh
py -m pip install --upgrade pip
```
Tambíen debes instalar (todas estas dependencias están en el archivo "requirements.txt"):
```sh
pip install wheel
```
Por último, si por algún motivo no se installó flask_mysql usa:
```sh
pip install flask flask_mysqldb
```
