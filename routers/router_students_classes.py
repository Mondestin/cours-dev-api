from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm
import utilities
from sqlalchemy.exc import IntegrityError

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


router= APIRouter(
    prefix="/students/classes",
    tags=["RelationsStudents"]
)

@router.get('')
async def list_transactions(
    token: Annotated[str, Depends(oauth2_scheme)], 
    cursor: Session = Depends(get_cursor)):
    #   get all relations between students and classes
        all_relations = cursor.query(models_orm.student_class_association).all()
        return all_relations 


class relation_post(BaseModel):
    student_id:int
    class_id:int

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_transaction(
    token: Annotated[str, Depends(oauth2_scheme)], 
    payload:relation_post,
    cursor: Session = Depends(get_cursor)
    ):
    
    new_relation= models_orm.student_class_association(student_id=payload.student_id, class_id=payload.class_id)
    try : 
        cursor.add(new_relation)
        cursor.commit()
        cursor.refresh(new_relation)
        return {'message' : f'New relation added successéfully' }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error while creating relation between student and class'
        )