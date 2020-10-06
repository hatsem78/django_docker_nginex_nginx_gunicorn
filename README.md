# Integración backend tdd django-rest-api

## Tecnología usada

###Backend
Django REST framework https://www.django-rest-framework.org/
seguridad utilizada es por tocken 
Ejemplo 

    curl -X GET --header 'Accept: application/coreapi+json' --header 'X-CSRFToken: ncl2GtZSzWkGLHvjC7PXtR1Ai2XgZsB4fxDJ1dVdnlbbq0y7G6v1jE0dlfYVVM9f' 'http://localhost:8010/api/check_weather/list/'
    
Utilización de Django-chache

servidor nginx y gunicorn

Deployment Docker

base de datos: Postgress 



###FrontEnd
Django y vue.js


###Utilizacion del sistema

Se debe contruir los contendores del sistemao:
    
    # Construye la imagen con las modificaciones del Dockerfile
    docker-compose build
    
    # Realizar una copia del archivo .env.sample he ingresar las credenciales de base de datos y api clima
    sudo cp .env.sample .env
    
    # Correr los archivos estaticos COMPOSE_HTTP_TIMEOUT=120 en caso de error timeout
    COMPOSE_HTTP_TIMEOUT=120 docker-compose run app sh -c "python manage.py collectstatic"
    
    # Correr los test garantia que las configuraciones de base de datos sean correcta y también de django
    COMPOSE_HTTP_TIMEOUT=120 docker-compose run app sh -c "echo yes | python manage.py collectstatic"
Ya generado las imagenes para utilizar el sistema se deben crear usuario admin

    docker-compose run app sh -c "python manage.py createsuperuser"
    Email: administrador@gmail.com
    Password: 
    Password (again): 
    Superuser created successfully.
    
Para utilizar el sistema una vez creado el administrador
     # puede cambiar el puerto configurado en el docker-compose
     docker-compose up
     
link: http://localhost:8005

### Lista de apis utilizadas

    app_name = 'meetup'
    http://localhost:8010/api/meetup/list/
    http://localhost:8010/api/meetup/list_page/
    http://localhost:8010/api/meetup/create/
    http://localhost:8010/api/meetup/update/<id>
    http://localhost:8010/api/meetup/get_meetup/<id>
    http://localhost:8010/api/meetup/delete/<id>
    
    app_name = 'check_weather'
    http://localhost:8010/api/check_weather/list/
    
    app_name = 'meetup_enroll_invite_users'
    http://localhost:8010/api/meetup_enroll_invite_users/list/
    http://localhost:8010/api/meetup_enroll_invite_users/list_page/
    http://localhost:8010/api/meetup_enroll_invite_users/create/
    http://localhost:8010/api/meetup_enroll_invite_users/update/<id>
    http://localhost:8010/api/meetup_enroll_invite_users/get_meetup/<id>
    http://localhost:8010/api/meetup_enroll_invite_users/delete/<id>
    
    app_name = 'notification'
    http://localhost:8010/api/notification/list/
    http://localhost:8010/api/notification/list_page/
    http://localhost:8010/api/notification/create/
    http://localhost:8010/api/notification/update/<id>
    http://localhost:8010/api/notification/delete/<id>
    http://localhost:8010/api/notification/is_seen/<id>
    http://localhost:8010/api/notification/is_read/<id>
    
    app_name = 'registration_check_in_user'
    http://localhost:8010/api/registration_check_in_user/registration/
    http://localhost:8010/api/registration_check_in_user/check_in/<id>
    
    app_name = 'user'
    http://localhost:8010/api/user/create/
    http://localhost:8010/api/user/token/
    http://localhost:8010/api/user/me/
 
    
 ### Implementaciíon integración continua
 
Para este caso práctico utilizamos la herramienta travis Sincronisa fácilmente el proyecto con CI para probar el código.  

    # Para implementar travis hay que copiar y renombrar el archivo 
    cp .travis.yml.sample .travis.yml 