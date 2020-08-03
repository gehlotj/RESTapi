# RESTful API using python and flask
The purpose of this demo is to create a simple REST API. We will be using python and Flask as our design platform and sql-lite for our database operation and postman to test our API.

The demo example uses PUT,DELETE,GET and POST method to demonstrate the basic functionality of API. The program also has a basic JWT authentication model implementation as well.

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
