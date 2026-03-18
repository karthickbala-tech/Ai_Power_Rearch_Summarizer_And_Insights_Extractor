import uuid, os, shutil
from fastapi import APIRouter, UploadFile, File, Depends
from app.services.ingestion_service import ingest_pdf
from app.core.config import DATA_DIR
from app.auth.auth_bearer import jwt_guard

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...), user=Depends(jwt_guard)):
    paper_id = str(uuid.uuid4())
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{paper_id}.pdf")
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    ingest_pdf(path, paper_id)
    return {"paper_id": paper_id}