
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto

router = APIRouter(
    prefix='/classes',
    tags=['Classes']
)

# Read
@router.get('')
async def get_classes(
    cursor: Session= Depends(get_cursor), 
    limit:int=10, offset:int=0):
    all_classes = cursor.query(models_orm.Classes).limit(limit).offset(offset).all() # Lancement de la requête
    classes_count= cursor.query(func.count(models_orm.Classes.id)).scalar()
    return {
        "classes": all_classes,
        "limit": limit,
        "total": classes_count,
        "skip":offset
    }

# Read by id
@router.get('/{class_id}', response_model=schemas_dto.Class_GETID_Response)
async def get_class(class_id:int, cursor:Session= Depends(get_cursor)):
    corresponding_class = cursor.query(models_orm.Classes).filter(models_orm.Classes.id == class_id).first()
    if(corresponding_class):  
        return corresponding_class
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding class found with id : {class_id}"
        )

# CREATE / POST 
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_class(payload: schemas_dto.Class_POST_Body, cursor:Session= Depends(get_cursor)):
    new_class = models_orm.Classes(name=payload.className, price=payload.classPrice) # build the insert
    cursor.add(new_class) # Send the query
    cursor.commit() #Save the staged change
    cursor.refresh(new_class)
    return {"message" : f"New class {new_class.name} added sucessfully with id: {new_class.id}"} 

# DELETE ? 
@router.delete('/{class_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(class_id:int, cursor:Session=Depends(get_cursor)):
    # Recherche sur le etudiant existe ? 
    corresponding_class = cursor.query(models_orm.Classes).filter(models_orm.Classes.id == class_id)
    if(corresponding_class.first()):
        # Continue to delete
        corresponding_class.delete() # supprime
        cursor.commit() # commit the stated changes (changement latent)
        return
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding Class with id: {class_id}'
        )

# Update
@router.patch('/{class_id}')
async def update_class(class_id: int, payload:schemas_dto.Class_PATCH_Body, cursor:Session=Depends(get_cursor)):
    # trouver le etudiant correspodant
    corresponding_class = cursor.query(models_orm.Classes).filter(models_orm.Classes.id == class_id)
    if(corresponding_class.first()):
        # mise à jour (quoi avec quelle valeur ?) Body -> DTO
        corresponding_class.update({'featured':payload.newFeatured})
        cursor.commit()
        return corresponding_class.first()
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding Class with id: {class_id}'
        )