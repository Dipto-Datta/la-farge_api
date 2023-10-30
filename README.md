# A powerful production level django boilerplate 

# prerequisite
    1. install [docker](https://docs.docker.com/engine/install/)
    2. install make -linux/mac

# How to run - linux/mac
    1. clone this repo
    2. cd repo
    2. make run-db
    3. make run
    4. make makemigrations
    5. make migrate

# How to run - windows
    1. clone this repo
    2. cd repo
    3. docker compose up -d db
    4. docker compose up backend --build --remove-orphans
	5. docker compose run backend python manage.py makemigrations
	6. docker compose run backend python manage.py migrate



# Features:
    1. add docker compose ✅
    2. add dockerfile ✅
    3. add makefile ✅
    4. add .gitignore ✅
    5. create django project ✅
    6. folder structure ✅
    7.  connect docker postgres db ✅
    8. create user model ✅
    9. create serializer ✅
    10. create model managemnet view with flter, search, pagination ✅
    11. create auth routes and views
        implement, manage JWT ✅
        create auth routes ✅
    12. implement swagger ✅
    13. handle authorization:
            create auth groups ✅
            provide permissions ✅

# Todo 
    * OTP login - email and sms
        1. no password only OTP login
        2. OTP verify on registration
    * auth routes:
        auth/ password/reset/ [name='rest_password_reset']
        auth/ password/reset/confirm[name='rest_password_reset_confirm']
    * Two Setp -- future
    * create global error handler
    * implement custom middleware/decorators


# Auth routes and sample payload
    POST -> auth/registration/ 
        {
        "email":"you@email.com",
        "password":"your_strong_password",
        "confirm_password":"your_strong_password"
        }
    
    POST -> auth/login/
        {
        "email":"you@email.com",
        "password":"your_strong_password"
        }

    POST -> auth/logout/
        ** access token required
        {
            "refresh":"your_refresh_token"
        }
    
    GET auth/user/
        ** access token required
    PUT auth/user/:id/
        ** access token required
        {
        "id": id,
        "key": "value",
        "key": "value",
        .
        .
        .
        "key":"value"
        }
    PATCH auth/user/:id/  -- for updating a single field
        ** access token required
        {
        "id": id,
        "key": "value"
        }
    DELETE auth/user/:id/
        ** access token required

    auth/password/change/
    auth/token/verify/
    auth/token/refresh/


[//]: # (drop schema public cascade;)

[//]: # (create schema public;)

[//]: # (This is how I resolve aulter user model mid project:)

[//]: # (Drop the database but DO NOT delete the User initial migration.)

[//]: # (Make sure in your 0001_initial.py -> class Migration.initial is set to True.)

[//]: # (Run migration python manage.py migrate)
