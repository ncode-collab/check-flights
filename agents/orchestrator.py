import os
import json
from typing import Dict, Any, Optional
from google import genai
from dotenv import load_dotenv

load_dotenv()

class OrchestratorAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-3-flash-preview"
        
    def parse_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input to extract flight parameters.
        Returns a JSON object with flight parameters or natural response if no flight intent.
        """
        prompt = f"""
        You are an AI Flight Search Orchestrator. Your goal is to extract flight search parameters from user input.
        
        If flight-related intent is detected:
        Extract and normalize flight constraints into a JSON object.
        JSON schema:
        {{ "origin": "string (IATA code or City)", "destination": "string (IATA code or City)", "departure_date": "YYYY-MM-DD", "return_date": "YYYY-MM-DD | null", "price_limit": "number | null", "passengers": "number | 1" }}
        
        Rules:
        - Dates must be normalized to ISO format (YYYY-MM-DD). If no year is mentioned, assume 2026.
        - If no departure_date is mentioned, assume tomorrow's date (2026-03-30) as a default.
        - Normalize origin/destination to IATA codes if possible.
        - If a field is not provided, infer when reasonable, otherwise set to null.
        - Output the JSON object wrapped in triple backticks: ```json ... ```
        
        If no flight-related intent is detected:
        Respond naturally and helpfully as a general conversational assistant.
        Output your response as a simple string, NOT JSON.

        User input: "{user_input}"
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            text = response.text.strip()
            
            # Try to extract JSON from backticks
            if "```json" in text:
                json_part = text.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_part)
                return {"type": "flight_search", "params": data}
            
            # If no JSON backticks but it looks like JSON
            if text.startswith("{") and text.endswith("}"):
                data = json.loads(text)
                return {"type": "flight_search", "params": data}
                
            # Otherwise treat as chat response
            return {"type": "chat_response", "message": text}
            
        except Exception as e:
            # If it's a quota error, provide a friendly message
            error_str = str(e)
            if "RESOURCE_EXHAUSTED" in error_str:
                return {"type": "chat_response", "message": "I'm currently experiencing high demand. Please try again in a moment."}
            
            # Fallback for parsing errors
            if 'text' in locals() and text:
                return {"type": "chat_response", "message": text}
            
            return {"type": "chat_response", "message": "I'm sorry, I'm having trouble processing that right now."}

    def summarize_results(self, user_input: str, flight_data: Any) -> str:
        """
        Generate a natural language summary of the flight search results.
        """
        if not flight_data or (isinstance(flight_data, dict) and "error" in flight_data):
            return "I'm sorry, I couldn't find any flights matching your criteria."

        prompt = f"""
        You are an AI Flight Assistant. You just performed a flight search for the user: "{user_input}"
        
        Here are the results:
        {json.dumps(flight_data[:5], indent=2)} # Top 5 results
        
        Provide a concise natural-language recommendation (e.g., cheapest, fastest, best value).
        Highlight key details like price and airline.
        Keep it friendly and helpful.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"I found some flights for you, but I had trouble summarizing them. Error: {str(e)}"
