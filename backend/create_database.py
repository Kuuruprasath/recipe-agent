from app.database import Base
from app.database import engine
from app.models.fridge_images import FridgeImage
from app.models.ingredients import Ingredient

Base.metadata.create_all(bind=engine)

print("Tables created")