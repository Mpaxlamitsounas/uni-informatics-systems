from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose InfoSys database
db = client['InfoSys']
students = db['Students']

# Initiate Flask App
app = Flask(__name__)

# Insert Student
# Create Operation
@app.route('/insertstudent', methods=['POST'])
def insert_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data or not "yearOfBirth" in data or not "email" in data:
        return Response("Information incompleted",status=500,mimetype="application/json")
    
    # count() deprecated
    result = students.find({"email":data["email"]})
    count = 0
    result = students.find({})
    for i in range(students.count_documents({})):
        try:
            result[i]
            count += 1
        except:
            break    
    
    if count == 0 :
        if len(data['address']) != 0:
            student = {"email": data['email'], "name": data['name'],  "yearOfBirth":data['yearOfBirth'], 'address': data['address']}
        else:
            student = {"email": data['email'], "name": data['name'],  "yearOfBirth":data['yearOfBirth']}
        # Add student to the 'students' collection
        students.insert_one(student)
        return Response("was added to the MongoDB",status=200,mimetype='application/json') 
    else:
        return Response("A user with the given email already exists",status=200,mimetype='application/json')

# Read Operations
# Get all students
@app.route('/getallstudents', methods=['GET'])
def get_all_students():
    iterable = students.find({})
    output = []
    for student in iterable:
        student['_id'] = None 
        output.append(student)
    return jsonify(output)

# Get the number of all the students in the DB 
@app.route('/getstudentcount', methods=['GET'])
def get_students_count():
    # count() deprecated
    number_of_students = 0
    result = students.find({})
    for i in range(students.count_documents({})):
        try:
            result[i]
            number_of_students += 1
        except:
            break    
        
    return jsonify({"Number of students": number_of_students})

# Find student by email
@app.route('/getstudent/<string:email>', methods=['GET'])
def get_student_by_email(email):
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')
    student = students.find_one({"email":email})
    if student !=None:
        student = {'_id':str(student["_id"]),'name':student["name"],'email':student["email"], 'yearOfBirth':student["yearOfBirth"]}
        return jsonify(student)
    return Response('no student found',status=500,mimetype='application/json')

# Get students with addresses
@app.route('/getStudentsWithAddress', methods=['GET'])
def get_students_with_address():
    iterable = students.find({'address': {'$ne': None}})
    output = []
    for student in iterable:
        student['_id'] = None 
        output.append(student)
    return jsonify(output)

# Find student adress by email
@app.route('/getStudentsAddress/<student_email>', methods=['GET'])
def get_students_address_by_email(student_email):
    students = get_students_with_address()
    
    for student in students.get_json():
        # Only 1 student per email
        if student['email'] == student_email:
            return student['address']
            
    return ''

# Find students with address and born between 1980-1989
@app.route('/getEightiesAddress', methods=['GET'])
def get_eighties_address():
    students = get_students_with_address()
    
    output = []
    for student in students.get_json():
        if 1980 <= student['yearOfBirth'] <= 1989:
            output.append(student)
            
    return jsonify(output)

# Get number of students with address
@app.route('/countAddress', methods=['GET'])
def count_address():
    students = get_students_with_address()
    
    number_of_students = 0
    for _ in students.get_json():
        number_of_students += 1
            
    return jsonify({"Number of students with addresses": number_of_students})

# Find students born in specific year
@app.route('/countYearOfBirth/<yearOfBirth>', methods=['GET'])
def count_year_of_birth(yearOfBirth):
    result = students.find({'yearOfBirth': int(yearOfBirth)})
    
    number_of_students = 0
    for i in range(students.count_documents({})):
        try:
            result[i]
            number_of_students += 1
        except:
            break
            
    return jsonify({'Number of students born in year': number_of_students})

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)