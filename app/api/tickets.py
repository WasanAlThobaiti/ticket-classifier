from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import TicketModel
from app.schemas import TicketCreate, TicketResponse
router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=TicketResponse)
def create_ticket(ticket_in: TicketCreate, db: Session = Depends(get_db)):
    # Check for duplicate tickets
    existing_ticket = db.query(TicketModel).filter(TicketModel.id == ticket_in.id).first()
    if existing_ticket:
        return existing_ticket
    
    # Create new ticket with pending status
    new_ticket = TicketModel(
        id=ticket_in.id,
        subject=ticket_in.subject,
        body=ticket_in.body,
        status="pending"
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.get("/", response_model=List[TicketResponse])
def list_tickets(
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    query = db.query(TicketModel)
    
    if category:
        query = query.filter(TicketModel.category == category)
    if priority:
        query = query.filter(TicketModel.priority == priority)
        
    offset = (page - 1) * page_size
    tickets = query.offset(offset).limit(page_size).all()
    return tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket