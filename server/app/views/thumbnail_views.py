import os
import uuid

from celery.result import AsyncResult
from fastapi.responses import FileResponse, JSONResponse
from fastapi import File, UploadFile, Request, APIRouter, BackgroundTasks, Form

from validators import is_valid_image
from workers.tasks import image_to_thumbnail


router = APIRouter()


def save_file(file, file_location):
    with open(file_location, 'wb') as out_file:
        while content := file.read(1024):
            out_file.write(content)


@router.post('/thumbnails/', status_code=202)
async def resize_image_to_thumbnail(request: Request, background_tasks: BackgroundTasks, image: UploadFile = File(...), sizes: str = Form(...)):

    from main import VALID_IMAGE_EXTENSIONS, STATIC_FILE_LOCATION
    if not is_valid_image(image.file, image.filename, VALID_IMAGE_EXTENSIONS):
        return JSONResponse(status_code=400,
                            content={"error": f"Image is not valid. Please ensure extension and file is of one of the following formats: {VALID_IMAGE_EXTENSIONS}"})

    image_extension = os.path.splitext(image.filename)[1]
    original_image = str(uuid.uuid4())
    file_location = os.path.join(STATIC_FILE_LOCATION, original_image)

    background_tasks.add_task(save_file, image.file, file_location)

    response_json = {}
    for size in sizes.split(','):

        generated_thumbnail_id = str(uuid.uuid4())
        generated_thumbnail_name = generated_thumbnail_id + image_extension
        image_to_thumbnail.apply_async(args=[file_location, generated_thumbnail_name, size], task_id=generated_thumbnail_id)
        thumbnail_url = os.path.join(str(request.url), generated_thumbnail_name)
        response_json[size] = thumbnail_url

    return response_json


@router.get('/thumbnails/{thumbnail_name}', status_code=200)
async def return_thumbnail(thumbnail_name: str):

    from main import STATIC_FILE_LOCATION
    thumbnail_id = os.path.splitext(thumbnail_name)[0]
    thumbnail_location = os.path.join(STATIC_FILE_LOCATION, thumbnail_name)
    thumbnail_extension = thumbnail_location.split('.')[1]

    result_status = AsyncResult(thumbnail_id).status

    if result_status == 'SUCCESS' and os.path.isfile(thumbnail_location):
        return FileResponse(thumbnail_location, media_type=f'image/{thumbnail_extension}')
    elif not os.path.isfile(thumbnail_location):
        return JSONResponse(status_code=404, content={"error": f"Image {thumbnail_name} not found."})
    elif not result_status == 'SUCCESS':
        return JSONResponse(status_code=409, content={"processing": f"Current status of image processing is {result_status}."})
