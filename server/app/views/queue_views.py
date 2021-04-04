import os
import uuid
import aiofiles

from celery.result import AsyncResult
from fastapi.responses import FileResponse, JSONResponse
from fastapi import File, UploadFile, Request, APIRouter

from validators import is_valid_image
from workers.tasks import image_to_thumbnail


router = APIRouter()


@router.post('/thumbnail-queue/', status_code=202)
async def resize_image_queue(request: Request, image: UploadFile = File(...)):

    from main import VALID_IMAGE_EXTENSIONS, STATIC_FILE_LOCATION
    if not is_valid_image(image.file, image.filename, VALID_IMAGE_EXTENSIONS):
        return JSONResponse(status_code=400,
                            content={"Error": f"Image is not valid. Please ensure extension and file is of one of the following formats: {VALID_IMAGE_EXTENSIONS}"})

    image_extension = os.path.splitext(image.filename)[1]
    thumbnail_id = str(uuid.uuid4())
    thumbnail_name = thumbnail_id + image_extension
    file_location = os.path.join(STATIC_FILE_LOCATION, thumbnail_name)

    async with aiofiles.open(file_location, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)

    image_to_thumbnail.apply_async(args=[file_location, thumbnail_name], task_id=thumbnail_id)

    thumbnail_url = os.path.join(str(request.url), thumbnail_name)

    return {'Resized image URL': thumbnail_url}


@router.get('/thumbnail-queue/{thumbnail_name}', status_code=200)
async def return_resized_image_queue(thumbnail_name: str):

    thumbnail_id = os.path.splitext(thumbnail_name)[0]
    result_status = AsyncResult(thumbnail_id).status

    if result_status == 'SUCCESS':
        return FileResponse(thumbnail_name)
    else:
        return JSONResponse(status_code=409, content={"Processing": f"Current status of image processing is {result_status}."})
