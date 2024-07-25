# init_db.py is responsible for creating the tables in the database.
from infra import Base, engine
from models import User  # Import all other models here as well

def init_db():
	# Create all tables
	Base.metadata.create_all(engine)

if __name__ == "__main__":
	init_db()