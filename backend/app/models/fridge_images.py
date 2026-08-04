from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from app.database import Base
# Creating FridgeImage table
class FridgeImage(Base):

    __tablename__ = "fridge_images"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    image_path = Column(String, nullable=False)
    
    # Creating a relationship with ingredients table
    ingredients = relationship(
        "Ingredient",
        back_populates="image",
        cascade="all, delete-orphan"
    )