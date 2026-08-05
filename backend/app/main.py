from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from google.cloud import vision
from app.AI.vision import getIngredients
import uuid
from app.database import saveDatabase, getIngredient, updateIngredient
from pydantic import BaseModel

# 1. Define the schema first
class IngredientSchema(BaseModel):
    id: int
    name: str
    confidence: float
    category: str

    class Config:
        from_attributes = True 

app = FastAPI()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/kuuru/Downloads/kitchen-agent-503711-160bde113797.json"

# Middlewares to tell backend where to communicated with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Smart Recipe API is running"}


# Function that receives a file and uploads it to a local storage
@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    UPLOAD_FOLDER = "uploads"
    # Check if uploaded file is an image
    if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
    # Getting the bytes of image
    image_bytes = await file.read()
    #Saving each file
    filename = f"{uuid.uuid4()}.jpg"

    path = os.path.abspath(os.path.join(UPLOAD_FOLDER,filename))

    with open(path, "wb") as f:
        f.write(image_bytes)

    ingredients = getIngredients(
        image_bytes=image_bytes, 
        mime_type=file.content_type # What is the file type
    )
    # image_id = saveDatabase(filename,path,ingredients)
    image_id = 1

    return image_id

@app.get("/api/ingredients/{image_id}")
async def get_ingredients(image_id: int):


    ingredients = getIngredient(image_id)

    return [
        {
            "id": ingredient.id,
            "name": ingredient.name,
            "confidence": ingredient.confidence,
            "category": ingredient.category
        }
        for ingredient in ingredients
    ]


@app.put("/api/ingredients/{image_id}")
def update_ingredients(image_id: int, ingredients: list[IngredientSchema]):

    try:
        updateIngredient(image_id,ingredients)
    except Exception as e:
        raise HTTPException(
            detail=f"Database update failed: {str(e)}"
        )


    return {"message": "Updated"}
        