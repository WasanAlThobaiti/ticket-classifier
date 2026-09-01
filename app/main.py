from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import TicketModel
from app.api import tickets
from app.worker.worker import start_background_worker

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_background_worker()
    print("Starting up Ticket Classifier Service...")
    yield
    print("Shutting down gracefully...")

app = FastAPI(
    title="🚀 Ticket Classifier AI Service",
    description="An enterprise-grade, asynchronous AI ticket classification engine.",
    version="1.0.0",
    docs_url=None,
    lifespan=lifespan
)

app.include_router(tickets.router)

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    original_html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Ticket Classifier AI - Premium Edition",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )
    html_content = original_html.body.decode("utf-8")
    custom_css = """
    <style>
        body { background-color: #0f172a !important; color: #f8fafc !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .swagger-ui .topbar { background-color: #1e293b !important; border-bottom: 2px solid #3b82f6; }
        .swagger-ui .info h1, .swagger-ui .info p, .swagger-ui .info table, .swagger-ui .info td, .swagger-ui .info th { color: #f8fafc !important; }
        .swagger-ui .scheme-container { background-color: #1e293b !important; box-shadow: none !important; }
        .swagger-ui .opblock { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 8px !important; }
        .swagger-ui .opblock.opblock-post { border-color: #10b981 !important; background: rgba(16, 185, 129, 0.05) !important; }
        .swagger-ui .opblock.opblock-get { border-color: #3b82f6 !important; background: rgba(59, 130, 246, 0.05) !important; }
        .swagger-ui .btn.execute { background-color: #3b82f6 !important; color: white !important; border-radius: 6px; }
    </style>
    """
    final_html = html_content.replace("</body>", f"{custom_css}</body>")
    return HTMLResponse(final_html)

@app.get("/")
def root():
    return {
        "message": "Welcome to Ticket Classifier Service",
        "service": "Ticket Classifier AI",
        "status": "Online 🚀",
        "documentation": "/docs"
    }

@app.post("/tickets/{ticket_id}/reclassify", status_code=202)
def reclassify_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket.status = "pending"
    ticket.category = None
    ticket.priority = None
    ticket.summary = None
    db.commit()
    
    return {"message": f"Ticket {ticket_id} queued for re-classification", "id": ticket_id, "status": "pending"}