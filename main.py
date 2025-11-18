import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Program, Event, Leader, Testimonial, FAQ, Registration


app = FastAPI(title="All Male Area API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "All Male Area API running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": [],
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"
    return response


# ---------- Content Endpoints ----------

@app.get("/api/programs", response_model=List[Program])
def list_programs():
    docs = get_documents("program", {}, None)
    # Convert Mongo dicts to Program list
    programs: List[Program] = []
    for d in docs:
        d.pop("_id", None)
        programs.append(Program(**d))
    programs.sort(key=lambda p: p.order)
    return programs


@app.get("/api/events", response_model=List[Event])
def list_events(program: Optional[str] = None):
    filt = {"program_slug": program} if program else {}
    docs = get_documents("event", filt, None)
    out: List[Event] = []
    for d in docs:
        d.pop("_id", None)
        # Convert possible string dates
        if isinstance(d.get("starts_at"), str):
            d["starts_at"] = datetime.fromisoformat(d["starts_at"])  # type: ignore
        if isinstance(d.get("ends_at"), str) and d["ends_at"]:
            d["ends_at"] = datetime.fromisoformat(d["ends_at"])  # type: ignore
        out.append(Event(**d))
    # Sort by next date
    out.sort(key=lambda e: e.starts_at)
    return out


@app.get("/api/leaders", response_model=List[Leader])
def list_leaders():
    docs = get_documents("leader", {}, None)
    out: List[Leader] = []
    for d in docs:
        d.pop("_id", None)
        out.append(Leader(**d))
    return out


@app.get("/api/testimonials", response_model=List[Testimonial])
def list_testimonials():
    docs = get_documents("testimonial", {}, None)
    out: List[Testimonial] = []
    for d in docs:
        d.pop("_id", None)
        out.append(Testimonial(**d))
    return out


@app.get("/api/faq", response_model=List[FAQ])
def list_faq():
    docs = get_documents("faq", {}, None)
    out: List[FAQ] = []
    for d in docs:
        d.pop("_id", None)
        out.append(FAQ(**d))
    return out


# ---------- Registration Endpoint ----------

class RegistrationCreated(BaseModel):
    id: str
    status: str


@app.post("/api/register", response_model=RegistrationCreated)
def register(reg: Registration):
    try:
        inserted_id = create_document("registration", reg)
        return {"id": inserted_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
