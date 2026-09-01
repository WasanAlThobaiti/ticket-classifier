from app.llm.fake_llm import FakeLLM

VALID_CATEGORIES = ["billing", "technical", "account", "other"]
VALID_PRIORITIES = ["low", "medium", "high"]

def validate_llm_output(output: dict) -> bool:
    category = output.get("category")
    priority = output.get("priority")
    
    if category not in VALID_CATEGORIES:
        return False
    if priority not in VALID_PRIORITIES:
        return False
    return True

def process_ticket_classification(ticket):
    # Simulate LLM call
    raw_result = FakeLLM.classify_ticket(ticket.subject, ticket.body)
    
    if validate_llm_output(raw_result):
        ticket.category = raw_result["category"]
        ticket.priority = raw_result["priority"]
        ticket.summary = raw_result["summary"]
        ticket.status = "classified"
        return True
    else:
        # Increment retry count or mark as failed if max retries reached
        ticket.retry_count += 1
        if ticket.retry_count >= 2:
            ticket.status = "failed"
        else:
            ticket.status = "pending" # Keep pending for next retry
        return False