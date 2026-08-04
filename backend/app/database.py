import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL =", DATABASE_URL)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

from app.models.fridge_images import FridgeImage
from app.models.ingredients import Ingredient

def saveDatabase(fname, path, ingredients):

    db = SessionLocal()
    try:

        db_image = FridgeImage(
            filename=fname,
            image_path=path
        )

        db.add(db_image)
        db.flush()

        for ingredient in ingredients["ingredients"]:

            db.add(
                Ingredient(
                    image_id=db_image.id,
                    name=ingredient["name"],
                    confidence=ingredient["confidence"],
                    category=ingredient["category"]
                )
            )

        db.commit()
        db.refresh(db_image)
        return db_image.id

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()