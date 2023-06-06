from fastapi import FastAPI
from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    email: str 

app= FastAPI() #variable names for the server

# init list of students
students = [
    {
    "id": 1,
    "name": "John",
    "email": "test@yousch.com",
    },
    {
    "id": 2,
    "name": "John Doe",
    "email": "test-2@yousch.com",
    }
]
# default route
@app.get("/")
async def root():
    return {"message": "hello from main"}

# get students list
@app.get("/students")
async def getStudents():
    # return list of students
    return {
           "students" :students,
           "limit": 10,
           "total" : 2,
           "skip": 0
        }

# post student
@app.post("/student")
async def createStudent(student: Student):
    # add new student in array of students
    students.append(student)
    return { "message": "Student " + student.name + " added succesfully "}

# get student by id
@app.get("/student/{id}")
async def showStudent(id: int):
    #find student in the array
    return students[id-1]

# delete student from list
@app.delete("/student/{id}")
async def deleteStudent(id: int):
    #delete student from the list
    students.pop(id)
    return { "message": "Student deleted succesfully"}