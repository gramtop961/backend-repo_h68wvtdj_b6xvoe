import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Tee, Subscriber

app = FastAPI(title="Limited Edition Tees API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Limited Edition Tees API running"}

@app.get("/api/tees/current", response_model=List[Tee])
def get_current_tees(month: Optional[str] = None):
    """
    Return tees for the provided month (YYYY-MM). If not provided, uses the current month.
    """
    try:
        from datetime import datetime
        target_month = month or datetime.utcnow().strftime("%Y-%m")
        filter_dict = {"release_month": target_month, "status": "current"}
        docs = get_documents("tee", filter_dict)
        # Convert ObjectId and other non-serializables if needed
        for d in docs:
            d.pop("_id", None)
        return [Tee(**d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tees/archive", response_model=List[Tee])
def get_archive(limit: int = 24):
    try:
        docs = get_documents("tee", {"status": "archived"}, limit=limit)
        for d in docs:
            d.pop("_id", None)
        return [Tee(**d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/subscribe")
def subscribe(sub: Subscriber):
    try:
        # De-dup by email for simplicity
        existing = db["subscriber"].find_one({"email": sub.email}) if db else None
        if existing:
            return {"status": "ok", "message": "You're already subscribed."}
        create_document("subscriber", sub)
        return {"status": "ok", "message": "Subscribed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db

        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
