from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from google import genai
from google.genai import types
import prompts
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=GEMINI_API_KEY)
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(system_instruction=prompts.system_prompt)
)

@app.get("/")
async def root():
    return {"message": "Backend is Running"}

@app.post("/upload-context-file")
async def upload_context_file(file: UploadFile = File(...)):
    if not (file.filename.endswith('.md') or file.filename.endswith('.txt')):
        raise HTTPException(status_code=400, detail="Only .md or .txt files are allowed.")
    content = (await file.read()).decode("utf-8")

    '''temporary response for testing, need to be commented later'''
    return {"response": "fil aagyi h"}
    try:
        # Directly get Gemini's summary or response for the uploaded content
        prompt = f"Answer from the following context only:\n\n{content}"
        response = chat.send_message(prompt)
        return {
            "response": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/gemini-response")
async def get_gemini_response(user_query: str = Form(...)):
    try:
        response = chat.send_message(user_query)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

