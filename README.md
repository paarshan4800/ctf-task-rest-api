# CTF Backend Task
## This API is created using **Flask-RESTful** and **MySQL** database.

## Setup
### [Download Python](https://www.python.org/downloads/)


### [Download MySQL Server](https://dev.mysql.com/downloads/installer/)

**Important** : *Remember the username and passowrd while setting up MySQL. We will need this for Flask and MySQL connection.*

In this [db.sql](https://github.com/paarshan4800/ctf-task-rest-api/blob/master/db.sql), there is sql code for database and table creation and few insertion statements.

Now open MySQL Command Line Client and copy/follow those statements/instructions in [db.sql](https://github.com/paarshan4800/ctf-task-rest-api/blob/master/db.sql).

In this [config.py](https://github.com/paarshan4800/ctf-task-rest-api/blob/master/config.py), instead of `<user>` and `<password>` in user and password field, enter the username and password you gave while MySQL setup.

### [Setup Flask](https://www.youtube.com/watch?v=QjtW-wnXlUY)




## Packages to be installed using pip
`pip install flask`

`pip install flask_restful`

`pip install flask_mysqldb`

`pip install flask_cors`

`pip install PyJWT`



# API Endpoints
This API has six endpoints.

* Login
* Get all records **
* Search records **
* Add new record **
* Delete existing record **
* Update existing record **

**Note** : ** *Token is needed for access*

*Assuming that the flask server is running on port* **5000**.

**Base URL** - http://127.0.0.1:5000/

## Login
`http://127.0.0.1:5000/login` - **POST** Method


Only existing users can access these API endpoints.

Username | Password
------------ | -------------
user123 | testing123
user456 | testing456
user789 | testing789


**Note** : *Inorder to access the endpoints, access token must be obtained and should be included in the header.*

To obtain the access token, enter username and password with basic authentication type under authorization tab.

**Note** : *Access Token will automatically expire in 10 minutes. To access endpoints, login again.*


Login Auth![Login Auth](/images/login/auth.png)


Access Token![Access Token](/images/login/response.png)


## Get all records

`http://127.0.0.1:5000/records` - **GET** Method

To access this endpoint, include the access token obtained in ***value*** column with key as ***access-token*** under the headers tab.

Token for Records![Token for Records](/images/records/access_token.png)


Response![Response](/images/records/response.png)

If endpoints are accessed without access token, it will return
![](/images/token_1.png)



## Search records

`http://127.0.0.1:5000/record` - **GET** Method

To search records by name, enter the name to search in **JSON** format in body tab.

Like this, `{ "name" : "bruno" }`

Search Body![Search Body](/images/record/search_body_json.png)


Search Response![Search Response](/images/record/search_response.png)


## Add new record

`http://127.0.0.1:5000/record` - **POST** Method

To search records by name, enter the name to search in **JSON** format in body tab.

Like this, `{ "name" : "de gea" }`

Add Body![Add Body](/images/record/add_body_json.png)


Add Response![Add Response](/images/record/add_response.png)


## Delete existing record

`http://127.0.0.1:5000/record` - **DELETE** Method

To delete a record, enter the id of the record in **JSON** format in body tab.

Like this, `{ "id" : 12 }`

Delete Body![Delete Body](/images/record/delete_body_json.png)


Delete Response![Delete Response](/images/record/delete_response.png)


## Update existing record

`http://127.0.0.1:5000/record` - **PUT** Method


To update a record, enter the id and the new name of the record in **JSON** format in body tab.

Like this, `{ "id" : 12 , "name" : "david de gea" }`

Update Body![Update Body](/images/record/update_body_json.png)


Update Response![Update Response](/images/record/update_response.png)
