from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from classes.database import get_cursor
from classes import models_orm, schemas_dto, database
import utilities
from typing import List

# Ajout du schema Oauth sur un endpoint précis (petit cadenas)
# Le boutton "Authorize" ouvre un formulaire en popup pour capturer les credentials
from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# create user
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
# egt list of users
@router.get('', response_model=List[schemas_dto.User_response])
async def get_all_users(cursor: Session = Depends(database.get_cursor)):
    all_users = cursor.query(models_orm.Users).all()
    return all_users

# get user by id
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
    
# update user
@router.patch('/{user_id}', response_model=schemas_dto.User_response)
async def update_student(token: Annotated[str, Depends(oauth2_scheme)], user_id: int, payload:schemas_dto.User_PATCH_Body, cursor:Session=Depends(get_cursor)):
    corresponding_user = cursor.query(models_orm.Users).filter(models_orm.Users.id == user_id)
    if(corresponding_user.first()):
        # encrypt the user new password 
        new_hashed_password = utilities.hash_password(payload.userPassword) 
        # update student info in database using DTO
        corresponding_user.update({'email':payload.userEmail, 'password':new_hashed_password})
        cursor.commit()
        return corresponding_user.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No user with id:{user_id}'
        )

# delete user
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(token: Annotated[str, Depends(oauth2_scheme)], user_id:int, cursor:Session=Depends(get_cursor)):
    # check if user exists
    corresponding_user = cursor.query(models_orm.Users).filter(models_orm.Users.id == user_id)
    
    # delete the first match
    if(corresponding_user.first()):
        corresponding_user.delete()
        cursor.commit() 
        return {"message" : f"User was sucessfully deleted"}
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding user with id: {user_id}'
        )