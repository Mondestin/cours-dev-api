
from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

# Database 
from classes.database import database_engine 
import classes.models_orm 

#Routers
import routers.router_students, routers.router_users, routers.router_classes, routers.router_auth

# create tables if no presente in the Database
classes.models_orm.Base.metadata.create_all(bind=database_engine)

#Start Application
app= FastAPI( 
    title="Yousch API",
    description=api_description,
    openapi_tags=tags_metadata 
    )


# Set routes
app.include_router(routers.router_students.router)
app.include_router(routers.router_users.router)
app.include_router(routers.router_classes.router)
app.include_router(routers.router_auth.router)