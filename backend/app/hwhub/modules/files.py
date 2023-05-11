from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from typing import List

import os
import aiofiles

router = APIRouter(
    prefix="/api/v0.1/files",
    responses={404: {"description": "Not found"}},
    tags=["Files"],
)

FILES_PATH = '/../upload_files/'


def make_unique_filename(filename):
    """
    Given a filename, returns a unique filename by appending a number to the end of the filename
    if a file with that name already exists.
    """
    filename = filename.lower().replace(" ", "_")
    if not os.path.exists(filename):
        # If the filename doesn't exist, it's already unique
        return filename

    # If the filename exists, add a number to the end to make it unique
    i = 1
    while True:
        new_filename = f"{os.path.splitext(filename)[0]}_{i}{os.path.splitext(filename)[1]}"
        if not os.path.exists(new_filename):
            return new_filename
        i += 1


@router.post("/upload")
async def upload_file(files: List[UploadFile]):
    try:
        file_names = []
        for in_file in files:
            new_file_name = make_unique_filename(in_file.filename)
            out_file_path = FILES_PATH + new_file_name
            async with aiofiles.open(out_file_path, 'wb') as out_file:
                content = await in_file.read()  # async read
                await out_file.write(content)  # async write
            file_names.append(new_file_name)

        return {"status": 200, "files": file_names}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str):
    try:
        return FileResponse(FILES_PATH + filename)
    except Exception as e:
        return {"status": 500, "error": str(e)}
