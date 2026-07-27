from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from google.cloud import vision
from AI.vision import getIngredients

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

    if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    content = await file.read()

    ingredients = getIngredients(content)

    return ingredients
        