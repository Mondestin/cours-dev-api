
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto

router = APIRouter(
    prefix='/students',
    tags=['Students']
)

# get list of students
@router.get('')
async def get_students(
    cursor: Session= Depends(get_cursor), 
    limit:int=10, offset:int=0):
    all_students = cursor.query(models_orm.Students).limit(limit).offset(offset).all() # Lancement de la requête
    students_count= cursor.query(func.count(models_orm.Students.id)).scalar()
    return {
        "students": all_students,
        "limit": limit,
        "total": students_count,
        "skip":offset
    }

# Read by id
@router.get('/{student_id}', response_model=schemas_dto.Student_GETID_Response)
async def get_student(student_id:int, cursor:Session= Depends(get_cursor)):
    corresponding_student = cursor.query(models_orm.Students).filter(models_orm.Students.id == student_id).first()
    if(corresponding_student):  
        return corresponding_student
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding Student found with id : {student_id}"
        )

# Create student
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_student(payload: schemas_dto.Student_POST_Body, cursor:Session= Depends(get_cursor)):
    new_student = models_orm.Students(name=payload.studentName, surname=payload.studentSurname, is_active=payload.studentIsActive) # build the insert
    cursor.add(new_student) 
    cursor.commit() 
    cursor.refresh(new_student)
    return {"message" : f"New Student {new_student.name} added sucessfully with id: {new_student.id}"} 



# Update student
@router.patch('/{student_id}')
async def update_student(student_id: int, payload:schemas_dto.Student_PATCH_Body, cursor:Session=Depends(get_cursor)):
    # find the user in the database
    corresponding_student = cursor.query(models_orm.Students).filter(models_orm.Students.id == student_id)
    if(corresponding_student.first()):
        # update student info in database using DTO
        corresponding_student.update({'name':payload.studentName, 'surname':payload.studentSurname, 'is_active':payload.studentIsActive,})
        cursor.commit()
        return corresponding_student.first()
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding Student with id: {student_id}'
        )
    
# delete student
@router.delete('/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id:int, cursor:Session=Depends(get_cursor)):
    # check if student exists
    corresponding_student = cursor.query(models_orm.Students).filter(models_orm.Students.id == student_id)
    
    # delete the first match
    if(corresponding_student.first()):
        corresponding_student.delete() # delete the student
        cursor.commit() # commit the stated changes
        return {"message" : f"Student was sucessfully deleted"}
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding Student with id: {student_id}'
        )