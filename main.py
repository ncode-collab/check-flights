
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents.orchestrator import OrchestratorAgent
from agents.flight_search import FlightSearchAgent
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize agents
orchestrator = OrchestratorAgent()
flight_search = FlightSearchAgent()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_input = request.message
    
    # Agent 1: Parse intent
    intent = orchestrator.parse_intent(user_input)
    
    if intent["type"] == "chat_response":
        return {
            "chat_response": intent["message"],
            "flight_data": None
        }
    
    # Agent 1 → Agent 2: Perform flight search
    flight_params = intent["params"]
    print(f"Extracted flight parameters: {flight_params}")
    
    flight_data = flight_search.search_flights(flight_params)
    
    # Agent 2 → Agent 1: Summarize results
    summary = orchestrator.summarize_results(user_input, flight_data)
    
    return {
        "chat_response": summary,
        "flight_data": flight_data
    }

@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
