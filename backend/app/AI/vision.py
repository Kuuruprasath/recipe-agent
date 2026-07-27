from fastapi import File, HTTPException
from google.cloud import vision

def getIngredients(content):

    try:
        vision_client = vision.ImageAnnotatorClient()
    except Exception as e:
        print(f"Failed to initialise Vision Client: {e}")

    image = vision.Image(content=content)
    response = vision_client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations
    
    if response.error.message:
        raise HTTPException(status_code=500, detail=response.error.message)
    
    detected_objects = []
    for obj in localized_object_annotations:
        detected_objects.append({
            "name": obj.name,
            "confidence": obj.score,
        })
    
    return {
    "objects_found_count": len(detected_objects),
    "objects": detected_objects
    }
