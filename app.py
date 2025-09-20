from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import shutil
from pathlib import Path
import base64
import tempfile

from ai.ai_processor import process_file

app = FastAPI(title="SIH2025_AI - FRA Claim Processor")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 1️⃣ File Upload API (multipart/form-data)
@app.post("/api/process_claim")
async def process_claim(file: UploadFile = File(...)):
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = process_file(str(file_path))
        return JSONResponse(content={"status": "success", "result": result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


# 2️⃣ JSON Upload API (base64 or file path)
class ClaimRequest(BaseModel):
    filename: str
    file_base64: str | None = None   # if backend sends base64 encoded PDF/image
    file_path: str | None = None     # if backend sends existing server file path


@app.post("/webgis/process-json")
async def process_json(req: ClaimRequest):
    try:
        if req.file_base64:
            # Decode base64 to temporary file
            temp_file = UPLOAD_DIR / req.filename
            with open(temp_file, "wb") as f:
                f.write(base64.b64decode(req.file_base64))
            file_path = str(temp_file)

        elif req.file_path:
            file_path = req.file_path  # directly use path if already on server
        else:
            return JSONResponse(status_code=400, content={"status": "error", "message": "No file provided"})

        result = process_file(file_path)
        return JSONResponse(content={"status": "success", "result": result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
