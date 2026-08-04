from app.database import SessionLocal
from app.models.fridge_images import FridgeImage
from app.models.ingredients import Ingredient

db = SessionLocal()

print("Images:")
for image in db.query(FridgeImage).all():
    print(image.id, image.filename)

print()

print("Ingredients:")
for ingredient in db.query(Ingredient).all():
    print(
        ingredient.id,
        ingredient.image_id,
        ingredient.name,
        ingredient.confidence,
        ingredient.category
    )

db.close()