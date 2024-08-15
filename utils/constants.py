#

from dotenv import load_dotenv
import os


load_dotenv()


SECRET_KEY = "8ad0e156393dd1fda266d418b0ed3fad7514dc6ebed3e9ff8d35cb235dd4aa32"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DB_HOST     = os.getenv("DATABASE_HOST") 
DB_PORT     = os.getenv("DATABASE_PORT")
DB_USERNAME = os.getenv("DATABASE_USERNAME")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_DATABASE = os.getenv("DATABASE_NAME")
