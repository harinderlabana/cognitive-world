# --- Cognitive World - AI Backend (Upgraded with AI) ---
# This is the "brain" of our application. It now uses the Gemini API to think.

import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json # Import the json library to handle potential JSON parsing errors

# --- TUTORIAL: AI Configuration ---
# Replace the placeholder below with the API key you got from Google AI Studio.
# For a real application, you would store this key more securely, but for our
# hackathon, placing it here is the simplest way to get started.
API_KEY = "AIzaSyCZRoOnQWZ9HyORtJ0bNO7NHno2RjmgCtM" 
genai.configure(api_key=API_KEY)

# We are using a fast and powerful current model.
model = genai.GenerativeModel('gemini-1.5-flash')


# This is our data model for incoming commands. It remains unchanged.
class Command(BaseModel):
    text: str

# This is our FastAPI server instance.
app = FastAPI()

# The CORS middleware configuration also remains unchanged.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "AI Director is online and ready."}


# --- TUTORIAL: Upgraded Command Processor ---
# This is where the magic happens. This endpoint now talks to the AI.
@app.post("/process-command")
def process_command(command: Command):
    received_text = command.text
    print(f"Received command: '{received_text}'. Sending to Gemini AI...")

    # --- Prompt Engineering (IMPROVED) ---
    # We've added a special rule to our prompt to handle the "begin" command.
    prompt = f"""
    You are the director of a 3D virtual world. You will receive a command from a user.
    Your job is to decide what action to take.
    You must respond with ONLY a JSON object with two keys: "action" and "target".
    - The "action" can be 'change_scenery', 'display_text', or 'unknown'.
    - The "target" is the subject of the command (e.g., "Mars", "the ocean").
    
    SPECIAL RULE: If the user command is "begin", "start", or "go", the action must be 'change_scenery' and the target should be 'a mountain landscape'.
    
    User command: "{received_text}"
    
    Your JSON response:
    """

    try:
        # We send our carefully crafted prompt to the Gemini model.
        response = model.generate_content(prompt)
        
        # We clean up the AI's response to make sure it's valid JSON.
        ai_response_text = response.text.strip().replace("`", "").replace("json", "")
        print(f"AI response received: {ai_response_text}")

        # We will now parse the JSON here on the backend to ensure it's valid
        # before sending it. This is a more robust approach.
        try:
            # We try to parse the AI's text response into a Python dictionary.
            json_response = json.loads(ai_response_text)
            # If successful, FastAPI will automatically convert this dictionary back to a JSON response for the frontend.
            return json_response
        except json.JSONDecodeError:
            # If the AI gives us a response that isn't perfect JSON, we catch the error.
            print("Error: AI did not return valid JSON.")
            return {"action": "error", "target": "AI response was not valid JSON."}


    except Exception as e:
        # If anything goes wrong with the AI call, we'll log it and send an error.
        print(f"Error calling Gemini API: {e}")
        return {"action": "error", "target": "Could not process command with AI."}

