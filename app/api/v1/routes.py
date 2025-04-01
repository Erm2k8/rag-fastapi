from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from typing import Annotated
from services.query import QueryService
from .schemas import QueryRequest, ResponseModel
from .dependencies import get_query_service

router = APIRouter()

@router.get("/")
async def index():
    return {"message": "Hello, world!"}

@router.post("/query/", response_model=ResponseModel)
async def handle_query(
    request: QueryRequest,
    query_service: QueryService = Depends(get_query_service)
):
    try:
        format_pdf_path = f'data/documents/{request.pdf_path}'
        return query_service.execute_query(
            pdf_path=format_pdf_path,
            query=request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

