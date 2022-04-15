# Nextia Test
Technical test for backend developers


# To implement
- Django Rest Framework
- PostgreSQL
- Pandas
- Git
- Github

# Use cases
1. Create Project: "technicaltest"
2. Create Base model with:
    - **id:** Serial, Primary Key.
    - **created_at:** Datetime, auto created add.
    - **updated_at:** Datetime, auto updated add.

3. Create User model and CRUD with:
    - **name:** Varchar(50), not null.
    - **username:** Varchar(50), unique, not null.
    - **password:** Varchar(255), hashed, write only.

4. Simple JWT Authentication:
    - Only token access.
    - No refresh access.
    - Implemented in all endpoint.

5. Create Products ("Bienes") model with:
    - **name:** Varchar(255), not null.
    - **description:**: varchar(255), null.
    - **user**: Integer, Foreign Key related to User

6. Migrate data.csv to database using pandas.
    - User "admin" created when installing for the first time.
    - All products related to this user, unspecified requirement.

7. CRUD Products Model.
    - **GET:** with 3 versions:
        - GET: Get the product by path parameter.
        - LIST: Get all products.
        - LIST: Get all products by id list as query parameters (requirement 8).
    - **POST:** Create one product.
    - **PATCH:** Update one product by path parameter.
    - **DELETE:** Delete one product by path parameter.
    
    - All cases works only for JWT authenticated users
    - One user only can access to own products.


# Run project
### Requirements
- Docker, Docker Compose
- Python, Django, Django REST Framework

### First installation (on linux)
1. Install docker and docker-compose.
2. ```cd technicaltest```
3. Create the .env file as (for this example):
```
DEBUG=0
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost [::1] *

POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_DB=django
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
4. RUN ```docker-compose up``` and project is ready:
    - Database Ready.
    - Initial Django Migration.
    - Testing validation.
    - Initial data migration.
    - Project listen on port 8000.
5. For login use:
    - method: POST
    - route: HOST:8000/user/login
    - payload(json): {"username": "admin", "password": "admin"}
6. For register user use:
    - method: POST
    - route: HOST:8000/user/register
    - payload(json): {"username": "test", "password": "test"}