# scraping-udemy-list-courses-for-user

Dado una perfil business de la forma:  
https://XXXX.udemy.com/user/YYYYY/  

lista los cursos a los que el usuario esta YYYYY esta inscripto usando la api de publica de udemy.

## Breve explicación:  
Dado el perfil se realiza scraping para poder sacar el id de usuario, usando ese id de usuario e interactuando con la api de udemy se puede ir recorriendo pagina y trabajando los json para sacar los cursos que posee.
Tambien se puede sacar los datos de los cursos: precio, autores, icono y otros datos, pero no viene al objetivo del script-

## Instalar:
``pip install -r requirements.txt``

## Ejecutar:
``python main.py``
 
