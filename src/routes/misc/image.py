import os
import uuid
from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from config import get_config

route = APIRouter(prefix="/image", tags=["Image"])

config = get_config()


@route.get("/{filename}")
async def get_image(filename: str):
    file_path = config.image.directory / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    return FileResponse(file_path)


@route.post("/upload")
async def upload_image(
    file: UploadFile = File(...), custom_filename: Optional[str] = None
):
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in config.image.allower_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {config.image.allower_extensions}",
        )

    filename = custom_filename or f"{uuid.uuid4()}{file_ext}"
    save_path = config.image.directory / filename

    file_size = 0
    async with aiofiles.open(save_path, "wb") as buffer:
        while content := await file.read(1024):
            file_size += len(content)
            if file_size > config.image.max_size_mb * 1024 * 1024:
                await buffer.close()
                os.remove(save_path)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File too large. Max size: {config.image.max_size_mb}MB",
                )
            await buffer.write(content)

    return {"filename": filename, "size": file_size}


@route.delete("/{filename}")
async def delete_image(filename: str):
    file_path = config.image.directory / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    try:
        os.remove(file_path)
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting image: {str(e)}",
        )
