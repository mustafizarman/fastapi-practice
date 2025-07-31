
import os
from datetime import datetime
from pathlib import Path
from typing import IO
from fastapi import UploadFile, HTTPException, status
from src.core.config import settings

VALID_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}

def validate_image_extension(filename: str):
    ext = filename.split(".")[-1].lower()
    if ext not in VALID_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image file extension. Allowed: {', '.join(VALID_IMAGE_EXTENSIONS)}"
        )

async def save_profile_picture(file: UploadFile, user_id: int) -> str:
    validate_image_extension(file.filename)

    Path(settings.PROFILE_PICS_DIR).mkdir(parents=True, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    file_name = f"user_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
    file_path = os.path.join(settings.PROFILE_PICS_DIR, file_name)

    try:
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)  # Read 1MB chunks
                if not chunk:
                    break
                buffer.write(chunk)
        return file_path
    except Exception as e:
        # Clean up if save fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not save file: {e}")

def delete_profile_picture(file_path: str):
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}") 