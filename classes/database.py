from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

database_url='put url to db here'

# create connection to db
database_engine = create_engine(database_url)
print("Connected to Database...")
# set cursor
SessionTemplate = sessionmaker(bind=database_engine, autocommit=False, autoflush=False)


def get_cursor():
    db= SessionTemplate()
    try:
        yield db
    finally:
        db.close()


