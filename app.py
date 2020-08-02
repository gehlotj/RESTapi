from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, or_
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath('.')
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir,"sis.db")
app.config['JWT_SECRET_KEY'] = 'your-secret'

db = SQLAlchemy(app)
mm = Marshmallow(app)
jwt = JWTManager(app)

#database operations
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')

@app.cli.command('db_delete')
def db_delete():
    db_drop_all()
    print('Database deleted')

@app.cli.command('db_seed')
def db_seed():
    verma = User(user_id = 1000,
                email = "yreddy@alwaysready.com",
                password = "007bond")

    reddy = User(user_id = 1001,
                email = "rverma@goldmine.com",
                password = "audi")

    student1 = Student(student_id = 100,
                        first_name = "Joe",
                        last_name = "Doe",
                        grade = 5)
    student2 = Student(student_id = 101,
                        first_name = "Tom",
                        last_name = "Worry",
                        grade = 6)
    student3 = Student(student_id = 102,
                        first_name = "Gerry",
                        last_name = "Sorry",
                        grade = 7)
    student4 = Student(student_id = 103,
                        first_name = "John",
                        last_name = "Demo",
                        grade = 8)

    db.session.add(verma)
    db.session.add(reddy)
    db.session.add(student1)
    db.session.add(student2)
    db.session.add(student3)
    db.session.add(student4)
    db.session.commit()
    print("Databasse data inserted")


@app.route('/')
def root():
    return jsonify(message = "")

@app.route('/login',methods=['POST'])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]
    get_email = User.query.filter_by(email = email, password = password).first()
    if get_email:
        access_token = create_access_token(identity = email)
        return jsonify(message = "Login Successfully", access_token = access_token)
    else:
        return jsonify(message = "Incorrect email or password"),401


@app.route('/lookup/<string:student_name>',methods=["GET"]) #get example
def lookup(student_name: str):
    get_name = Student.query.filter((Student.first_name == student_name.title()) | (Student.last_name == student_name.title())).all()
    if get_name:
        result = students_schema.dump(get_name)
        return jsonify(result)
    else:
        return jsonify(message="No student found with that name"), 404


@app.route('/add_student',methods=['POST']) #post example
@jwt_required
def add_student():
    get_id = request.form['student_id']
    result = Student.query.filter_by(student_id =  get_id).first()
    if result:
        return jsonify(message = "Student already exists"), 404
    else:
        f_name = request.form['first_name']
        l_name = request.form['last_name']
        grade = request.form['grade']

        new_student = Student(student_id = get_id,
                             first_name = f_name,
                             last_name = l_name,
                             grade = grade)
        db.session.add(new_student)
        db.session.commit()
        return jsonify(message="Student created successfully!!"),200


@app.route('/delete_student',methods=["DELETE"])
@jwt_required
def delete_student():
    get_id = request.form['student_id']
    result = Student.query.filter_by(student_id =  get_id).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        return jsonify(message="Student deleted successfully"),200
    else:
        return jsonify(message="No student with the ID entered"),401


@app.route('/update_student',methods=["PUT"])
@jwt_required
def update_student():
    get_id = request.form['student_id']
    result = Student.query.filter_by(student_id =  get_id).first()
    if result:
        result.first_name = request.form["first_name"]
        result.last_name = request.form["last_name"]
        result.grade = request.form["grade"]
        db.session.commit()
        return jsonify(message="Student record updated successfully!")

    else:
        return jsonify(message = "No student match found")


@app.route('/list_all',methods=["GET"])
def list_all():
    result = Student.query.all()
    if result:
        return jsonify(students_schema.dump(result))
    else:
        return jsonify(message="No record found")


#database models
class User(db.Model):
    __tablename__ = "users"
    user_id = Column(Integer,primary_key = True)
    email = Column(String, unique = True)
    password = Column(String)

class Student(db.Model):
    __tablename__ = "students"
    student_id = Column(Integer,primary_key = True)
    first_name = Column(String)
    last_name = Column(String)
    grade = Column(Integer)

#the following Marshmallow config return jsonify object.
class UserSchema(mm.Schema):
    class Meta:
        fields = ('user_id','email','password')

class StudentSchema(mm.Schema):
    class Meta:
        fields = ('student_id','first_name','last_name','grade')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


if __name__ == '__main__' :
    app.run(debug=True)
