from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Ingredient(Base):

    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    image_id = Column(
        Integer,
        ForeignKey("fridge_images.id")
    )
    name = Column(String)
    confidence = Column(Float)
    category = Column(String)
    
    image = relationship(
        "FridgeImage",
        back_populates="ingredients"
    )