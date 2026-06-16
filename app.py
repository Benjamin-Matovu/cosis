from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis
import os

# Database connection
DATABASE_URL = "postgresql://postgres:devops123@postgres:5432/cosis_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Redis connection
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "COSIS API running! 🎓"}

@app.get("/health")
def health():
    # Check database
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "✅"
    except:
        db_status = "❌"
    
    # Check Redis
    try:
        redis_client.ping()
        redis_status = "✅"
    except:
        redis_status = "❌"
    
    return {
        "database": db_status,
        "redis": redis_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
