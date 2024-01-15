from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from config.db import engine
from config.models import Tmetric
from schemas.metric import Metric


router = APIRouter(prefix="/metrics",
                    tags=["metrics crud"],
                    responses={status.HTTP_404_NOT_FOUND: {"response": "not found"}})


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@router.post("/savemetric", response_model=dict, status_code = status.HTTP_201_CREATED)
async def savequery(metric_data: Metric, db: Session = Depends(get_db)):
    try:    
        db_metric = metric_data.model_dump()
        db.execute(insert(Tmetric).values(db_metric))
        db.commit()
        return {"response": "metric saved", "id": metric_data.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la metrica: {str(e)}")

@router.get("/metrics/{device_id}", status_code = status.HTTP_200_OK)
async def savequery(device_id: str, db: Session = Depends(get_db)):
    metrics = db.query(Tmetric).filter(Tmetric.device_id == device_id).all()
    if not metrics:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return metrics


