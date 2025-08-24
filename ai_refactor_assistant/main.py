import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

# --- New Configuration Block ---
# Load environment variables from the .env file
load_dotenv()

# Configure the Gemini API with the key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
# -----------------------------

# Create an instance of the FastAPI class
app = FastAPI()

# --- New CORS Middleware Block ---
origins = [
    "http://localhost:5173",
    "https://ai-refactor-pi.vercel.app/" # The address of our React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------

class CodeSnippet(BaseModel):
    code: str

# Pydantic model for the request body
class CodeSnippet(BaseModel):
    code: str

@app.get("/")
def read_root():
    return {"message": "AI Refactor Assistant is running!"}

@app.post("/analyze")
def analyze_code(snippet: CodeSnippet):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    prompt = f"""
    You are an expert software engineer. Your task is to refactor the following Python code to improve its readability, performance, and adherence to best practices. Also only provide the code, do not add whatever improvements you did or any justifications only the code.
    
    Provided Code:
    ```python
    {snippet.code}
    ```

    Return only the refactored code inside a single Python code block.
    """

    response = model.generate_content(prompt)

    # --- New Debugging & Error Handling ---
    # Print the full, detailed response to your terminal
    print(response) 

    try:
        # --- New Parsing Logic ---
        raw_text = response.text
        
        # 1. Remove the outer ```python and ``` fences
        # 2. Strip any leading/trailing whitespace
        clean_code = raw_text.replace("```python", "").replace("```", "").strip()
        
        return {"refactored_code": clean_code}
        # ------------------------
        
    except ValueError:
        return {"error": "Failed to get a response from the AI. It may have been blocked for safety reasons."}
    # --------------------------------------