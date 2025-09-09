# --- Cognitive World - AI Backend ---
# This file will be the "brain" of our application.
# It uses FastAPI to create a web server that our frontend can talk to.

# First, we import the necessary tools.
# Pydantic's BaseModel is used to define the structure of the data we expect to receive.
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# This is a "data model". It tells FastAPI that when a request comes in,
# it should expect a JSON object with a key named "text" that has a string value.
# For example: {"text": "hello world"}
class Command(BaseModel):
    text: str

# Create an instance of the FastAPI application. This is our main server object.
app = FastAPI()

# --- CORS Middleware ---
# This is a crucial security step. By default, a web browser will not allow a webpage
# (our index.html) to make requests to a different address (our Python server)
# unless the server explicitly gives it permission. This code gives that permission.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for our simple test case)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# --- API Endpoints ---
# An "endpoint" is a specific URL on our server that the frontend can send requests to.
# The "@app.get('/')" is a "decorator". It tells FastAPI that any GET request
# to the main URL ("/") should be handled by the function right below it.
@app.get("/")
def read_root():
    # For now, this function just sends back a simple welcome message.
    # The message is in a format called JSON, which is the standard way for
    # APIs to communicate.
    return {"message": "Hello from the AI Director!"}

# TUTORIAL UPDATE: This is our new endpoint for processing commands.
# "@app.post" means it only accepts POST requests, which are used for sending data.
# The URL will be http://127.0.0.1:8000/process-command
@app.post("/process-command")
def process_command(command: Command):
    # FastAPI automatically takes the incoming JSON, validates it against our Command model,
    # and gives us a clean Python object to work with.
    
    # We can access the text from the command like this:
    received_text = command.text
    print(f"Received command from frontend: {received_text}") # This will print in your terminal

    # For now, we will just send a confirmation message back to the frontend.
    # In the future, this is where our AI logic will go.
    return {"status": "Command received successfully", "command": received_text}

