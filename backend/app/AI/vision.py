import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
# Load the api key from .env
# client = genai.Client(
#     api_key=os.environ["GEMINI_API_KEY"]
# )

# Prompting gemini to give json of the ingredients found in the image
def getIngredients(image_bytes: bytes, mime_type: str):

    # prompt = """
    #             You are an expert food recognition assistant.

    #             Analyse this refrigerator image.

    #             Identify every visible edible ingredient.

    #             Rules:
    #             - Ignore shelves.
    #             - Ignore containers unless the food inside is clearly visible.
    #             - Ignore kitchen appliances.
    #             - Merge duplicate ingredients.
    #             - Use lowercase singular ingredient names.
    #             - Confidence must be between 0 and 1.

    #             Return ONLY valid JSON.

    #             {
    #                 "ingredients":[
    #                     {
    #                         "name":"",
    #                         "confidence":0.0,
    #                         "category":""
    #                     }
    #                 ]
    #             }
    #         """

    # response = client.models.generate_content(
    #     model="gemini-3.6-flash",
    #     contents=[
    #         prompt,
    #         types.Part.from_bytes(
    #             data=image_bytes,
    #             mime_type=mime_type,
    #         ),
    #     ],
    #     config=types.GenerateContentConfig( 
    #         response_mime_type="application/json",
    #     ),
    # )
    response = """{
  "ingredients": [
    {
      "name": "milk",
      "confidence": 0.99,
      "category": "dairy"
    },
    {
      "name": "egg",
      "confidence": 0.98,
      "category": "protein"
    },
    {
      "name": "broccoli",
      "confidence": 0.93,
      "category": "vegetable"
    }
    ]
    }
    """
    #Add response.text
    return json.loads(response)