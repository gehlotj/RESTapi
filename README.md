# RESTful API using python and flask
The purpose of this demo is to create a simple REST API. We will be using python and Flask as our design platform and sql-lite as database operation and postman to test our API.

The demo example uses PUT,DELETE,GET and POST method. The program has a simple implementation of token based authentication.

### Usage
$ flask db_create\
$ flask db_seed\
$ python3 app.py

* To retrieve token\
http://localhost:5000/login \
In postman pass following form data:\
 ```email = rverma@goldmine.com```\
 ```password = audi```

* To add student\
http://localhost:5000/add_student \
In postman pass following form data:\
 ```student_id = 1```\
 ```first_name = Jagga```\
 ```last_name = Denim```
 ```grade = 9```

* To list students\
http://localhost:5000/list_all \
List all the entries

* To delete student\
http://localhost:5000/delete_student \
In postman pass following form data:\
 ```student_id = 1```

 #### Reference:
 * Postman :- https://www.postman.com/
