"""
Script para importar leads desde archivo CSV
"""

import csv
import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.database import get_db_context
from app.models.lead import Lead, OperatorEnum, LeadStatusEnum
from sqlalchemy.exc import IntegrityError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def import_leads_from_csv(csv_file_path: str, target_operator: str = "CLARO"):
    """
    Importar leads desde archivo CSV
    
    Formato esperado del CSV:
    phone_number,name,email,current_operator,notes
    +51987654321,Juan Pérez,juan@example.com,WOW,Cliente interesado
    
    Args:
        csv_file_path: Ruta al archivo CSV
        target_operator: Operador objetivo por defecto (CLARO, WOW, WIN)
    """
    logger.info(f"📂 Importando leads desde: {csv_file_path}")
    logger.info(f"🎯 Operador objetivo: {target_operator}")
    
    imported_count = 0
    skipped_count = 0
    error_count = 0
    
    with get_db_context() as db:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    # Validar campos requeridos
                    if not row.get('phone_number'):
                        logger.warning(f"⚠️ Fila sin número de teléfono, saltando...")
                        skipped_count += 1
                        continue
                    
                    # Verificar si ya existe
                    existing_lead = db.query(Lead).filter(
                        Lead.phone_number == row['phone_number']
                    ).first()
                    
                    if existing_lead:
                        logger.info(f"⏭️ Lead ya existe: {row['phone_number']}, saltando...")
                        skipped_count += 1
                        continue
                    
                    # Crear lead
                    lead = Lead(
                        phone_number=row['phone_number'],
                        name=row.get('name'),
                        email=row.get('email'),
                        current_operator=OperatorEnum(row['current_operator']) if row.get('current_operator') else None,
                        target_operator=OperatorEnum(target_operator),
                        notes=row.get('notes'),
                        status=LeadStatusEnum.PENDING
                    )
                    
                    db.add(lead)
                    db.commit()
                    
                    imported_count += 1
                    logger.info(f"✅ Lead importado: {row['phone_number']}")
                    
                except IntegrityError as e:
                    db.rollback()
                    logger.error(f"❌ Error de integridad: {row.get('phone_number')} - {str(e)}")
                    error_count += 1
                    
                except Exception as e:
                    db.rollback()
                    logger.error(f"❌ Error importando: {row.get('phone_number')} - {str(e)}")
                    error_count += 1
    
    # Resumen
    logger.info("\n" + "="*50)
    logger.info("📊 RESUMEN DE IMPORTACIÓN")
    logger.info("="*50)
    logger.info(f"✅ Importados: {imported_count}")
    logger.info(f"⏭️ Saltados: {skipped_count}")
    logger.info(f"❌ Errores: {error_count}")
    logger.info(f"📈 Total procesados: {imported_count + skipped_count + error_count}")
    logger.info("="*50)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Importar leads desde CSV")
    parser.add_argument("csv_file", help="Ruta al archivo CSV")
    parser.add_argument(
        "--operator",
        choices=["CLARO", "WOW", "WIN"],
        default="CLARO",
        help="Operador objetivo (por defecto: CLARO)"
    )
    
    args = parser.parse_args()
    
    import_leads_from_csv(args.csv_file, args.operator)
