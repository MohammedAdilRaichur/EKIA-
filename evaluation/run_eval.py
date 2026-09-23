import os
import sys
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from langchain_core.messages import HumanMessage
from app.agent.graph import app_graph

test_questions = [
    "What is the accommodation limit for business travel according to the Travel Policy?",
    "I'm travelling for 3 days. What is my total accommodation limit?",
    "How many employees are in the Engineering department?",
    "What should I do if my company laptop is compromised?"
]

def run_evaluation():
    print("Starting EKIA Evaluation...")
    print("-" * 50)
    
    for idx, question in enumerate(test_questions, 1):
        print(f"\nQ{idx}: {question}")
        try:
            response = app_graph.invoke({"messages": [HumanMessage(content=question)]})
            answer = response["messages"][-1].content
            print(f"Answer: {answer}\n")
            
            # Print intermediate tool calls if present
            for msg in response["messages"]:
                if msg.type == "tool":
                    print(f"[Tool Usage Detected] -> {msg.name}")
                    
        except Exception as e:
            print(f"Error executing question: {e}")
            
    print("-" * 50)
    print("Evaluation Complete.")

if __name__ == "__main__":
    run_evaluation()
