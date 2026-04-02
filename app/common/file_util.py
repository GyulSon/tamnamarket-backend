import os
import shutil
from fastapi import UploadFile

# Base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def save_upload_file(upload_file: UploadFile, sub_folder: str) -> str:
    """
    Save an uploaded file to the local static directory (e.g., 'images' or 'voices').
    Returns the relative path string, e.g., '/static/images/filename.jpg'.
    """
    folder_path = os.path.join(BASE_DIR, "static", sub_folder)
    os.makedirs(folder_path, exist_ok=True)
    
    file_location = os.path.join(folder_path, upload_file.filename)
    
    # Read/Write file (Synchronously using standard Python context for simplicity/compatibility)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(upload_file.file, file_object)
        
    return f"/static/{sub_folder}/{upload_file.filename}"
