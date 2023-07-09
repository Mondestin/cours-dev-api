
from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata


# Database 
from classes.database import database_engine 
import classes.models_orm # Import des ORM

#Import des routers
import routers.router_students, routers.router_users, routers.router_classes, routers.router_auth

# Créer les tables si elles ne sont pas présente dans la DB
classes.models_orm.Base.metadata.create_all(bind=database_engine)





#Lancement de l'API
app= FastAPI( 
    title="Yousch API",
    description=api_description,
    openapi_tags=tags_metadata # tagsmetadata definit au dessus
    )

# Ajouter les routers dédiés
app.include_router(routers.router_students.router)
app.include_router(routers.router_users.router)
app.include_router(routers.router_classes.router)
app.include_router(routers.router_auth.router)