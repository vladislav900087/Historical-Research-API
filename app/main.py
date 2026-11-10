from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.dependencies import get_db

from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

@app.get('/health')
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return {'status': 'healthy', 'database': 'connected'}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Database connection failed: {e}')

