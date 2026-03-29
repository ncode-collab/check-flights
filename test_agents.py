from agents.orchestrator import OrchestratorAgent
import json

def test_parsing():
    agent = OrchestratorAgent()
    
    # Test flight query
    query1 = "Find me a flight from London to Paris on March 15th 2026 for 2 people"
    result1 = agent.parse_intent(query1)
    print(f"Query 1: {query1}")
    print(f"Result 1: {json.dumps(result1, indent=2)}")
    
    # Test general query
    query2 = "What's the weather like?"
    result2 = agent.parse_intent(query2)
    print(f"\nQuery 2: {query2}")
    print(f"Result 2: {json.dumps(result2, indent=2)}")

if __name__ == "__main__":
    test_parsing()
