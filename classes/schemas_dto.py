from datetime import datetime
from pydantic import BaseModel

# DTO : Data Transfert Object ou Schema
# Représente la structure de la données (data type) en entrée ou en sortie de notre API.

# STUDENT
class Student_POST_Body (BaseModel):
    studentName: str
    studentSurname: str
    studentIsActive: bool
 

class Student_PATCH_Body (BaseModel):
    studentName: str
    studentSurname: str
    studentIsActive: bool

class Student_GETID_Response(BaseModel): # format de sortie (response)
    id: int
    name: str
    surname: str
    is_active: bool
    class Config: # Lors des réponses, nous avons souvant à utiliser les données sortie de notre database. La Config ORM nous permet de "choisir" les columnes à montrer. 
        orm_mode= True
        
# CLASS
class Class_POST_Body (BaseModel):
    className: str
    classLevel: str

class Class_PATCH_Body (BaseModel):
    className: str
    classLevel: str

class Class_GETID_Response(BaseModel): # format de sortie (response)
    id: int
    name: str
    level: str
    class Config: # Lors des réponses, nous avons souvant à utiliser les données sortie de notre database. La Config ORM nous permet de "choisir" les columnes à montrer. 
        orm_mode= True

# USER
class User_POST_Body (BaseModel):
    userEmail:str
    userPassword: str

class User_PATCH_Body (BaseModel):
    userEmail:str
    userPassword: str

class User_response (BaseModel): 
    id: int
    email:str
    create_at: datetime
    # not sending the password
    class Config: # Importante pour la traduction ORM -> DTO
        orm_mode= True  

# Role
class Role_POST_Body (BaseModel):
    roleName:str

class Role_PATCH_Body (BaseModel):
    roleName:str

class Role_response (BaseModel): 
    id: int
    name:str
    class Config: # Importante pour la traduction ORM -> DTO
        orm_mode= True      