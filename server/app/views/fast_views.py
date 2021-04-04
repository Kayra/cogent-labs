import os
import uuid

from fastapi.responses import FileResponse, JSONResponse
from fastapi import File, UploadFile, BackgroundTasks, Request, APIRouter

from validators import is_valid_image
from worker import image_to_thumbnail


router = APIRouter()


@router.post('/thumbnail/', status_code=202)
async def resize_image(request: Request, background_tasks: BackgroundTasks, image: UploadFile = File(...)):

    from main import VALID_IMAGE_EXTENSIONS
    if not is_valid_image(image.file, image.filename, VALID_IMAGE_EXTENSIONS):
        return JSONResponse(status_code=400,
                            content={"Error": f"Image is not valid. Please ensure extension and file is of one of the following formats: {VALID_IMAGE_EXTENSIONS}"})

    image_extension = os.path.splitext(image.filename)[1]
    thumbnail_name = str(uuid.uuid4()) + image_extension

    background_tasks.add_task(image_to_thumbnail, image.file, thumbnail_name)

    thumbnail_url = os.path.join(str(request.url), thumbnail_name)

    return {'Resized image URL': thumbnail_url}


@router.get('/thumbnail/{thumbnail_name}', status_code=200)
async def return_resized_image(thumbnail_name: str):

    if os.path.isfile(thumbnail_name):
        return FileResponse(thumbnail_name)
    else:
        return JSONResponse(status_code=404, content={"Error": "Image not found"})