#

from sqlalchemy                 import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import sessionmaker

from utils import constants


USERNAME = constants.DB_USERNAME
PASSWORD = constants.DB_PASSWORD
HOSTNAME = constants.DB_HOST
PORT     = int(constants.DB_PORT)
DB       = constants.DB_DATABASE

SQLALCHEMY_DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

BaseClass = declarative_base()
