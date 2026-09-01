import time
import threading
from app.database import SessionLocal
from app.models import TicketModel
from app.services.classifier import process_ticket_classification

def background_worker_loop():
    while True:
        db = SessionLocal()
        try:
            # Fetch pending tickets
            pending_tickets = db.query(TicketModel).filter(TicketModel.status == "pending").all()
            
            for ticket in pending_tickets:
                # Process classification with validation and retries
                process_ticket_classification(ticket)
                db.commit()
        except Exception as e:
            print(f"Worker error: {e}")
            db.rollback()
        finally:
            db.close()
        
        # Sleep briefly before checking for new pending tickets
        time.sleep(2)

def start_background_worker():
    worker_thread = threading.Thread(target=background_worker_loop, daemon=True)
    worker_thread.start()