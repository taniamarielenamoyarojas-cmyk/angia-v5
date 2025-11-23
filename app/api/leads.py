"""
API endpoints para gestión de leads
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.webhook import LeadCreate, LeadResponse
from app.models.lead import Lead, LeadStatusEnum, OperatorEnum
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/", response_model=LeadResponse, status_code=201)
async def create_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo lead manualmente
    
    Args:
        lead_data: Datos del lead
        db: Sesión de base de datos
    
    Returns:
        Lead creado
    """
    # Verificar si ya existe
    existing_lead = db.query(Lead).filter(Lead.phone_number == lead_data.phone_number).first()
    if existing_lead:
        raise HTTPException(status_code=400, detail="Lead ya existe con este número de teléfono")
    
    # Crear lead
    lead = Lead(
        phone_number=lead_data.phone_number,
        name=lead_data.name,
        email=lead_data.email,
        current_operator=OperatorEnum(lead_data.current_operator) if lead_data.current_operator else None,
        target_operator=OperatorEnum(lead_data.target_operator),
        notes=lead_data.notes,
        status=LeadStatusEnum.PENDING
    )
    
    db.add(lead)
    db.commit()
    db.refresh(lead)
    
    logger.info(f"✅ Lead creado manualmente: {lead.phone_number}")
    
    return lead


@router.get("/", response_model=List[LeadResponse])
async def list_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    target_operator: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Listar leads con filtros opcionales
    
    Args:
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a retornar
        status: Filtrar por estado (opcional)
        target_operator: Filtrar por operador objetivo (opcional)
        db: Sesión de base de datos
    
    Returns:
        Lista de leads
    """
    query = db.query(Lead)
    
    # Aplicar filtros
    if status:
        query = query.filter(Lead.status == LeadStatusEnum(status))
    
    if target_operator:
        query = query.filter(Lead.target_operator == OperatorEnum(target_operator))
    
    # Paginación
    leads = query.offset(skip).limit(limit).all()
    
    return leads


@router.get("/{phone_number}", response_model=LeadResponse)
async def get_lead(phone_number: str, db: Session = Depends(get_db)):
    """
    Obtener un lead por número de teléfono
    
    Args:
        phone_number: Número de teléfono del lead
        db: Sesión de base de datos
    
    Returns:
        Lead encontrado
    """
    lead = db.query(Lead).filter(Lead.phone_number == phone_number).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    
    return lead


@router.put("/{phone_number}/status", response_model=LeadResponse)
async def update_lead_status(
    phone_number: str,
    status: str,
    db: Session = Depends(get_db)
):
    """
    Actualizar estado de un lead
    
    Args:
        phone_number: Número de teléfono del lead
        status: Nuevo estado
        db: Sesión de base de datos
    
    Returns:
        Lead actualizado
    """
    lead = db.query(Lead).filter(Lead.phone_number == phone_number).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    
    try:
        lead.status = LeadStatusEnum(status)
        db.commit()
        db.refresh(lead)
        
        logger.info(f"✅ Estado actualizado: {phone_number} -> {status}")
        
        return lead
        
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Estado inválido: {status}")


@router.get("/stats/summary")
async def get_stats_summary(db: Session = Depends(get_db)):
    """
    Obtener resumen estadístico de leads
    
    Args:
        db: Sesión de base de datos
    
    Returns:
        Estadísticas de leads
    """
    total_leads = db.query(Lead).count()
    
    stats = {
        "total_leads": total_leads,
        "by_status": {},
        "by_operator": {}
    }
    
    # Contar por estado
    for status in LeadStatusEnum:
        count = db.query(Lead).filter(Lead.status == status).count()
        stats["by_status"][status.value] = count
    
    # Contar por operador
    for operator in OperatorEnum:
        count = db.query(Lead).filter(Lead.target_operator == operator).count()
        stats["by_operator"][operator.value] = count
    
    return stats
