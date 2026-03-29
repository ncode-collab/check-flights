# AI Flight Search Assistant

A multi-agent AI application that allows users to search for flights using natural language. It uses the Gemini 2.0 Flash model (via `google-genai`) to parse user intent and the Duffel API to fetch real-time flight offers.

## Features

- **Natural Language Parsing:** Automatically extracts origin, destination, and dates from user queries.
- **Intelligent Defaults:** Automatically sets departure dates (e.g., tomorrow) if none are specified.
- **Real-time Search:** Fetches live flight data from multiple airlines via the Duffel API.
- **Conversational UI:** A clean web interface for chatting with the assistant.

## Prerequisites

- Python 3.9+
- A Google Gemini API Key
- A Duffel API Key

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd check-flights
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    DUFFEL_API_KEY=your_duffel_api_key_here
    ```

## Running the Application

1.  **Start the server:**
    ```bash
    python3 main.py
    ```

2.  **Access the UI:**
    Open your browser and navigate to `http://localhost:8000`.

3.  **Example Prompts:**
    - "I want to go to paris from London"
    - "Are there any flights from New York to Tokyo next Friday?"
    - "Find me the cheapest flight from San Francisco to Berlin for May 15th."

## Project Structure

- `main.py`: Entry point for the FastAPI application.
- `agents/orchestrator.py`: Handles intent parsing and response summarization using Gemini.
- `agents/flight_search.py`: Manages communication with the Duffel API (using raw HTTP for reliability).
- `static/`: Frontend assets (HTML, CSS, JS).
- `requirements.txt`: Python package dependencies.
