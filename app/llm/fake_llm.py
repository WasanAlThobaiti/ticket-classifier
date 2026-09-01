import random

class FakeLLM:
    @staticmethod
    def classify_ticket(subject: str, body: str) -> dict:
        text = f"{subject} {body}".lower()
        
        # Handle prompt injection or bad inputs simulation for testing
        if "ignore all previous instructions" in text:
            return {
                "category": "banana", # Invalid category to test validation
                "priority": "SUPER HIGH", # Invalid priority
                "summary": "Attempted prompt injection detected."
            }
            
        if "payment" in text or "charged" in text or "bill" in text:
            return {
                "category": "billing",
                "priority": "high",
                "summary": "Customer reports a billing or payment issue."
            }
        elif "log in" in text or "password" in text or "access" in text:
            return {
                "category": "account",
                "priority": "medium",
                "summary": "Customer is experiencing account access issues."
            }
        elif "error" in text or "bug" in text or "crash" in text:
            return {
                "category": "technical",
                "priority": "high",
                "summary": "Customer reported a technical bug or system error."
            }
        else:
            return {
                "category": "other",
                "priority": "low",
                "summary": "General inquiry or feedback."
            }