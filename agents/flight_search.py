import os
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv

load_dotenv()

class FlightSearchAgent:
    def __init__(self):
        self.api_token = os.getenv("DUFFEL_API_KEY")
        if not self.api_token:
            raise ValueError("DUFFEL_API_KEY not found in environment variables.")
        self.base_url = "https://api.duffel.com/air"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Duffel-Version": "v2",
            "Content-Type": "application/json"
        }

    def search_flights(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query Duffel API for flight search results using raw HTTP.
        """
        try:
            # 1. Create Offer Request
            offer_request_url = f"{self.base_url}/offer_requests"
            
            # Ensure we have required params
            origin = params.get("origin")
            destination = params.get("destination")
            departure_date = params.get("departure_date")
            
            if not all([origin, destination, departure_date]):
                return {"error": "Missing required search parameters (origin, destination, or departure_date)"}

            payload = {
                "data": {
                    "slices": [
                        {
                            "origin": origin,
                            "destination": destination,
                            "departure_date": departure_date,
                        }
                    ],
                    "passengers": [{"type": "adult"}] * params.get("passengers", 1)
                }
            }

            resp = requests.post(offer_request_url, headers=self.headers, json=payload)
            if resp.status_code != 201:
                return {"error": f"API Error (Offer Request): {resp.text}"}
            
            offer_request_id = resp.json()["data"]["id"]

            # 2. List Offers
            offers_url = f"{self.base_url}/offers?offer_request_id={offer_request_id}"
            resp = requests.get(offers_url, headers=self.headers)
            if resp.status_code != 200:
                return {"error": f"API Error (List Offers): {resp.text}"}
            
            offers = resp.json()["data"]

            formatted_results = []
            for offer in offers:
                first_slice = offer["slices"][0]
                first_segment = first_slice["segments"][0]
                
                formatted_results.append({
                    "id": offer["id"],
                    "airline": offer["owner"]["name"],
                    "price": float(offer["total_amount"]),
                    "currency": offer["total_currency"],
                    "departure_time": first_segment["departing_at"],
                    "arrival_time": first_segment["arriving_at"],
                    "duration": first_slice["duration"],
                    "stops": len(first_slice["segments"]) - 1,
                    "origin": first_segment["origin"]["iata_code"],
                    "destination": first_segment["destination"]["iata_code"]
                })

            return formatted_results

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error in FlightSearchAgent: {e}")
            return {"error": str(e)}
