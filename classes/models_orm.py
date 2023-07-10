from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Class de base pour créer les models
Base= declarative_base()

# Intermediate table for the many-to-many relationship
student_class_association = Table(
    'student_class_association',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('class_id', Integer, ForeignKey('classes.id')),
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()') 

)

# Les ORM sont des classes python basée sur les tables de notre base de données
class Students(Base):
    __tablename__= "students"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=True, server_default='TRUE') # server_default permet de donner une valeur par default
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')  #now() représente la date/time actuelle

    # Many-to-Many relationship
    classes = relationship("Class", secondary=student_class_association, back_populates="students")

class Classes(Base):
    __tablename__="classes"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    level = Column(String, nullable=False)
    create_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')  

    # Many-to-Many relationship
    students = relationship("Student", secondary=student_class_association, back_populates="classes")

class Users(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')  
    # bind user and role
    roles = relationship("Role", back_populates="user")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    # bind roles and User
    user = relationship("User", back_populates="roles")
  
    
    