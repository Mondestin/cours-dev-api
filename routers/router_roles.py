
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/roles',
    tags=['Roles']
)

# get roles
@router.get('')
async def get_roles(
    # token: Annotated[str, Depends(oauth2_scheme)],
    cursor: Session= Depends(get_cursor), 
    limit:int=10, offset:int=0):
    all_roles = cursor.query(models_orm.Roles).limit(limit).offset(offset).all() # Lancement de la requête
    roles_count= cursor.query(func.count(models_orm.Roles.id)).scalar()
    return {
        "roles": all_roles,
        "limit": limit,
        "total": roles_count,
        "skip":offset
    }

# create role 
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_role( payload: schemas_dto.Role_POST_Body, cursor:Session= Depends(get_cursor)):
    new_role = models_orm.Roles(name=payload.roleName) # build the insert
    cursor.add(new_role) # Send the query
    cursor.commit() #Save the staged change
    cursor.refresh(new_role)
    return {"message" : f"New role {new_role.name} added sucessfully with id: {new_role.id}"} 

# delete a role  
@router.delete('/{role_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(token: Annotated[str, Depends(oauth2_scheme)], role_id:int, cursor:Session=Depends(get_cursor)):
    # Recherche sur le role existe ? 
    corresponding_role = cursor.query(models_orm.Roles).filter(models_orm.Roles.id == role_id)
    if(corresponding_role.first()):
        # Continue to delete
        corresponding_role.delete() # supprime
        cursor.commit() # commit the stated changes (changement latent)
        return
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding role with id: {role_id}'
        )

# Update a role
@router.patch('/{role_id}')
async def update_role(token: Annotated[str, Depends(oauth2_scheme)], role_id: int, payload:schemas_dto.Role_PATCH_Body, cursor:Session=Depends(get_cursor)):
    # trouver le role correspodant
    corresponding_role = cursor.query(models_orm.Roles).filter(models_orm.Roles.id == role_id)
    if(corresponding_role.first()):
      
        corresponding_role.update({'name':payload.roleName})
        cursor.commit()
        return corresponding_role.first()
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding role with id: {role_id}'
        )