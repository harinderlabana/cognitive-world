# --- Cognitive World - AI Backend ---
# This file will be the "brain" of our application.
# It uses FastAPI to create a web server that our frontend can talk to.

# First, we import the necessary tools.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# In our next step, we will create a new endpoint, like "/process_command",
# that will receive the text from our voice commands.

