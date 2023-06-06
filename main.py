from fastapi import FastAPI, Body, Response, status,HTTPException
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
@app.get("/students",)
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
async def createStudent(student: Student, response: Response):
    # add new student in array of students
    students.append(student)
    # setting the status code
    response.status_code=status.HTTP_201_CREATED
    return { "message": "Student " + student.name + " added succesfully "}

# get student by id
@app.get("/student/{student_id}")
async def showStudent(student_id: int, response: Response):
    
    # check if the student was found
    try: 
     #find student in the array
     student=students[student_id-1]
     # setting the status code
     response.status_code=status.HTTP_200_OK
     return student
    except:
      raise HTTPException(
         status.HTTP_404_NOT_FOUND,
         detail="Student was not found"
      )
        
# delete student from list
@app.delete("/student/{id}", status_code=200)
async def deleteStudent(id: int):
    #delete student from the list
    students.pop(id)
    return { "message": "Student deleted succesfully"}