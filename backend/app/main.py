from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    try:

        filepath = f"uploads/{file.filename}"

        contents = await file.read()
        with open(filepath, "wb") as f:
            f.write(contents)
                
        return {"status": "success", "filename": file.filename, "saved_to": filepath}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")