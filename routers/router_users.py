from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from classes import models_orm, schemas_dto, database
import utilities
from typing import List


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('', response_model=schemas_dto.User_response, status_code= status.HTTP_201_CREATED)
async def create_user(
    payload: schemas_dto.User_POST_Body, 
    cursor: Session = Depends(database.get_cursor),
    ):
    try: 
        # 1. On ne stock pas le mot de pass "en claire" mais le hash
        hashed_password = utilities.hash_password(payload.userPassword) 
        # 2. Creation d'un object ORM pour être injecté dans la DB 
        new_user= models_orm.Users(password=hashed_password, email= payload.userEmail)
        # 3. Send query
        cursor.add(new_user) 
        # 4. Save the staged changes
        cursor.commit() 
        # Pour obtenir l'identifiant
        cursor.refresh(new_user) 
        return new_user # not a python dict -> donc il faut un mapping
    except IntegrityError: # Se déclanche si un utilisateur possède déjà la même email (unique=True)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists" 
        )
    
@router.get('', response_model=List[schemas_dto.User_response])
async def get_all_users(cursor: Session = Depends(database.get_cursor)):
    all_users = cursor.query(models_orm.Users).all()
    return all_users

# Exercice not an actual use case
@router.get('/{user_id}', response_model=schemas_dto.User_response)
async def get_user_by_id(user_id:int, cursor: Session = Depends(database.get_cursor)):
    corresponding_user = cursor.query(models_orm.Users).filter(models_orm.Users.id == user_id).first()
    if(corresponding_user):
        return corresponding_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No user with id:{user_id}'
        )