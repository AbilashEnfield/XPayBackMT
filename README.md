
# FastAPI with PostgrSQL and MongoDB

I have created this project with three main features signup, upload image and get user details.



## Deployment

I have dockerized this project with three containers PostgreSQL, FastAPI and Pgadmin

Pull from this Github repository and run following commands:

**To build and start the containers**
```bash
  docker-compose up -d --build
```

**To initialize the database and schema**
```bash
  docker-compose run web alembic upgrade head
```

**To detect the available models and create migration file**
```bash
  docker-compose run web alembic revision --autogenerate -m "first migration"
```
**To imigrate the models using the migration file created in previous step**
```bash
  docker-compose run web alembic upgrade head
```
 ### Now the APP is ready to go...

## API Reference

#### Test FastAPI running

```http
  GET localhost:8000/
```

#### User signup

```http
  POST localhost:8000/api/users/signup/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `full_name`      | `string` | **Required**. Full name of the user |
| `email`      | `string` | **Required**. User email address |
| `password`      | `string` | **Required**. Password |
| `phone`      | `string` | **Required**. User mobile number |

```
Sample:
  {
    "full_name":"Abilash",
    "email":"abilash@here.com",
    "password":"letmepass",
    "phone":"1234567897"
}
```

#### Upload Profile Picture

```http
  POST localhost:8000/api/users/upload/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `file` | **Required**. Profile Picture |
| `email`      | `string` | **Required**. Registered email |
| `database`      | `string` | **Required**. "P" for PostgreSQL and "M" for storing image in MongoDB |


#### Get User details

```http
  GET localhost:8000/api/users/details/{email}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email`      | `string` | **Required**. Registered email |




## DATABASE
## Postgres

log in to the pgadmin running in local at http://localhost:5050/ to check the tables and its entries.

STEP 1:

**Login with credentials**

email : pgadmin4@pgadmin.org

password : admin

STEP 2:

**Create a new server**

Name : FastAPI

Host : db

Username : postgres

Password : postgres

Once the database server is created. Ouer tables and datas will be under database Postgres -> Schema -> Tables.

## MongoDB

Login into MongoDB Cloud at https://account.mongodb.com/account/login with email abilashenfield@gmail.com and password "LetMePass123".

And move to Dashboard then Database -> Browse Collections ->  our collections will be stored there.



## ------------------------------------------ Happy Coding👨‍💻 ------------------------------------------------